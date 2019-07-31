import selectors
import socket
from wgsi_server.http_parsed import BaseRequest
import time
from wgsi_server.tools import format_date_time

class MhttpServer(object):
    def __init__(self, host, port,application):
        self.selector = selectors.DefaultSelector()
        self.sock = socket.socket()
        self.address = (host, port)
        self.app=application
        self.request_queue_size = 5
        self.open_socket()

    def accept(self, sock):
        sel = self.selector
        conn, addr = sock.accept()  # Should be ready
        conn.setblocking(False)
        sel.register(conn, selectors.EVENT_READ, self.read)

    def start_response(self, status, headers_list):
        r = 'HTTP/1.1 {}\r\n'.format(status)
        for h in headers_list:
            k = h[0]
            v = h[1]
            r += '{}: {}\r\n'.format(k, v)

        r += "Date: %s\r\n" % format_date_time(time.time())
        r += "Server: neuedu-wsgi\r\n"
        r += '\r\n'

        self.response = r.encode()

    def write(self, sock):
        print('write')
        sel = self.selector

        body = self.app(self.req.getenv(), self.start_response)

        for data in body:
            self.response += data

        resp = self.response
        sock.send(resp)

        sel.unregister(sock)
        sock.close()

    def read(self, conn):
        sel = self.selector

        data = conn.recv(1000)  # Should be ready
        if data:
            conn.setblocking(False)
            sel.unregister(conn)

            # print('echoing', repr(data))

            s = data.decode('utf-8')
            self.req = BaseRequest(s)

            sel.register(conn, selectors.EVENT_WRITE, self.write)
        else:
            print('closing', conn)
            sel.unregister(conn)
            conn.close()

    def server_close(self):
        self.sock.close()
        self.selector.close()

    def server_bind(self):
        sock = self.sock

        sock.bind(self.address)
        self.server_address = sock.getsockname()

    def server_listen(self):

        self.sock.listen(self.request_queue_size)

    def open_socket(self):
        sock = self.sock

        self.server_bind()
        self.server_listen()
        sock.setblocking(False)

    def serve_forever(self):
        sock = self.sock
        sel = self.selector

        sel.register(sock, selectors.EVENT_READ, self.accept)
        try:
            while True:
                events = sel.select()
                for key, mask in events:
                    callback = key.data
                    callback(key.fileobj)
        finally:
            print('close')
            self.server_close()