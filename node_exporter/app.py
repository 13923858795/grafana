
import random, datetime, json
from flask import Flask
from flask import make_response
from redis_connect import Redis

app = Flask(__name__)

def key():
    return random.randint(-300, 300)


def resp(txt):
    rst = make_response(txt)
    rst.headers['Content-Type'] = 'text/plain; version=0.0.4; charset=utf-8'
    return rst


@app.route('/metrics')
def hello_world():

    print (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))


    rsp = ''
    for k in Redis.keys():
        k = k.decode('utf-8')
        v = Redis.get(k)
        if v:
            v = v.decode('utf-8')
            rsp = rsp + f'{k} {v}\n'
        else:
            pass




    return resp(rsp)


def run_web(port):
    app.run(debug=True, host='0.0.0.0', port=port)



