# example of wait for one message

import threading
from socketIO_client import SocketIO
class WaitUntillRecv:
    def __init__(self):
        print('init')
        self.received = False
        self.socketio = SocketIO('http://ss.chinacloudsites.cn/', verify=False)
        self.socketio.on('player0', self.on_event) # once received
        self.receive_events_thread = threading.Thread(target=self._receive_events_thread) # new thread for listening forever
        self.receive_events_thread.daemon = True
        self.receive_events_thread.start()
    def on_event(self, map):
        self.received = True
        self.map = map
        self.socketio.disconnect() # stop waiting
        print('received!')
    def _receive_events_thread(self):
        self.socketio.wait()
        print('ended!')


# parse http
waitClas = WaitUntillRecv()
while not waitClas.received:
    pass

print(waitClas.map)