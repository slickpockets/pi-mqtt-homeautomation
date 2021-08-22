#!/usr/bin/python3
# import backend
from app import app
import logging


if __name__ == "__main__":
    logging.basicConfig(filename='/var/log/python/flask.log',level=logging.DEBUG)
    app.run(host='0.0.0.0', port=5000, debug=True)
    logging.info("must turn off autoreloader in production")
