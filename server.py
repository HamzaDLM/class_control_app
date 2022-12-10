# CLASS CONTROL APP - SERVER SIDE (TEACHER)
# TODO: check if connection is still maintained
# TODO: add security via tokens and end-to-end encryption
# TODO: Support multiple clients
import numpy as np
import socket
import pickle
from datetime import datetime
import time
from PIL import Image
import os

LOCATION = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

# ANSI COLORS
MAIN = '\001\033[38;5;85m\002'
GREEN = '\001\033[38;5;82m\002'
GRAY = PLOAD = '\001\033[38;5;246m\002'
NAME = '\001\033[38;5;228m\002'
RED = '\001\033[1;31m\002'
FAIL = '\001\033[1;91m\002'
ORANGE = '\033[0;38;5;214m\002'
LRED = '\033[0;38;5;202m\002'
BOLD = '\001\033[1m\002'
UNDERLINE = '\001\033[4m\002'
END = '\001\033[0m\002'

# LOG LEVELS
INFO = f'{MAIN}Info{END}'
WARNING = f'{LRED}Warning{END}'
IMPORTANT = f'{ORANGE}Important{END}'
FAIL = f'{RED}Fail{END}'
DEBUG = f'{ORANGE}Debug{END}'
SUCCESS = f'{GREEN}SUCCESS{END}'

class CCA_SERVER:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def start_connection(self):
        global client, addr, sock
        while True:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.bind((self.host, self.port))
                sock.listen(5)
                print(f"{INFO} Waiting for the client...")
                client, addr = sock.accept()
                ipcli = client.recv(1024).decode()
                print(
                    f"{SUCCESS} Connection is established successfully with {ipcli}"
                )
                break
            except:
                print(f"{WARNING} Host address already in use")
                sock.close()
            time.sleep(2)

    def banner(self):
        print(
            FAIL
            + r'''
________/\\\\\\\\\________/\\\\\\\\\_____/\\\\\\\\\____        
 _____/\\\////////______/\\\////////____/\\\\\\\\\\\\\__       
  ___/\\\/_____________/\\\/____________/\\\/////////\\\_      
   __/\\\______________/\\\_____________\/\\\_______\/\\\_     
    _\/\\\_____________\/\\\_____________\/\\\\\\\\\\\\\\\_    
     _\//\\\____________\//\\\____________\/\\\/////////\\\_   
      __\///\\\___________\///\\\__________\/\\\_______\/\\\_  
       ____\////\\\\\\\\\____\////\\\\\\\\\_\/\\\_______\/\\\_ 
        _______\/////////________\/////////__\///________\///__
'''
            + END
            + '''
        Type help to see available commands!
'''
        )

    def list_commands(self):
        print(
            r'''
        List of commands:

        **** INFORMATION ****
        - help        : GET ALL AVAILABLE COMMANDS
        - mac         : GET MACHINE'S MAC ADDRESS
        - history     : GET BROWSER HISTORY (LAST 20)
        - scrn        : GET SCREENSHOT OF CURRENT SESSION

        **** CONTROL ****
        - killc       : DISCONNECT CLIENT
        - quit        : DISCONNECT SERVER
        - shutdown    : SHUTDOWN THE CLIENT'S DEVICE
        - voloff      : TURN VOLUME TO 0%
        - volon       : TURN VOLUME TO 100%
        - monoff      : TURN MONITOR OFF
        - monon       : TURN MONITOR ON

        **** SETTINGS ****
        '''
        )

    def result(self):
        client.send(command.encode())
        result_output = client.recv(1024).decode()
        print(result_output)

    def execute(self):
        while True:
            global command
            command = input('Command >> ')

            if command == 'mac':
                self.result()
            
            elif command == 'shutdown':
                self.result()

            elif command == 'volon':
                self.result()

            elif command == 'voloff':
                self.result()

            elif command == 'monon':
                self.result()

            elif command == 'monoff':
                self.result()

            elif command == 'help':
                self.list_commands()

            elif command == 'killc':
                self.result()

            elif command == 'quit':
                print(f"{INFO} Terminating server connection!")
                sock.close()
                break

            elif command == 'history':
                client.send(command.encode())
                result = client.recv(1024 * 10)
                result = pickle.loads(result)
                for h in result:
                    print(f"{datetime.fromtimestamp(h)} : {result[h]}")

            elif command == 'scrn':
                client.send(command.encode())
                self.receive_scrn()

            else:
                print(f"{WARNING}: {command} is not a valid command!")

    def getTS(self):
        return str(int(time.time()))

    def receive_scrn(self):
        try:
            img_path = os.path.join(LOCATION, f'scrn/host__{self.getTS()}.npy')
            file = open(img_path, 'wb')
            data = client.recv(1024)
            file.write(data)
            while data != b'':
                data = client.recv(1024)
                file.write(data)
                if len(data) < 1024:
                    break
            file.close()
            o_file = np.load(img_path)
            pil_img = Image.fromarray(np.uint8(o_file)).convert('RGB')
            pil_img.show()
            print(f"{SUCCESS}: screenshot received")
        except:
            print(f"{WARNING}: screenshot failed")
            sock.close()


if __name__ == '__main__':
    server = CCA_SERVER('127.0.0.1', 4444)
    server.banner()
    server.start_connection()
    server.execute()
