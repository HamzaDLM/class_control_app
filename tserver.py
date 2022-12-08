# import threading
# import socket
# import time

# HOST = socket.gethostbyname(socket.gethostname())
# PORT = 4444
# ADDR = (HOST, PORT)

# def handle_client():
#     pass

# def execute_commands(client_id):
#     pass

# def main():
#     pass


# if __name__ == "__main__":
#     pass

#Host Side script
#Host will be sending the screen to client.

import numpy as np 
import socket
from PIL import ImageGrab

filename = 'host_data.npy'

print("started.\nListening for connections...")
s = socket.socket()
s.bind((socket.gethostname(), 1234))
s.listen(0)

conn, addr = s.accept()
print('connection established.')

img = np.array(ImageGrab.grab())
np.save(filename, img)
file = open(filename, 'rb')
data = file.read(1024)
conn.send(data)

while data != b'':
    data = file.read(1024)
    conn.send(data)

print('data has been successfully transmitted.')