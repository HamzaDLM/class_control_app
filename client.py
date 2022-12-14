# CLASS CONTROL APP - CLIENT SIDE (STUDENTS)
# TODO: check if connection still maintained
# TODO: instead of turning monitor off, black screen overlay with message (Focus on your teacher) + turn off keyboards
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
from ctypes import cast, POINTER
import ctypes
from utils import encrypt_send, decrypt_recv


# FIXME: to point to server?
HOST = socket.gethostbyname(socket.gethostname())
PORT = 4444
ADDR = (HOST, PORT)

MAC_ADDRESS = get_mac_address()
LOCATION = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
HOST_PATH = "C:\Windows\System32\drivers\etc\hosts"
IP_ADDRESS = "127.0.0.1"
PLATFORM = {"system": plt.system(), "release": plt.release(), "version": plt.version()}
BUF_SIZE = 1024

HWND_BROADCAST = 65535
WM_SYSCOMMAND = 274
SC_MONITORPOWER = 61808
GENERIC_READ = -2147483648
GENERIC_WRITE = 1073741824
FILE_SHARE_WRITE = 2
FILE_SHARE_READ = 1
FILE_SHARE_DELETE = 4
CREATE_ALWAYS = 2

# FIXME:
AES_KEY = "C&F)J@NcRfUjXn2r"

if "Windows" in PLATFORM["system"]:
    user32 = ctypes.WinDLL("user32")
    kernel32 = ctypes.WinDLL("kernel32")


class CCA_CLIENT:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    @staticmethod
    def send_msg(client, data: str) -> None:
        cipher = encrypt_send(AES_KEY, data)
        client.send(cipher)

    @staticmethod
    def recv_msg(client, buf_size=BUF_SIZE) -> bytes:
        cipher = client.recv(buf_size)
        msg = decrypt_recv(AES_KEY, cipher)
        return msg

    def start_connection(self):
        global sock
        print("[*] Looking for master!")
        while True:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.connect((self.host, self.port))
                self.send_msg(sock, MAC_ADDRESS.encode())
                self.recv_msg()
                self.send_msg(sock, f"{PLATFORM['system']} {PLATFORM['release']}".encode())
                self.recv_msg()
                print(f"[*] Connected to host {self.host}:{self.port}")
                break
            except:
                sock.close()
            time.sleep(2)

    def execute_commands(self):
        while True:
            # FIXME: fix when server releases the connection (infinite loop)
            command = self.recv_msg().decode()

            if command == "mac":
                self.send_msg(sock, MAC_ADDRESS.encode())

            elif command == "history":
                self.send_msg(sock, self.getHistory())

            elif command == "scrn":
                self.getScreenshot()

            elif command == "killc":
                self.send_msg(sock, b"exit")
                break

            elif command == "volon":
                self.ctrlVolume(1)

            elif command == "voloff":
                self.ctrlVolume(0)

            elif command == "shutdown":
                os.system("shutdown /s /t 3")  # shutdown after 3 seconds
                self.send_msg(sock, 
                    f"{socket.gethostbyname(socket.gethostname())} is being shutdown".encode()
                )
                sock.close()

            elif command == "monoff":
                self.ctrlMonitor(0)

            elif command == "monon":
                self.ctrlMonitor(1)

            time.sleep(1)

    def ctrlMonitor(self, status: int):
        try:
            if "Windows" in PLATFORM["system"]:
                if status:
                    self.send_msg(sock, 
                        f"{socket.gethostbyname(socket.gethostname())}'s monitor was turned on".encode()
                    )
                    user32.SendMessage(
                        HWND_BROADCAST, WM_SYSCOMMAND, SC_MONITORPOWER, -1
                    )
                if not status:
                    self.send_msg(sock, 
                        f"{socket.gethostbyname(socket.gethostname())}'s monitor was turned off".encode()
                    )
                    user32.SendMessage(
                        HWND_BROADCAST, WM_SYSCOMMAND, SC_MONITORPOWER, 2
                    )
            if "Linux" in PLATFORM["system"]:
                import subprocess

                if status:
                    subprocess.run(["xset", "-display", ":0.0", "dpms", "force", "off"])
                if not status:
                    subprocess.run(["xset", "-display", ":0.0", "dpms", "force", "on"])
        except:
            print("Error with monitor command!")
            self.send_msg(sock, b"Problem with monitor command")

    def ctrlVolume(self, status: int):
        try:
            if "Windows" in PLATFORM["system"]:
                from comtypes import CLSCTX_ALL
                from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

                devices = AudioUtilities.GetSpeakers()
                interface = devices.Activate(
                    IAudioEndpointVolume._iid_, CLSCTX_ALL, None
                )
                volume = cast(interface, POINTER(IAudioEndpointVolume))
                if status:
                    if volume.GetMute() == 1:
                        volume.SetMute(0, None)
                    volume.SetMasterVolumeLevel(volume.GetVolumeRange()[1], None)
                    self.send_msg(sock, "Volume is increased to 100%".encode())
                else:
                    volume.SetMasterVolumeLevel(volume.GetVolumeRange()[0], None)
                    self.send_msg(sock, "Volume is decreased to 0%".encode())
            if "Linux" in PLATFORM["system"]:
                from subprocess import call

                if status:
                    call(["amixer", "-D", "pulse", "sset", "Master", "50%"])
                    self.send_msg(sock, "Volume is decreased to 50%".encode())
                if not status:
                    call(["amixer", "-D", "pulse", "sset", "Master", "0%"])
                    self.send_msg(sock, "Volume is decreased to 0%".encode())
        except:
            print("Error with volume command!")
            self.send_msg(sock, b"Problem with volume command")

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
        img_array = np.array(ImageGrab.grab())
        # img_size = img_array.size * img_array.itemsize
        img_path = os.path.join(LOCATION, f"scrn/{MAC_ADDRESS}_{self.getTS()}.npy")
        np.save(img_path, img_array)
        file = open(img_path, "rb")
        data = file.read(BUF_SIZE)
        self.send_msg(sock, data)
        while data != b"":
            data = file.read(BUF_SIZE)
            self.send_msg(sock, data)
        print("[*] Screenshot sent successfully")


if __name__ == "__main__":
    # TODO: add the interupt process
    client = CCA_CLIENT(HOST, PORT)
    try:
        client.start_connection()
        client.execute_commands()
    except:
        print("Error occured")
    print("[*] Terminating session")
