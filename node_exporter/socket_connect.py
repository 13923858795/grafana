import socketserver
import json
import os
import sys
from time import sleep
from logging import handlers
from datetime import datetime, timedelta
# import paho.mqtt.publish as publish
from log import logger
from redis_connect import Redis


class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):
    def setup(self):
        logger.info('starting a handler for ' + str(self.client_address))
        self.request.settimeout(3)
        self.data = None
        self.data_list = []  # [ID, DT, D1, ... Dn]
        self.list_of_data_list = []
        self.processing_list_of_data_list = []
        self.processed_list_of_data_list = []

    def filter(self, list_of_data):
        '''
        :param list_of_data:
        :return: abs max number of list_of_data, but should in (-1000, 1000)
        '''
        results = sorted(list_of_data, key=lambda x: abs(x), reverse=True)
        for data in results:
            if -10000 < data < 10000:
                return data

        return 0

    def handle(self):
        try:
            while True:
                self.data = self.request.recv(1024)

                if not self.data:
                    break

                data = self.data.decode('utf-8').split(' ')
                print(data)
                id_ = data[1]
                v_list = [i if '\n' not in i else i[:-2] for i in data[3:]]
                _k = 0
                for _v in v_list:
                    k = f'key_{id_}_{_k}'
                    logger.info(f'数据为{k} {_v}')
                    Redis.set(k, _v, 10)

                    _k += 1

        except Exception:
            logger.exception('from ' + str(self.client_address))
            raise Exception('threading handler error')

    def finish(self):
        super(ThreadedTCPRequestHandler, self).finish()
        logger.info('finished a handler for ' + str(self.client_address))


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    allow_reuse_address = True




