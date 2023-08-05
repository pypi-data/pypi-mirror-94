import dataclasses
import json
import logging
import os
import subprocess
import tarfile
import tempfile

import dacite
import falcon.asgi
from whitesource_common import protocol

import model
import paths
import util


class Component:

    async def on_websocket(self, req: falcon.Request, ws: falcon.asgi.WebSocket):

        try:
            log = logging.getLogger(__name__)
            await ws.accept()

            log.info('receiving metadata...')
            try:
                metadata = dacite.from_dict(
                    data_class=protocol.WhiteSourceApiExtensionWebsocketMetadata,
                    data=json.loads(await ws.receive_text()),
                )

                log.info('receiving whitesource config...')
                ws_config = dacite.from_dict(
                    data_class=protocol.WhiteSourceApiExtensionWebsocketWSConfig,
                    data=json.loads(await ws.receive_text()),
                )

            except (json.decoder.JSONDecodeError, dacite.exceptions.MissingValueError):
                await ws.close(
                    code=protocol.WhiteSourceApiExtensionStatusCodeReasons.CONTRACT_VIOLATION.value
                )
                return

            if metadata.chunkSize > metadata.length:
                await ws.close(
                    code=protocol.WhiteSourceApiExtensionStatusCodeReasons.CHUNK_SIZE_TOO_BIG.value
                )
                return

            with tempfile.TemporaryDirectory() as tmp_dir:
                log.info('receiving binary...')
                with tempfile.NamedTemporaryFile() as tar_file:
                    received = 0
                    while received < metadata.length:
                        chunk = await ws.receive_data()
                        tar_file.write(chunk)
                        log.info(
                            f'{util.sizeof_fmt(received)}/{util.sizeof_fmt(metadata.length)}\
                               ({received}/{metadata.length})'
                        )
                        received += len(chunk)
                    tar_file.seek(0)
                    log.info(
                        f'{util.sizeof_fmt(received)}/{util.sizeof_fmt(metadata.length)}\
                           ({received}/{metadata.length})'
                    )

                    try:
                        # extract tar
                        with tarfile.open(fileobj=tar_file, mode='r|*', bufsize=1024) as f:
                            while tar_info := f.next():
                                f.extract(tar_info, path=tmp_dir)
                    except (
                            tarfile.ReadError,
                            UnicodeDecodeError,
                            tarfile.InvalidHeaderError,
                    ):
                        await ws.close(
                            code=protocol.WhiteSourceApiExtensionStatusCodeReasons
                                .BINARY_CORRUPTED.value
                        )
                        return

                log.info('starting scan...')
                wss_agent_hardlink_path = util.get_wss_agent_hardlink(tmp_dir=tmp_dir)
                result = _scan_component(
                    wss_agent_dir=tmp_dir,
                    component_path=tmp_dir,
                    ws_config=ws_config,
                )

                os.unlink(wss_agent_hardlink_path)

                if result.returncode == 0:
                    log.info('scan finished successfully.')
                    res = _build_scan_result_response(successful=True,
                                                      message='scan finished successfully')
                else:
                    msg = _check_err_result(result=result)
                    res = _build_scan_result_response(successful=False,
                                                      message=msg)

                await ws.send_text(json.dumps(dataclasses.asdict(res)))

        except falcon.WebSocketDisconnected:
            return


def _build_scan_result_response(
    successful: bool,
    message: str,
):
    res = {
        'successful': successful,
        'message': message
    }
    res = dacite.from_dict(
        data_class=model.ScanResult,
        data=res
    )
    return res


def _check_err_result(result: subprocess.CompletedProcess):
    err_string = (result.stderr.decode('utf-8') or '') + (result.stdout.decode('utf-8') or '')
    if result.returncode == 251:
        logging.error(f'Error: {result.returncode}. invalid userKey or apiKey')
        return f'{result.returncode}: invalid userKey or apiKey\n{err_string}'

    elif result.returncode == 252:
        logging.error(f'Error: {result.returncode}. Invalid productToken or wss.url')
        return f'{result.returncode}: invalid productToken or wss.url\n{err_string}'

    else:
        logging.error(f'scan finished with {result.returncode}. Unknown error code')
        return f'{result.returncode}: unknown error code\n{err_string}'


def _scan_component(
    wss_agent_dir: str,
    component_path: str,
    ws_config: protocol.WhiteSourceApiExtensionWebsocketWSConfig,
) -> subprocess.CompletedProcess:
    # if we have extra config create a new tmp_file and concatenate static and dynamic conf

    with open(paths.static_config_path, 'r') as conf:
        static_config = conf.read()

    with tempfile.NamedTemporaryFile() as tmp_config:
        tmp_config.write(static_config.encode('utf-8'))
        tmp_config.write(f'\nrequesterEmail={ws_config.requesterEmail}'.encode('utf-8'))
        if ws_config.extraWsConfig:
            for key, value in ws_config.extraWsConfig.items():
                tmp_config.write(f'\n{key}={value}'.encode('utf-8'))

        # this seek is needed for the ws agent to read the full config file
        tmp_config.seek(0)

        logging.info('executing agent with extra config...')
        result = run_whitesource_scan(
            wss_agent_dir=wss_agent_dir,
            component_path=component_path,
            config_path=tmp_config.name,
            java_path=paths.java_path,
            ws_config=ws_config,
        )
    return result


def run_whitesource_scan(
    wss_agent_dir: str,
    component_path: str,
    java_path: str,
    ws_config: protocol.WhiteSourceApiExtensionWebsocketWSConfig,
    config_path: str,
) -> subprocess.CompletedProcess:
    wss_agent_path = os.path.join(wss_agent_dir, paths.wss_agent_name)
    args = [
        java_path,
        '-Xms256m',
        '-Xmx512m',
        '-jar', wss_agent_path,
        '-c', config_path,
        '-d', component_path,
        '-apiKey', ws_config.apiKey,
        '-userKey', ws_config.userKey,
        '-wss.url', ws_config.wssUrl,
        '-productToken', ws_config.productToken,
        '-project', ws_config.projectName,
        # if project version is added each new version will create a new project in product
        # this will overload the product with projects this no project version
        # '-projectVersion', ws_config.projectVersion,
    ]

    return subprocess.run(
        args,
        cwd=wss_agent_dir,
        capture_output=True,
    )
