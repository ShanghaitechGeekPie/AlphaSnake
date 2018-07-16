import threading
import copy
from socketIO_client import SocketIO


SOCKET_SERVER_URL = 'http://as.chinacloudsites.cn/'


class WaitUntilRecv:
    def __init__(self, topic, check):
        # print('init')
        self.msg = []
        self.check = check
        self.socketio = SocketIO(SOCKET_SERVER_URL, verify=False)
        self.event = threading.Event()
        self.socketio.on(topic, self.on_event)  # once received
        self.receive_events_thread = threading.Thread(target=self._receive_events_thread)
        # new thread for listening forever
        self.receive_events_thread.daemon = True
        self.receive_events_thread.start()

    def on_event(self, msg):
        msg = copy.deepcopy(msg)
        print(type(msg))
        if self.check(msg):
            self.msg = msg
            self.socketio.disconnect()  # stop waiting
            # print('received!')
            self.event.set()

    def wait(self):
        self.event.wait()

    def _receive_events_thread(self):
        self.socketio.wait()
        # print('ended!')


# waitClas = WaitUntillRecv()
# waitClas.wait()

# print(waitClas.msg)
