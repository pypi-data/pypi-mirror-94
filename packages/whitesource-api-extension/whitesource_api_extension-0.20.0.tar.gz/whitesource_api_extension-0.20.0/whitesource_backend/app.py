import logging
import threading

import falcon.asgi

import component
import util


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
