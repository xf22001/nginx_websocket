from django.shortcuts import render

# Create your views here.
import time
import logging
import os

logger = logging.getLogger('django.request')

## Create your views here.
from  dwebsocket.decorators import accept_websocket

class ws_api(object):
    def __init__(self, request, *args, **kwargs):
        self.request = request

    def handshake(self, *args, **kwargs):
        pass

    def recv(self, *args, **kwargs):
        pass

    def send(self, msg, *args, **kwargs):
        pass

    def disconnect(self, *args, **kwargs):
        pass

class dwebsocket_api(ws_api):
    def __init__(self, request):
        super(dwebsocket_api, self).__init__(request)
        self.request = request

    def handshake(self, *args, **kwargs):
        pass

    def recv(self, *args, **kwargs):
        msg = self.request.websocket.wait(1)
        if msg:
            msg = bytes.decode(msg)
        return msg

    def send(self, msg, *args, **kwargs):
        logger.debug('send %s' %(msg))
        if msg:
            self.request.websocket.send(msg.encode())

    def disconnect(self, *args, **kwargs):
        self.request.websocket.close()

class uwsgi_api(ws_api):
    def __init__(self, request):
        import uwsgi
        super(uwsgi_api, self).__init__(request)
        self.request = request
        self.uwsgi = uwsgi

    def handshake(self, *args, **kwargs):
        self.uwsgi.websocket_handshake()

    def recv(self, *args, **kwargs):
        msg = self.uwsgi.websocket_recv()
        msg = msg.decode()
        return msg

    def send(self, msg, *args, **kwargs):
        logger.debug('send %s' %(msg))
        self.uwsgi.websocket_send(msg)

    def disconnect(self, *args, **kwargs):
        self.uwsgi.disconnect()

def ws_loop(api):
    api.handshake()
    logger.debug(os.environ)
    api.send("你好，很高兴为你服务")
    try:
        while True:
            msg = api.recv()
            if msg:
                logger.debug('received %s' %(msg))
                datetime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
                api.send('[%s]:%s' %(datetime, msg))
    except:
        api.disconnect()

@accept_websocket
def dws_ws_connect(request):
    if request.is_websocket():
        api = dwebsocket_api(request)
        ws_loop(api)

def uwsgi_ws_connect(request):
    api = uwsgi_api(request)
    ws_loop(api)

ws_connect = dws_ws_connect
