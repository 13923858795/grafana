import socket, time
import random
from log import logger
from redis_connect import Redis



def run(HOST, PORT):
    # 创建实例
    sk = socket.socket()
    # 定义IP和端口
    ip_port = (HOST, PORT)
    # 绑定监听
    sk.bind(ip_port)
    # 设置最大链接数
    sk.listen(5)
    # 轮询，不断的接收数据
    while True:
        # 提示信息
        print("正在等待接收数据。。。。。")
        # 接收数据
        conn, address = sk.accept()
        # 定义信息
        msg = "链接成功!"
        # 返回信息 py3.x以上，网络数据的发送接收都是byte类型
        # str则需要编码
        conn.send(msg.encode())
        # 不断接收客户端发送的信息
        while True:
            # 每次读取缓冲区1024字节的数据
            data = conn.recv(1024)
            # 打印数据,处理数据逻辑
            data = data.decode('utf-8').split(' ')
            id_ = data[1]
            v_list = [i if '\n' not in i else i[:-2] for i in data[3:]]
            _k = 0
            for _v in v_list:
                k = f'key_{id_}_{_k}'
                logger.info(f'数据为{k} {_v}')
                Redis.set(k, _v, 10)

                _k += 1

        # 主动关闭链接
        conn.close()



HOST = '0.0.0.0'
PORT = 5858


if __name__ == '__main__':
    while True:
        try:
            run(HOST, PORT)
            logger.info('starting socket server on {}:{}.'.format(HOST, str(PORT)))

        except Exception as e:
            logger.exception('stopped socket server on {}:{}'.format(HOST, str(PORT)))
            logger.exception(e)

        time.sleep(3)
