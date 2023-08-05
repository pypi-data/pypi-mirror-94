import datetime
import logging
import os
import shutil
import tempfile
import threading

import requests

import paths


# noqa disables flake8 linting for error E501 = line too long
ws_agent_url = 'https://github.com/whitesource/unified-agent-distribution/releases/latest/download/wss-unified-agent.jar'  # noqa: E501


def update_or_download_agent():
    log = logging.getLogger(__name__)
    if os.path.isfile(path=paths.wss_agent_path):
        modification_date = datetime.datetime.fromtimestamp(os.stat(paths.wss_agent_path).st_mtime)
        if modification_date < datetime.datetime.now() - datetime.timedelta(hours=24):
            log.info('ws agent is older than 24 hours. Agent will be updated...')

            # updating ws agent in new thread
            threading.Thread(
                target=pull_latest_wss_agent,
                args=[paths.wss_agent_path],
                daemon=True,
            ).start()
        else:
            log.info(
                f'wss agent is up to date and present on file system {paths.wss_agent_path=}.'
                ' Using this one...',
            )
    else:
        try:
            # download wss agent and block thread
            log.info('wss agent not found on file system. Pulling it now...')
            pull_latest_wss_agent(paths.wss_agent_path)
        except requests.exceptions.HTTPError as e:
            log.error(f'could not download ws agent {e.request=}. Keeping the current one...')


def get_wss_agent_hardlink(tmp_dir: str) -> str:
    update_or_download_agent()

    # at this point the wss_agent is present on the machine
    # creating a hard link so the current agent will not be garbage collected
    wss_agent_hardlink_path = os.path.join(tmp_dir, paths.wss_agent_name)
    os.link(src=paths.wss_agent_path, dst=wss_agent_hardlink_path)

    return wss_agent_hardlink_path


def pull_latest_wss_agent(wss_agent_path: str):
    log = logging.getLogger(__name__)
    # write res stream in tmp file because of multi threading
    tmp_file = None
    try:
        tmp_file = tempfile.NamedTemporaryFile(delete=False)
        with requests.get(url=ws_agent_url, stream=True) as res:

            res.raise_for_status()

            for chunk in res.iter_content(chunk_size=8192):
                tmp_file.write(chunk)

            log.info('agent downloaded. Moving it to tmp dir...')

            shutil.move(src=tmp_file.name, dst=wss_agent_path)
        tmp_file.close()

        log.info('ws agent pulled successfully.')

    except Exception:
        log.error('an error occured while pulling ws agent')
        os.unlink(tmp_file.name)
        raise RuntimeError('error pulling wss agent')


def sizeof_fmt(num, suffix='B'):
    for unit in ['','Ki','Mi','Gi','Ti','Pi','Ei','Zi']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)
