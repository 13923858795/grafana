import time
from socket_connect import run_socket
from log import logger

HOST = '0.0.0.0'
socket_port = 5858


if __name__ == '__main__':
    while True:
        try:
            run_socket(socket_port)
            logger.info('starting socket server on {}:{}.'.format(HOST, str(socket_port)))

        except Exception as e:
            logger.exception('stopped socket server on {}:{}'.format(HOST, str(socket_port)))
            logger.exception(e)

        time.sleep(3)
