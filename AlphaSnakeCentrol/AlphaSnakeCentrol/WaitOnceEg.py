# example of wait for one message

import threading
import copy
from socketIO_client import SocketIO
class WaitUntillRecv:
    def __init__(self):
        print('init')
        self.msg = []
        self.received = False
        self.socketio = SocketIO('https://as.chinacloudsites.cn/', verify=False)
        self.socketio.on('judged', self.on_event) # once received
        self.receive_events_thread = threading.Thread(target=self._receive_events_thread) # new thread for listening forever
        self.receive_events_thread.daemon = True
        self.receive_events_thread.start()
    def on_event(self, msg):
        print(type(msg))
        self.msg = copy.deepcopy(msg)
        self.socketio.disconnect() # stop waiting
        print('received!')
        self.received = True
    def _receive_events_thread(self):
        self.socketio.wait()
        print('ended!')


# parse http
waitClas = WaitUntillRecv()
while not waitClas.received:
    pass

print(waitClas.msg)