# -*- coding: utf-8 -*-
# @Author: robertking, philipxyc
# @Date:   2018-07-13 17:34:38
# @Last Modified by:   robertking
# @Last Modified time: 2019-03-12 16:34:49


import threading
from socketIO_client import SocketIO
import logging
import os


SOCKET_SERVER_URL = os.environ['SOCKET_SERVER_URL']

logger = logging.getLogger(__name__)


class MessageHandle:
    def __init__(self):
        self._lock = threading.Lock()
        self._listeners = []
        self._msg = [None]

    def listen(self):
        evt = threading.Event()

        self._lock.acquire()
        try:
            self._listeners.append(evt)
        except Exception as e:
            logger.error('Message Handle received error when listening: {}'.format(e))
            raise
        finally:
            self._lock.release()

        return self._msg, evt

    def update(self, msg):
        self._lock.acquire()
        try:
            self._msg[0] = msg
            self._msg = [None]
            listeners = self._listeners
            self._listeners = []
        except Exception as e:
            logger.error('Message Handle received error when updating: {}'.format(e))
            raise
        finally:
            self._lock.release()

        for evt in listeners:
            evt.set()


class NotificationCenter:

    def __init__(self, socket_server_url, topic):
        self._lock = threading.Lock()
        self._msgs = {}
        self._socketio = SocketIO(SOCKET_SERVER_URL, verify=False)
        self._socketio.on(topic, self.update)  # once received
        self._receive_events_thread = threading.Thread(target=self._receive_events_thread)
        # new thread for listening forever
        self._receive_events_thread.daemon = True
        self._receive_events_thread.start()

    def _receive_events_thread(self):
        self._socketio.wait()

    def _get_msgobj(self, gid, course=None):
        self._lock.acquire()
        try:
            if gid in self._msgs:
                msgobj = self._msgs[gid]
            else:
                msgobj = MessageHandle()
                self._msgs[gid] = msgobj
        except Exception as e:
            logger.error('Notification Center received error{}: {}'
                         .format(e, ' when ' + course if course else ''))
            raise
        finally:
            self._lock.release()

        return msgobj

    def listen(self, gid):
        msgobj = self._get_msgobj(gid, 'listening')
        return msgobj.listen()

    def update(self, raw_msg):
        msgobj = self._get_msgobj(raw_msg['gid'], 'updating')
        msgobj.update(raw_msg)
