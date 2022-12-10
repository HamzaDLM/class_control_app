from threading import Thread
import socket
import time
import sys 

HOST = socket.gethostbyname(socket.gethostname())
PORT = 4444
ADDR = (HOST, PORT)

clients = []

def handle_client(client_socket, client_address):
    print("Connected to: ", client_address)
    data = client_socket.recv(1024).decode()
    print(data)

def execute_commands():
    while True:
        global command
        command = input('command > ')
        print(command)

def main():
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(ADDR)
        print('socket created')
    except socket.error as err:
        print('socket creation failed: ', err)
        sys.exit()
    server_socket.listen(20)
    main_thread = Thread(target=execute_commands)
    main_thread.start()
    while True:
        client_socket, client_address = server_socket.accept()
        clients.append(client_address)
        client_thread = Thread(target=handle_client, args=(client_socket, client_address))
        client_thread.start()


if __name__ == "__main__":
    main()
