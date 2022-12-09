#This is client side script

import socket
import numpy as np 
# import cv2
from PIL import ImageGrab

s = socket.socket()
s.connect((socket.gethostname(), 1234))
print("connected.")

# img #
filename = 'host_data.npy'

img = np.array(ImageGrab.grab())
np.save(filename, img)
file = open(filename, 'rb')
data = file.read(1024)
s.send(data)

while data != b'':
    data = file.read(1024)
    s.send(data)
# img #

s.close()