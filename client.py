# CLASS CONTROL APP - CLIENT SIDE (STUDENTS)
# TODO:: check if connection still maintained
from getmac import get_mac_address
from browser_history import get_history
from PIL import ImageGrab
import os
import time
import platform as plt
import socket
import pickle
from datetime import datetime
import numpy as np

MAC_ADDRESS = get_mac_address()
LOCATION = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
HOST_PATH = "C:\Windows\System32\drivers\etc\hosts"
IP_ADDRESS = "127.0.0.1"
PLATFORM = {"system": plt.system(), "release": plt.release(), "version": plt.version()}

class CCA_CLIENT:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def start_connection(self):
        global sock
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self.host, self.port))
        sending = socket.gethostbyname(socket.gethostname())
        sock.send(sending.encode())
        print(f"[*] Connected to host {self.host}:{self.port}")

    def execute(self):
        while True:
            command = sock.recv(1024).decode()

            if command == "getmacaddr":
                sock.send(MAC_ADDRESS.encode())

            elif command == "bhistory":
                sock.send(self.getHistory())

            elif command == "screenshot":
                print('started scrn')
                self.getScreenshot()

            elif command == "exitclient":
                sock.send(b"exit")
                break

    def getTS(self):
        return str(int(time.time()))

    def getHistory(self):
        # Get the last 20 browser history items
        b_history = get_history()
        b_history = b_history.histories  # [(date/url),]
        b_history = b_history[len(b_history) - 20 : len(b_history)]
        f = lambda p: (datetime.timestamp(p[0]), p[1])
        b_history = dict(map(f, b_history))

        return pickle.dumps(b_history)

    def getScreenshot(self):
        print('started screenshot')
        img_array = np.array(ImageGrab.grab())
        img_path = os.path.join(LOCATION, f"scrn/{MAC_ADDRESS}_{self.getTS()}.npy")
        np.save(img_path, img_array)
        file = open(img_path, 'rb')
        data = file.read(1024)
        sock.send(data)
        while data != b'':
            print('sending...')
            data = file.read(1024)
            sock.send(len(data))
        sock.send(b'')
        print('[*] Screenshot sent successfully')


if __name__ == "__main__":
    client = CCA_CLIENT("127.0.0.1", 4444)
    while True:
        try:
            client.start_connection()
            client.execute()
        except:
            print("[*] Looking for master!")
        time.sleep(2)
