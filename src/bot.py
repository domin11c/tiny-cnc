from .base import *
from time import sleep

class BOTHandler(HandlerSocket):

    def __init__(self, sock: socket, sockAddr: tuple) -> None:
        super().__init__(sock, sockAddr)
        BOTManager.add(self)

    def handler(self) -> None:
        self.setTimeout(10)

        while 1:
            try:
                self.send('tiny')
                
                if self.recv(escape=False) == 'tall':
                    sleep(5)
                else:
                    break
                
            except Exception:
                break
        
        BOTManager.remove(self)
        self.close()

class BOTServer(ServerSocket):

    def __init__(self, addr: str, port: int) -> None:
        super().__init__(addr, port, BOTHandler)