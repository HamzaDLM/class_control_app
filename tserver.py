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
from PIL import Image


print("started.\nListening for connections...")
s = socket.socket()
s.bind((socket.gethostname(), 1234))
s.listen(0)

conn, addr = s.accept()
print(addr)
print('connection established.')

# img #
filename = 'client_data.npy'
file = open(filename, 'wb')

data = conn.recv(1024)
file.write(data)

while data != b'':
    data = conn.recv(1024)
    file.write(data)
file.close()

o_file = np.load(filename)
PIL_image = Image.fromarray(np.uint8(o_file)).convert('RGB')
# PIL_image = Image.fromarray(numpy_image.astype('uint8'), 'RGB')
PIL_image.show()
# o_file = cv2.cvtColor(o_file, cv2.COLOR_BGR2RGB)
# cv2.imshow('transferred file', o_file)
# cv2.waitKey(0)
# img #


print('data has been successfully transmitted.')