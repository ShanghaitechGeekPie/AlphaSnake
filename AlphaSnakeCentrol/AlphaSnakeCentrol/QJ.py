# -*- coding: utf-8 -*-
# @Author: robertking
# @Date:   2018-07-15 22:59:23
# @Last Modified by:   robertking
# @Last Modified time: 2019-03-14 01:55:21


from field import Field
import time
import requests
from datetime import datetime
from socketIO_client import SocketIO
# from socket_io_emitter import Emitter
import os


SOCKET_SERVER_URL = os.environ['SOCKET_SERVER_URL']
SERVER_URL_BASE = os.environ['SERVER_URL_BASE']

ROUND_TIME_SLICE = float(os.environ['ROUND_TIME_SLICE'])


def getready():
    while True:
        res = requests.get(SERVER_URL_BASE + '/ready').json()
        if res:
            return res
        time.sleep(15)


def getmoves(gid):
    return requests.post(SERVER_URL_BASE + '/move', {'gid': gid}).json()


socketio = SocketIO(SOCKET_SERVER_URL, verify=False)
# socketio = Emitter({'host': '127.0.0.1', 'port': 3000})


def emit(topic, data):
    socketio.emit(topic, data)
    # socketio.Emit(topic, data)


def updategame(gid, checkpoint, status=None):
    data = {'gid': gid, 'time': checkpoint}
    if status:
        data['status'] = status
    return requests.post(SERVER_URL_BASE + '/update', data)


PENDING = 0
READY = 1
RUNNING = 2
END = 3


if __name__ == '__main__':
    while True:
        game = getready()
        gid = game['id']
        players = sorted(game['players'])
        print('Game #{} ready, players: {}.'.format(gid, players))

        num_players = len(players)
        player_index = {pid: idx for idx, pid in enumerate(players)}

        field = Field(num_players)

        checkpoint = datetime.utcnow()
        emit('init', {'gid': gid, 'map': field.map.reshape(-1).tolist()})

        print('Game update result:', updategame(gid, checkpoint, RUNNING).status_code)
        print('Game #{} starts.'.format(gid))

        while True:
            time.sleep(ROUND_TIME_SLICE)

            moves = [-1] * num_players
            for pid, direction in getmoves(gid):
                moves[player_index[pid]] = direction
            print('Game #{} players move: {}.'.format(gid, moves))

            new_map, raw_status = field.go(moves)

            status = [2 if s else 0 for s in raw_status] if sum(raw_status) == 1 else raw_status

            checkpoint = datetime.utcnow()
            emit('judged', {
                'gid': gid, 'map': new_map.tolist(),
                'status': list(zip(players, status))
            })

            if sum(raw_status) <= 1:
                print('Game update result:', updategame(gid, checkpoint, END).status_code)
                print('Game #{} ended, result: {}.'.format(gid, status))
                break
            else:
                print('Game update result:', updategame(gid, checkpoint).status_code)
                print('Game #{} updated, status: {}.'.format(gid, status))

        time.sleep(20)

socketio.disconnect()
