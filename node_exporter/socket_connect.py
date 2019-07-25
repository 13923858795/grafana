import socket, time
import subprocess
from redis_connect import Redis


def run_socket(port):
    server = socket.socket()
    server.bind(('', port))
    server.listen(5)
    print('socket 等待连接.....')
    conn, addr = server.accept()
    print('socket 已连接......')
    while True:
        data = conn.recv(10240)
        data = data.decode('utf-8').split(' ')
        id_ = data[1]
        v_list = [i if '\n' not in i else i[:-2] for i in data[3:]]
        _k = 0
        for _v in v_list:
            k = f'{id_}_{_k}'
            Redis.set(k, str(time.time()), 10)
            _k += 1
        cmd = subprocess.Popen(data,
                               shell=True,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
        stdout = cmd.stdout.read()
        stderr = cmd.stderr.read()


