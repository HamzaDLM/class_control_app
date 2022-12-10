import socket
import time

HOST = socket.gethostbyname(socket.gethostname())
PORT = 4444
ADDR = (HOST, PORT)

def main():
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(ADDR)
        client_socket.send(b'connected')
        # Send mac address
    except:
        print('prblem')
    while True:
        time.sleep(1)
        command = client_socket.recv(1024).decode()
        if command == "something":
            print(command)

if __name__ == "__main__":
    main()