import time
from socket_connect import run_socket
from app import run_web
from multiprocessing import Process
from log import logger

HOST = '0.0.0.0'
api_port = 9100


if __name__ == '__main__':
    while True:
        try:
            run_web(api_port)
            logger.info('starting api server on {}:{}.'.format(HOST, str(api_port)))

        except Exception as e:
            logger.exception('stopped api server on {}:{}'.format(HOST, str(api_port)))
            logger.exception(e)

        time.sleep(3)





