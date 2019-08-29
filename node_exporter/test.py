import socketserver
import json, time
import os
import sys
from time import sleep
from logging import handlers
from datetime import datetime, timedelta
# import paho.mqtt.publish as publish
from log import logger
from redis_connect import Redis
import pymysql

# SQL_HOST = 'mysql'
# SQL_PORT = 3306
# SQL_USER = 'root'
# SQL_PASSWORD = '123456'
# SQL_DB_NAME = 'grafana'

SQL_HOST = '1.1.6.116'
SQL_PORT = 3306
SQL_USER = 'root'
SQL_PASSWORD = '123456'
SQL_DB_NAME = 'grafana'



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
                print("传入数据：", self.data)
                data = self.data.decode('utf-8').split(' ')
                logger.info(data)

                if data[0] == 'DATA':
                    id_ = data[1]
                    data = data[3:]
                else:
                    id_ = data[0]
                    data = data[2:]
                v_list = [i if '\n' not in i else i[:-2] for i in data]

                _k = 0
                for _v in v_list:
                    k = f'key_{id_}_{_k}'
                    logger.info(f'数据为{k} {_v}')

                    # Redis.set(k, str(_v), 10)

                    sql = f'''
                         INSERT INTO alerting_log (k,v,created_at) VALUES("{k}", '{_v}', NOW())
                         '''
                    _k += 1

        except Exception:
            logger.exception('from ' + str(self.client_address))
            raise Exception('threading handler error')

    def finish(self):
        super(ThreadedTCPRequestHandler, self).finish()
        logger.info('finished a handler for ' + str(self.client_address))

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    allow_reuse_address = True


HOST = '0.0.0.0'
socket_port = 5858

if __name__ == '__main__':

    try:
        server = ThreadedTCPServer((HOST, socket_port), ThreadedTCPRequestHandler)
        logger.info('starting socket server on {}:{}.'.format(HOST, str(socket_port)))
        server.serve_forever()
    except Exception as e:
        logger.exception('stopped socket server on {}:{}'.format(HOST, str(socket_port)))
        logger.exception(e)

        time.sleep(3)


# a =  'DATA 0 57418 0 0\r\nDATA 0 57468 0 0\r\nDATA 0 57518 0 0\r\nDATA 0 57568 0 0\r\nDATA 0 57618 0 2\r\nDATA 0 57668 0 4\r\nDATA 0 57718 0 -6\r\nDATA 0 57768 0 0\r\nDATA 0 57818 0 2\r\nDATA 0 57868 0 0\r\nDATA 0 57918 0 -2\r\nDATA 0 57968 0 2\r\nDATA 0 58018 0 4\r\nDATA 0 58068 0 2\r\nDATA 0 58118 0 0\r\nDATA 0 58168 0 2\r\nDATA 0 58218 0 2\r\nDATA 0 58268 0 2\r\nDATA 0 58318 0 0\r\nDATA 0 58368 0 2\r\n'
# datas =a.split('\r\n')
#
# for _d in a.split('\r\n'):
#     print(_d)
#
#
# print(len(datas))