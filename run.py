#!/usr/bin/python3
import os


def run(cmds):
    for cmd in cmds:
        os.system(cmd)

print("请使用 root 用户执行")

cmd = [
    'groupadd -g 472 grafana',
    'useradd -u 472 -g grafana grafana',
    'chown  -R grafana.grafana ./data/grafana',

    
    'groupadd -g 65534 nobody',# 还有问题  需要调整
    'useradd -u 65534 -g nobody',
    'chown  -R nobody ./data/prometheus',
    
    'docker stack deploy --compose-file=docker-compose.yml quatek',
    ]


run(cmd)