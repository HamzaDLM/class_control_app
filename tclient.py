#This is client side script

import socket
import numpy as np 
# import cv2
from PIL import Image

s = socket.socket()
s.connect((socket.gethostname(), 1234))
print("connected.")

filename = 'client_data.npy'
file = open(filename, 'wb')

data = s.recv(1024)
file.write(data)

while data != b'':
    data = s.recv(1024)
    file.write(data)
file.close()

o_file = np.load(filename)
PIL_image = Image.fromarray(np.uint8(o_file)).convert('RGB')
# PIL_image = Image.fromarray(numpy_image.astype('uint8'), 'RGB')
PIL_image.show()
# o_file = cv2.cvtColor(o_file, cv2.COLOR_BGR2RGB)
# cv2.imshow('transferred file', o_file)
# cv2.waitKey(0)
s.close()