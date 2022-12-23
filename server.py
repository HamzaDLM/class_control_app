# CLASS CONTROL APP - SERVER SIDE (TEACHER)
# TODO: add a remote updater (def to look for changes and update accordingly)
from threading import Thread
import numpy as np
import socket
from datetime import datetime
import time
from PIL import Image
import os
import sys
import pickle

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
INFO = f'[{MAIN}Info{END}]'
WARNING = f'[{LRED}Warning{END}]'
IMPORTANT = f'[{ORANGE}Important{END}]'
FAILING = f'[{RED}Fail{END}]'
DEBUG = f'[{ORANGE}Debug{END}]'
SUCCESS = f'[{GREEN}SUCCESS{END}]'

HOST = socket.gethostbyname(socket.gethostname())
PORT = 4444
ADDR = (HOST, PORT)

client_store = {}

class CCA_SERVER:
    def __init__(self, host, port):
        self.host = host
        self.port = port

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
                                             by HamzaDLM
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

                INFORMATION
        - help        : GET ALL AVAILABLE COMMANDS
        - mac         : GET MACHINE'S MAC ADDRESS
        - history     : GET BROWSER HISTORY (LAST 20)
        - scrn        : GET SCREENSHOT OF CURRENT SESSION

                CONTROL
        - killc       : DISCONNECT CLIENT
        - quit        : DISCONNECT SERVER
        - shutdown    : SHUTDOWN THE CLIENT'S DEVICE
        - voloff      : TURN VOLUME TO 0%
        - volon       : TURN VOLUME TO 100%
        - monoff      : TURN MONITOR OFF
        - monon       : TURN MONITOR ON

        '''
        )

    def list_client_commands(self):
        print(
            r'''

        List of client specific commands:

                INFORMATION 
        - help        : GET ALL AVAILABLE COMMANDS
        - mac         : GET MACHINE'S MAC ADDRESS
        - history     : GET BROWSER HISTORY (LAST 20)
        - scrn        : GET SCREENSHOT OF CURRENT SESSION

                CONTROL
        - killc       : DISCONNECT CLIENT
        - quit        : DISCONNECT SERVER
        - shutdown    : SHUTDOWN THE CLIENT'S DEVICE
        - voloff      : TURN VOLUME TO 0%
        - volon       : TURN VOLUME TO 100%
        - monoff      : TURN MONITOR OFF
        - monon       : TURN MONITOR ON

        '''
        )

    def execute_commands(self):
        global current_client # all or id of client
        current_client = None
        while True:
            global command

            if current_client:
                command = input(f'> connected to {current_client} > ')
                client_store[current_client]['commands'].append(command)
                if current_client and 'quit' in command:
                    current_client = None 

            else:
                command = input('> ')

                if 'help' in command:
                    self.list_commands()

                elif 'list' in command:
                    print(f'\n{"ID":<8} {"HOST":<15} {"PORT":<10} {"MAC":<20} {"SYSTEM":<20} {"Joined":<20}')
                    if client_store:
                        for k, v in client_store.items():
                            addr = v['address']
                            mac = v['mac']
                            system = v['system']
                            joined = v['joined']
                            print(f"{k:<8} {addr[0]:<15} {addr[1]:<10} {mac:<20} {system:<20} {joined:<20}")
                    else:
                        print('\nNo devices connected to host')
                        
                elif 'connect' in command:
                    parse = command.split(' ')
                    current_client = parse[-1]

                elif 'quit' in command:
                    confirmation = input('Do you wish to terminate the session? [y/n]: ')
                    selection = True if confirmation in ['y', 'yes'] else False
                    if selection:
                        server_socket.close()
                        print(f'\n{INFO} Terminating server session.')
                        try:
                            sys.exit(0)
                        except SystemExit:
                            os._exit(0)
                    else:
                        server.main()

                else:
                    print(f"\n{WARNING}: {command} is not a valid command!")

    def get_ts(self):
        return str(int(time.time()))

    def receive_scrn(self, client):
        try:
            img_path = os.path.join(LOCATION, f'scrn/host__{self.get_ts()}.npy')
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
            print(f"\n{SUCCESS}: screenshot received")
        except:
            print(f"\n{WARNING}: screenshot failed")
            server_socket.close()

    def result(self, client):
        client.send(command.encode())
        result_output = client.recv(1024).decode()
        print('\n' + result_output)

    def handle_client(self, client_id):
        print(f"\n{INFO} Connected to: {client_store[client_id]['address']}")
        # Get basic info to fill the client table
        s = client_store[client_id]['socket']
        client_store[client_id]['mac'] = s.recv(1024).decode()
        s.send(b'received')
        client_store[client_id]['system'] = s.recv(1024).decode()
        s.send(b'received')
        while True:
            # Extract commands and socket for this client instance
            c = client_store[client_id]['commands']
            if len(c) > 0:
                for com in c:
                    if 'help' in com:
                        self.list_client_commands()

                    elif 'mac' in com:
                        self.result(s)
                    
                    elif 'shutdown' in com:
                        self.result(s)
                    
                    elif 'volon' in com:
                        self.result(s)

                    elif 'voloff' in com:
                        self.result(s)

                    elif 'monon' in com:
                        self.result(s)
                    
                    elif 'monoff' in com:
                        self.result(s)

                    elif 'killc' in com:
                        self.result(s)
                    
                    elif command == 'quit':
                        print(f"\n{INFO} Terminating server connection!")
                        s.close()
                        break

                    elif command == 'history':
                        s.send(command.encode())
                        result = s.recv(1024 * 10)
                        result = pickle.loads(result)
                        for h in result:
                            print(f"\n{datetime.fromtimestamp(h)} : {result[h]}")

                    elif command == 'scrn':
                        s.send(command.encode())
                        self.receive_scrn(s)

                    else:
                        print(f"\n{WARNING}: {command} is not a valid command!")
                    
                    c.remove(com)

            time.sleep(1)
            

    def main(self):
        try:
            global server_socket
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_socket.bind(ADDR)
        except socket.error as err:
            print(f'\n{FAILING}: Socket creation failed: {err}')
            try:
                sys.exit(0)
            except SystemExit:
                os._exit(0)
        server_socket.listen(20)
        commands_thread = Thread(target=self.execute_commands)
        commands_thread.start()
        while True:
            # On client connection, initiate socket socket and add to store 
            client_socket, client_address = server_socket.accept()
            client_id = str(len(client_store)+1)
            client_store[client_id] = {
                'address': client_address,
                'socket': client_socket,
                'commands': [],
                'mac': 'N/A',
                'system': 'N/A',
                'joined': self.get_ts(),
            }
            client_thread = Thread(target=self.handle_client, args=(client_id,))
            client_thread.start()


if __name__ == "__main__":
    try:
        server = CCA_SERVER(HOST, PORT)
        server.banner()
        server.main()
    except KeyboardInterrupt:
        # FIXME: fix the interupt process by keyboard
        print(f"\n{INFO} Keyboard interrupt initiated")
        server_socket.close()
        print(f'\n{INFO} Terminating server session.')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
