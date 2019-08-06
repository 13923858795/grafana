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
import pymysql

SQL_HOST = 'mysql'
SQL_PORT = 3306
SQL_USER = 'root'
SQL_PASSWORD = '123456'
SQL_DB_NAME = 'grafana'


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

                    # try:
                    #     v = int(_v)
                    #     _v = v*5#  甲方要求  k*5   且 k*5 > 200 or k*5 < -200
                    #
                    #     if _v > 200 or _v < -200:
                    #         _v_f = str(_v)
                    #     else:
                    #         _v_f = ''
                    #
                    # except:
                    #     _v_f = ''

                    Redis.set(k, str(_v), 10)
                    # Redis.set(k+'_f', str(_v_f), 10)

                    sql = f'''   
                         INSERT INTO alerting_log (k,v,created_at) VALUES("{k}", {_v}, NOW())
                         '''
                    DB.sql_insert(sql)

                    _k += 1

        except Exception:
            logger.exception('from ' + str(self.client_address))
            raise Exception('threading handler error')

    def finish(self):
        super(ThreadedTCPRequestHandler, self).finish()
        logger.info('finished a handler for ' + str(self.client_address))


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    allow_reuse_address = True




