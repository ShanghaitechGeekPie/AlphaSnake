# -*- coding: utf-8 -*-
# @Author: robertking
# @Date:   2018-07-15 22:59:23
# @Last Modified by:   robertking
# @Last Modified time: 2018-07-16 02:23:09


from field import Field
import time
import requests
from SocketIO_client import SocketIO
from WaitOnceEg import SOCKET_SERVER_URL


SERVER_URL_BASE = 'http://127.0.0.1:9876'


def getready():
    while True:
        res = requests.get(SERVER_URL_BASE + '/ready').json()
        if res:
            return res
        time.sleep(5)


def getmoves(gid):
    return requests.post(SERVER_URL_BASE + '/move', {'gid': gid}).json()


def emit(topic, data):
    with SocketIO(SOCKET_SERVER_URL, verify=False) as socketio:
        socketio.emit(topic, data)
        socketio.wait(seconds=1)


def updategame(gid, status=None):
    data = {'gid': gid}
    if status:
        data['status'] = status
    return requests.post(SERVER_URL_BASE + '/update', data).json()


PENDING = 0
READY = 1
RUNNING = 2
END = 3


if __name__ == '__main__':
    while True:
        game = getready()
        gid = game['id']
        players = sorted(game['players'])

        field = Field(len(players))

        emit('init', {'gid': gid, 'map': field.getmap()})
        updategame(gid, RUNNING)

        while True:
            time.sleep(5)
            moves = sorted(getmoves(gid))

            new_map, status = field.go(list(map(lambda x: x[1], moves)))

            emit('judged', {
                'map': new_map,
                'status': list(zip(map(lambda x: x[0], moves), status))
            })

            if len([s for s in status if s == 1]) <= 1:
                updategame(gid, END)
                break
            else:
                updategame(gid)

        time.sleep(10)
