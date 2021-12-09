# -*- coding: utf-8 -*-
"""
---------------------------------------------------------
    File Name :         server_reader.py                             
    Description :                                       
    Author :            Karl                             
    Date :              2021-12-08                          
---------------------------------------------------------
    Change Activity :   2021-12-08
    
--------------------------------------------------------- 
"""
# https://zhuanlan.zhihu.com/p/146650395

"""
           input                      send               recv
stdin -------------> +------------+ -------------------------> +------------+
                     | tcp client |                            | tcp server |
stdout <------------ +------------+ <------------------------- +------------+
           output                     recv               send
"""
# Version 3:
# Fork one progress by one client connection
# Need more resource to support for concurrency


import signal
import socket
import queue
# import ssl
import sys
import os


class TcpServer:
    def __init__(self, server, backlog,
                 is_ssl=False,
                 cert_file='activation.webex.com.cer',
                 key_file='activation.webex.com.key'):
        self._server = server
        self._backlog = backlog
        self._end_flag = b'\n'
        self._close_flag = b''
        self._is_ssl = is_ssl
        self._cert_file = cert_file
        self._key_file = key_file

    def create_socket(self, server, backlog):
        listenfd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listenfd.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listenfd.bind(server)
        listenfd.listen(backlog)
        print(f'Progress [{os.getpid()}] Listen on {listenfd.getsockname()}')
        return listenfd

    def accept(self, listenfd):
        requestfd, addr = listenfd.accept()
        print(f'Progress [{os.getpid()}] Got connection from {addr}')
        return requestfd, addr

    def parse_request(self, requestfd, addr, requestq):
        data = requestfd.recv(100)
        while data != self._close_flag:
            print(f'Progress [{os.getpid()}] Got data: {data} from {requestfd.getpeername()}')
            if requestq.full():
                raise queue.Full
            else:
                requestq.put_nowait(data)
            if data.endswith(self._end_flag):
                return
            else:
                data = requestfd.recv(100)
        else:
            print(f'Progress [{os.getpid()}] Got data: {data} from {requestfd.getpeername()}')
            raise ValueError(f'Progress [{os.getpid()}] Got {data}[FIN] from {requestfd.getpeername()}')

    def handle_request(self, requestfd, addr):
        requestq = queue.Queue()
        while True:
            try:
                self.parse_request(requestfd, addr, requestq)
            except (ValueError, queue.Full) as excp:
                print(f'Progress [{os.getpid()}] Close connection, due to: {excp}')
                requestfd.close()
                return
            else:
                data = b''
                while not requestq.empty():
                    data += requestq.get_nowait()
                    print(f'Progress [{os.getpid()}] Queue data is：{data}')
                requestfd.sendall(data)

    # def handle(self, requestfd, addr):
    #     if self._is_ssl:
    #         try:
    #             requestfd = ssl.wrap_socket(requestfd,
    #                                         server_side=True,
    #                                         certfile=self._cert_file,
    #                                         keyfile=self._key_file,
    #                                         cert_reqs=None,
    #                                         ca_certs=None,
    #                                         ssl_version=None,
    #                                         ciphers=None)
    #         except ssl.SSLError as e:
    #             print(f'Progress [{os.getpid()}] SSL Error: {e}')
    #             requestfd.close()
    #     self.handle_request(requestfd, addr)

    def handle_chld(self, signum, stack):
        print(f'Progress [{os.getpid()}] Received signal {signum}')
        while True:
            try:
                wpid, _ = os.waitpid(-1, os.WNOHANG)
            except:
                continue
            else:
                if not wpid: break
                print(f'Progress [{os.getpid()}] child progress {wpid} has exited')

    def handle_int(self, signum, stack):
        sys.exit(f'Progress [{os.getpid()}] Received signal {signum}')

    def init_signals(self):
        signal.signal(signal.SIGCHLD, self.handle_chld)
        signal.signal(signal.SIGINT, self.handle_int)

    def run(self):
        # Create a tcp socket to serve clients
        listenfd = self.create_socket(self._server, self._backlog)
        self.init_signals()

        while True:
            # Block here to accept request, then fork a child progress
            try:
                requestfd, addr = self.accept(listenfd)
            except:
                continue
            else:
                print(f'Progress [{os.getpid()}] forking...')
                pid = os.fork()

                # Parent progress: closes its own requestfd, then wait signal chld occuring
                if pid:
                    requestfd.close()

                # Child process: closes its own listenfd, then handle client request until end
                else:
                    listenfd.close()
                    self.handle_request(requestfd, addr)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--host', default='192.168.1.104', type=str, help='server ip address')
    parser.add_argument('--port', default=8888, type=int, help='server port')
    parser.add_argument('--block', action='store_true', help='wether IO blocked or not')
    parser.add_argument('--backlog', default=2, type=int, help='max request number by server accepted at one time')
    args = parser.parse_args()

    TcpServer((args.host, args.port), args.backlog).run()
