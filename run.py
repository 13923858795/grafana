#!/usr/bin/python3
import os













def run(*cmds):
    for cmd in cmds:
        os.system(cmd)

print("请使用 root 用户执行")
c1 =  'groupadd -g 472 grafana'
c2 =  'useradd -u 472 -g grafana grafana'
c3 = 'chown  -R grafana.grafana ./grafana'
c4 = 'docker stack deploy --compose-file=docker-compose.yml quatek'


cmd = [
    'groupadd -g 472 grafana',
    'useradd -u 472 -g grafana grafana',
    'chown  -R grafana.grafana ./grafana',

    
    'groupadd -g 65534 nobody',# 还有问题  需要调整
    'useradd -u 65534 -g nobody',
    'chown  -R nobody ./prometheus/data/prometheus',
    
    'docker stack deploy --compose-file=docker-compose.yml quatek',
    ]


run(c1, c2, c3, c4)