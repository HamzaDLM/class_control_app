import socket

HOST = socket.gethostbyname(socket.gethostname())
PORT = 4444
ADDR = (HOST, PORT)

def main():
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(ADDR)
        client_socket.send(b'connected')
    except:
        print('prblem')
    while True:
        command = client_socket.recv(1024).decode()
        if command == "something":
            print(command)

if __name__ == "__main__":
    main()