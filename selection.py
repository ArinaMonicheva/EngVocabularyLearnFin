import subprocess
import sys
import tkinter as tk
from pynput.keyboard import Key, Listener
import pyautogui
import keyboard
import os
from PIL import Image, ImageTk
from functools import partial


WIDTH, HEIGHT = 1600, 900
topx, topy, botx, boty = 0, 0, 0, 0

rect_id = None
pyautogui.screenshot("./straight_to_disk.png")
path="mtr.jpg"

def get_mouse_posn(event):
    global topy, topx
    topx, topy = event.x, event.y

def update_sel_rect(event):
    global rect_id
    global topy, topx, botx, boty

    botx, boty = event.x, event.y
    canvas.coords(rect_id, topx, topy, botx, boty)  # Update selection rect.
    print( botx, boty, topx, topy)


window = tk.Tk()
window.title("Select Area")
window.geometry('%sx%s' % (WIDTH, HEIGHT))
window.configure(background='grey')

img = ImageTk.PhotoImage(Image.open("./straight_to_disk.png"))
canvas = tk.Canvas(window, width=img.width(), height=img.height(),borderwidth=0, highlightthickness=0)
canvas.pack(expand=True)
canvas.img = img  # Keep reference in case this code is put into a function.
canvas.create_image(0, 0, image=img, anchor=tk.NW)
# Create selection rectangle (invisible since corner points are equal).
rect_id = canvas.create_rectangle(topx, topy, topx, topy, dash=(2,2), fill='', outline='red')
canvas.bind('<Button-1>', get_mouse_posn)
canvas.bind('<B1-Motion>', update_sel_rect)



def exit_on_key(keyname):
    """ Create callback function that exits current process when the key with
        the given name is pressed.
    """
    def callback(event):
        print(event.name)
        if event.name == keyname:
            tcX=min(topx,botx)
            tcY=min(topy,boty)
            rWIDTH=max(topx,botx)-tcX
            rHEIGHT=max(topy,boty)-tcY

            fname = "./data.rect"
            file_rect = open(fname, 'w')
            file_rect.write('\n'.join([ str(tcX), str(tcY), str(rWIDTH), str(rHEIGHT)]))
            # Closing file
            file_rect.close()

            subprocess.Popen(['python', './prcl.py', str(tcX), str(tcY), str(rWIDTH), str(rHEIGHT)])
            sys.exit()
    return callback

if __name__ == '__main__':
    keyboard.hook(exit_on_key('esc'))
    window.mainloop()