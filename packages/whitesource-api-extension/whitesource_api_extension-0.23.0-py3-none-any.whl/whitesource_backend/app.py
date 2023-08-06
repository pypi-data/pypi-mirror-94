import argparse
import logging
import threading

import falcon.asgi
import uvicorn

import component
import util


util.configure_default_logging(force=True)


LOGGING_CONFIG = {
        "version": 1,
        "disable_existing_loggers": False,
        "loggers": {
            "uvicorn": {"level": logging.INFO},
            "uvicorn.error": {"level": logging.INFO},
            "uvicorn.access": {"level": logging.INFO},
        },
    }


def create_app():
    logger = logging.getLogger(__name__)
    logger.info('initializing falcon')
    app = falcon.asgi.App()
    app.add_route('/component', component.Component())

    threading.Thread(
        target=util.update_or_download_agent,
        daemon=True,
    ).start()

    return app


app = create_app()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', action='store', dest='port', type=int)
    args = parser.parse_args()
    uvicorn.run(
        'app:app',
        host="0.0.0.0",
        port=args.port,
        log_level='info',
        log_config=LOGGING_CONFIG,
        workers=4,
    )
