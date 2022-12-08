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

ANSI_color = {
    "HEADER": "\033[95m",
    "OKBLUE": "\033[94m",
    "OKCYAN": "\033[96m",
    "OKGREEN": "\033[92m",
    "WARNING": "\033[93m",
    "FAIL": "\033[91m",
    "ENDC": "\033[0m",
    "BOLD": "\033[1m",
    "UNDERLINE": "\033[4m",
}

def log_level(level):
    match level:
        case "info":
            return f"[{ANSI_color['OKBLUE']}INFO{ANSI_color['ENDC']}]"
        case "warning":
            return f"[{ANSI_color['WARNING']}WARNING{ANSI_color['ENDC']}]"
        case "fatal":
            return f"[{ANSI_color['FATAL']}FATAL{ANSI_color['ENDC']}]"
        case "success":
            return f"[{ANSI_color['OKGREEN']}SUCCESS{ANSI_color['ENDC']}]"

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
                print(f"{log_level('info')} Waiting for the client...")
                client, addr = sock.accept()
                ipcli = client.recv(1024).decode()
                print(f"{log_level('success')} Connection is established successfully with {ipcli}")
                break
            except:
                print(f"{log_level('warning')} Host address already in use")
                sock.close()
            time.sleep(2)

    def banner(self):
        print(
            ANSI_color['FAIL'] + 
            r"""
________/\\\\\\\\\________/\\\\\\\\\_____/\\\\\\\\\____        
 _____/\\\////////______/\\\////////____/\\\\\\\\\\\\\__       
  ___/\\\/_____________/\\\/____________/\\\/////////\\\_      
   __/\\\______________/\\\_____________\/\\\_______\/\\\_     
    _\/\\\_____________\/\\\_____________\/\\\\\\\\\\\\\\\_    
     _\//\\\____________\//\\\____________\/\\\/////////\\\_   
      __\///\\\___________\///\\\__________\/\\\_______\/\\\_  
       ____\////\\\\\\\\\____\////\\\\\\\\\_\/\\\_______\/\\\_ 
        _______\/////////________\/////////__\///________\///__
""" + ANSI_color['ENDC'] + """
        Type help to see available commands!
"""
        )

    def list_commands(self):
        print(
            r"""
        List of commands:

        - getmacaddr  : GET MACHINE'S MAC ADDRESS
        - exitclient  : DISCONNECT CLIENT
        - quit        : DISCONNECT SERVER
        - bhistory    : GET BROWSER HISTORY (LAST 40)
        - screenshot  : GET SCREENSHOT OF CURRENT SESSION
        - turnoff     : TURN OFF THE CLIENT DEVICE
        - help        : GET ALL AVAILABLE COMMANDS
        """
        )

    def result(self):
        client.send(command.encode())
        result_output = client.recv(1024).decode()
        print(result_output)

    def execute(self):
        while True:
            global command
            command = input("Command >> ")

            if command == "getmacaddr":
                self.result()

            elif command == "help":
                self.list_commands()

            elif command == "help":
                self.list_commands()

            elif command == "exitclient":
                self.result()

            elif command == "quit":
                print(f"{log_level('info')} Terminating server connection!")
                sock.close()
                break

            elif command == "bhistory":
                client.send(command.encode())
                result = client.recv(1024 * 10)
                result = pickle.loads(result)
                for h in result:
                    print(f"{datetime.fromtimestamp(h)} : {result[h]}")

            elif command == "screenshot":
                client.send(command.encode())
                self.receive_scrn()

            else:
                print(
                    f"{log_level('warning')}: {command} is not a valid command!"
                )

    def getTS(self):
        return str(int(time.time()))

    def receive_scrn(self):
        img_path = os.path.join(LOCATION, f"scrn/host__{self.getTS()}.npy")
        file = open(img_path, 'wb')
        data = client.recv(1024)
        file.write(data)
        while data != b'':
            print('receiving...')
            data = client.recv(1024)
            file.write(data)
        file.close()
        o_file = np.load(img_path)
        pil_img = Image.fromarray(np.uint8(o_file)).convert('RGB')
        pil_img.show()
        print(f"{log_level('success')}: screenshot received!")

    

if __name__ == "__main__":
    server = CCA_SERVER("127.0.0.1", 4444)
    server.banner()
    server.start_connection()
    server.execute()
