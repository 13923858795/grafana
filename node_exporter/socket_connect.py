import socketserver, config, time
import json
import os
import sys
from time import sleep
from logging import handlers
from datetime import datetime, timedelta
# import paho.mqtt.publish as publish
from log import logger
from redis_connect import Redis
import pymysql

SQL_HOST = config.SQL_HOST
SQL_PORT = config.SQL_PORT
SQL_USER = config.SQL_USER
SQL_PASSWORD = config.SQL_PASSWORD
SQL_DB_NAME = config.SQL_DB_NAME


class PyMysqlDB:
    def __init__(self):
        # 创建连接 项目 mysql
        self.conn = pymysql.connect(host=SQL_HOST, port=SQL_PORT, user=SQL_USER, passwd=SQL_PASSWORD, db=SQL_DB_NAME)
        # 创建游标
        self.cursor = self.conn.cursor()


SqlConnect = PyMysqlDB()
conn = SqlConnect.conn
cursor = SqlConnect.cursor


class DB:
    """ Mysql 直连数据库 """

    @classmethod
    def sql_first(cls, sql):
        cursor.execute(sql)
        model = cursor.fetchone()
        return model

    @classmethod
    def sql_all(cls, sql):
        cursor.execute(sql)
        model = cursor.fetchall()
        return model

    @classmethod
    def sql(cls, sql):
        cursor.execute(sql)
        conn.commit()
        return cursor.lastrowid

    @classmethod
    def sql_insert(cls, sql):
        cursor.execute(sql)
        conn.commit()
        return True


'''  创建数据表
CREATE TABLE `alerting_log`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `k` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `v` float NULL DEFAULT NULL,
  `created_at` datetime(0) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 104 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

'''

# sql = '''
#      INSERT INTO test (k,v,created_at) VALUES("1", 2, NOW())
#
#         '''
# a = DB.sql_insert(sql)
#
# print(a)





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
            while True:
                self.data = self.request.recv(1024)
                if not self.data:
                    break

                data = self.data.decode('utf-8')
                try:
                    self.func_data(data)
                except BaseException as e:
                    logger.info(e)

    def func_data(self, data):
        for _data in data.split('\r\n')[:1]:
            _d = _data.split(" ")
            if _d[0] == 'DATA':
                id_ = _d[1]
                v_list = _d[3:]
            else:
                id_ = _d[0]
                v_list = _d[2:]
            _k = 0
            for _v in v_list:
                k = f'key_{id_}_{_k}'
                logger.info(f'数据为{k} {_v}')
                if id_ != '0':
                    print(self.data)
                Redis.set(k, str(_v), 10)

                sql = f'''INSERT INTO alerting_log (k,v,created_at) VALUES("{k}", '{_v}', NOW())
                                  '''
                try:
                    DB.sql_insert(sql)
                except:
                    print(sql)
                _k += 1







    def finish(self):
        super(ThreadedTCPRequestHandler, self).finish()
        logger.info('finished a handler for ' + str(self.client_address))


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    allow_reuse_address = True




