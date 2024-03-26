import logging
from pygelf import GelfUdpHandler, GelfTcpHandler
from flask import request
from socket import error as SocketError
from config import GRAYLOG_HOST, GRAYLOG_PORT
from flask_jwt_extended import jwt_required, get_jwt_identity

class GraylogLogger:
    def __init__(self):
        self.logger = self._setup_logger()

    def _setup_logger(self):
        logging.basicConfig(level=logging.INFO)
        try:
            logger = logging.getLogger()
            logger.addHandler(GelfUdpHandler(host=GRAYLOG_HOST, port=GRAYLOG_PORT))
            logger.info('Init logger in python test')
            self.connected = True
        except SocketError as e:
            print (e)
            print(f"Failed to connect to Graylog server: {e}")
        return logger

    def log(self, message, level=logging.INFO):
            extra_data = {
            'user_agent': request.headers.get('User-Agent'),
            'remote_address': request.remote_addr,
            'method': request.method,
            'url': request.url,
            'user': str(get_jwt_identity()) if hasattr(request, 'jwt_identity') else 'anonymous'
            }
            self.logger.log(level, message, extra=extra_data)
    def close(self):
        for handler in self.logger.handlers:
            handler.close()
