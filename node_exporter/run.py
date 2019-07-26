import time
from socket_connect import run_socket
from app import run_web
from multiprocessing import Process
from log import logger

HOST = '0.0.0.0'
socket_port = 5858
api_port = 9100

run_socket = Process(target=run_socket, args=(socket_port,))
run_api = Process(target=run_web, args=(api_port,))

if __name__ == '__main__':
    while True:
        try:
            run_socket.start()
            logger.info('starting socket server on {}:{}.'.format(HOST, str(socket_port)))

            run_api.start()
            logger.info('starting api server on {}:{}.'.format(HOST, str(api_port)))

        except Exception as e:
            logger.exception('stopped server on {}:{}'.format(HOST, str(socket_port)))
            logger.exception(e)

        try:
            run_api.start()
            logger.info('starting api server on {}:{}.'.format(HOST, str(api_port)))
        except Exception as e:
            logger.exception('stopped server on {}:{}'.format(HOST, str(api_port)))
            logger.exception(e)

        time.sleep(3)





