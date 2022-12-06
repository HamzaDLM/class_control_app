# CLASS CONTROL APP - SERVER SIDE (TEACHER)
import socket
import pickle
from datetime import datetime

class bcolors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


class CCA_SERVER:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def start_connection(self):
        global client, addr, sock
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((self.host, self.port))
        sock.listen(5)
        print("[*] Waiting for the client...")
        client, addr = sock.accept()
        print()
        ipcli = client.recv(1024).decode()
        print(f"[*] Connection is established successfully with {ipcli}")
        print()

    def list_commands(self):
        print(
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

    List of commands:

        - getmacaddr  : GET MACHINE'S MAC ADDRESS
        - exitclient  : DISCONNECT CLIENT
        - exitserver  : DISCONNECT SERVER
        - bhistory    : GET BROWSER HISTORY (LAST 40)

        """
        )

    def result(self):
        client.send(command.encode())
        result_output = client.recv(1024).decode()
        print(result_output)

    def execute(self):
        self.list_commands()
        while True:
            global command
            command = input("Command: ")

            if command == "getmacaddr":
                self.result()

            elif command == "exitclient":
                self.result()

            elif command == "exitserver":
                print("Terminating server connection!")
                break

            elif command == "bhistory":
                client.send(command.encode())
                result = client.recv(1024*10)
                result = pickle.loads(result)
                for h in result: print(f"{datetime.fromtimestamp(h)} : {result[h]}")

            else:
                print(
                    f"{bcolors.WARNING}Warning: {command} is not a valid command!{bcolors.ENDC}"
                )


server = CCA_SERVER("127.0.0.1", 4444)

if __name__ == "__main__":
    server.start_connection()
    server.execute()
