#!/usr/bin/python3
# import backend
from app import create_app
import logging


if __name__ == "__main__":
    logging.basicConfig(filename='/var/log/python/flask.log',level=logging.DEBUG)
    app = create_app()
    app.run(app, '0.0.0.0', 5000, use_reloader=True, debug=True)
    logging.info("must turn off autoreloader in production")
