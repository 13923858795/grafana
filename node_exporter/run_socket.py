import time, config
from socket_connect import ThreadedTCPServer, ThreadedTCPRequestHandler
from log import logger

HOST = '0.0.0.0'
socket_port = 5858


if __name__ == '__main__':
    while True:
        try:
            server = ThreadedTCPServer((HOST, socket_port), ThreadedTCPRequestHandler)
            logger.info('starting socket server on {}:{}.'.format(HOST, str(socket_port)))
            server.serve_forever()
        except Exception as e:
            logger.exception('stopped socket server on {}:{}'.format(HOST, str(socket_port)))
            logger.exception(e)

        time.sleep(3)
