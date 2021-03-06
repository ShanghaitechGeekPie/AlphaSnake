import requests


SERVER_ROOT = 'https://alphasnake.geekpie.club'
# SERVER_ROOT = 'http://127.0.0.1:8000'

DEBUG = True

# define of step choice
class STEP:
    UNDEFINED = -1    # only for player died
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3


class STATUS:
    DIED = 0
    ALIVE = 1
    WIN = 2


# Submit one step and get result of this step.
#     args: step - using GoUp | GoRight | GoDown | GoLeft.


class Game:
    def __init__(self):
        pass

    def register(self, name):
        res = requests.post(SERVER_ROOT + '/init', {'name': name})
        if DEBUG:
            print(res.content)
        res = res.json()
        #  res = requests.post(SERVER_ROOT + '/init', {'name': name}).json()
        self._pid = res['pid']
        self._cookie = res['cookie']
        return res['map'], res['local_id']

    def submit_step(self, move):
        res = requests.post(SERVER_ROOT + '/go',
                            {'pid': self._pid, 'cookie': self._cookie, 'move': move}).json()
        return res['map'], res['status']
