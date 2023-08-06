"""
Threaded HTTP Server.
"""

import datetime, time, threading
from ..http_support.request_parsing import Request
from ..http_support.responses import Response
from ..http_support.formats import reply_format
from ..http_support.parse_time import gettime as _gettime
from ..http_support.environ import get_environ
from .version import version
import uuid
from io import StringIO
import traceback

__all__ = ("ThreadedHTTPServer",)

class ThreadedHTTPServer:
    """
    Threaded HTTP Server.
    Usage:
    >>> from serverhttp import *
    >>> app = App(__name__)
    >>> @coroutine
    @app.route("/", ["GET"])
    def test(environ):
        yield Response("200 OK")

    >>> s = ThreadedHTTPServer(app=app)
    >>> s.serve_forever("127.0.0.1", 60000)
    """
    use_ipv6 = False
    def __init__(self, name='', app=None, max_threads=2000, debug=False, 
    		sslcontext=None, 
    		):
        self.server = version
        self.functions = {}
        self.threads = []
        self.max_threads=max_threads
        self.reply_format = reply_format
        self._debug_=debug
        if app:
            self.app = app
            self.app.server = self.server
            self.name = self.app.name
            self.app.prepare_for_deploy(self)
        else:
            self.name = name
        self.sslcontext = sslcontext
        self._address_family = socket.AF_INET
        if self.use_ipv6:
        	self._address_family = socket.AF_INET6
        	
    def _serve_one_client(self, conn, addr):
        sid = uuid.uuid4().hex
        import time
        reply_format = self.reply_format
        timeout = 0.1
        if self.sslcontext:
            conn = self.sslcontext.wrap_socket(conn, server_side=True)
        while True:
            txt = conn.recv(65535).decode()
            if not txt:
                time.sleep(timeout)
                if timeout > 10:
                    conn.close()
                    return
                timeout += 0.1
                continue
            req = Request(txt)
            reply_obj = self._handle_request(req)
            cookie='session-id:{}'.format(sid)
            if len(reply_obj.cookies)==0:
                reply_obj.cookies = cookie
            else:
                reply_obj.cookies = reply_obj.cookies + ';' + cookie
            reply = str(reply_obj).encode()
            conn.sendall(reply)
            print(addr[0], '-', '"'+req.text+'"', '-', reply_obj.status)
    def _404(self, env):
        return Response('404 Not Found', 'text/html', '<h1>404 not found')
    def _405(self, env):
        return Response('405 Method Not Allowed')
    def _handle_request(self, request):
        splitted = request.text.split()
        env = get_environ(request)
        try:
            path = splitted[1].split('?')[0]
        except:
            path = splitted[1]
        method = splitted[0]
        try:
            res = self.functions[path]
        except KeyError:
            res = self._404
        try:
            res = res[method]
        except:
            res = self._405
        try:
            res = res(env)
        except BaseException as e:
            if self._debug_:
                i = StringIO()
                traceback.print_exc(file=i)
                traceback.print_exc()
                i.seek(0)
                d = i.read()
                res = Response('500 Server Error', 'text/plain', '500 server error:\r\n'+d)
            else:
                res = Response('500 Server Error', 'text/plain', '500 server error')
        return res
    def serve_forever(self, host, port):
        threads_append = self.threads.append
        import socket
        s = socket.socket(self._address_family)
        s.bind((host, port))
        if self.name != '':
            print('* Serving App {}'.format(self.name))
        print('* Serving On http://{host}:{port}'.format(host=host, port=port))
        print('* Press <CTRL-C> To Quit')
        self_serve_one_client = self._serve_one_client
        s.listen()
        try:
            while True:
                if len(self.threads)>self.max_threads:
                    continue
                tup = s.accept()
                t = threading.Thread(target=self_serve_one_client, args=tup)
                t.daemon = True
                threads_append(t)
                t.start()
        except:
            s.close()
            return

