import random

def v():
    return random.randint(0, 100)






import socket, time
import sys

# 创建 socket 对象
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 获取本地主机名
host = '10.1.6.108'
# 设置端口号
port = 5858
s.connect((host, port))
while True:
    # 连接服务，指定主机和端口

    data = f'0 123456789 {v()} {v()}'
    data = bytes(data, encoding='utf-8')

    # 接收小于 1024 字节的数据
    msg = s.send(data)
    # s.close()
    time.sleep(1)
