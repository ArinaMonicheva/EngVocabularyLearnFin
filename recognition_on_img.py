import copy
import os

import external_overlay
import timer
from external_overlay import ExternalOverlay
import dearpygui.dearpygui as dpg
import random
import string
import win32gui
import sys
import threading
import pyautogui
import paddleocr
import rapidfuzz
global PREVIOUS_FRAME_TXT


fname="./recognized.txt"

PASTE_DIST=rapidfuzz.distance.DamerauLevenshtein

PREVIOUS_FRAME_TXT = ""
BIN_DUMP_DIR = "./bin_dumps"
ocr = paddleocr.PaddleOCR(lang='en',
                          rec_model_dir="_models/rec/en/en_PP-OCRv4_rec_infer",
                          det_model_dir="_models/det/en/en_PP-OCRv4_det_infer",
                          use_gpu=True,
                          cls=False, show_log=False)
global list_boxes, idx, lines,WINDOW_WIDTH,rtopx,rtopy,rWIDTH,rHEIGHT
WINDOW_WIDTH=1000
WINDOW_HEIGHT=1000
file_rect = open('./data.rect', 'r')
lines_back=[]

title_pos=[[0,0],[1000,1000]]
wp=[[0,0],[500,300]]
DISPLACE_X=0
DISPLACE_Y=-20


def _log(sender, app_data, user_data):
    print(f"sender: {sender}, \t app_data: {app_data}, \t user_data: {user_data}")

def getrect(hwnd):
    global selection,title_pos
    rect = win32gui.GetWindowRect(hwnd)
    x = rect[0]
    y = rect[1]
    w = rect[2] - x
    h = rect[3] - y
    title_pos=[[x,y],[w,h]]

    print("Window %s:" % win32gui.GetWindowText(hwnd))
    print("\tLocation: (%d, %d)" % (x, y))
    print("\t    Size: (%d, %d)" % (w, h))


def intersection(lst1, lst2):
    return list(set(lst1) & set(lst2))


win_list=[]
ocr = paddleocr.PaddleOCR(lang='en',
                              rec_model_dir="_models/rec/en/en_PP-OCRv4_rec_infer",
                              det_model_dir="_models/det/en/en_PP-OCRv4_det_infer",
                              use_gpu=True,
                              cls=False, show_log=False)

def callback(hwnd, strings):
    path="./examples"
    rez = sorted(os.listdir(path))
    for n, item in enumerate(rez):
        strings.append(str(item))
    return True


def lsdir(path,strings):
    path = "./examples"
    rez = sorted(os.listdir(path))
    for n, item in enumerate(rez):
        strings.append(item)
    return strings


def enumw(win_list):
    # list of strings containing win handles and window titles
    win32gui.EnumWindows(callback, win_list)  # populate list

    for window in win_list:  # print results
        print(window)


def ferreshpr():
    enumw(win_list)


def _log(sender, app_data, user_data):
    print(f"sender: {sender}, \t app_data: {app_data}, \t user_data: {user_data}")


def predict(sender,path):
    path="./examples/"+path
    imgload(path)
    out = ocr.ocr(path)
    out_txt=""
    for di in out[0]:out_txt+="/"+di[1][0]+"/"
    print(out_txt)
    dpg.delete_item("prediction")
    dpg.draw_text([90,35], parent='pwindow', text=out_txt, tag="prediction", color=[255, 0, 0, 255], size=17)
    return out



#dpg.get_item_info()

dpg.create_context()
dpg.create_viewport(title="process list", width=800, height=700, decorated=True, always_on_top=True)

win_list=lsdir("./examples",win_list)
print(win_list)

def imgload(path,width=400,height=150):
    data = dpg.load_image(path)
 #   with dpg.texture_registry(show=True):
 #       dpg.add_static_texture(width=width, height=height, default_value=data, tag="texture_tag")
    #dpg.add_image("texture_tag",parent="pwindow")

with dpg.window(no_background=False, no_title_bar=False, tag="pwindow", pos=(300, 300), width=500, height=300):
    dpg.add_listbox([p for p in win_list], tag="prc_list", label="process to attach",  num_items=12, callback=predict)


with dpg.font_registry():
    with dpg.font("notomono-regular.ttf", 13, default_font=True, tag="Default font") as f:
        dpg.add_font_range_hint(dpg.mvFontRangeHint_Cyrillic)


with dpg.handler_registry(show=False, tag="__demo_keyboard_handler"):
    k_down = dpg.add_key_down_handler(key=dpg.mvKey_0,callback=_log)
    k_release = dpg.add_key_release_handler(key=dpg.mvKey_0,callback=_log)
    k_press = dpg.add_key_press_handler(key=dpg.mvKey_0,callback=_log)

dpg.bind_font("Default font")

dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("pwindow", True)
dpg.start_dearpygui()
dpg.destroy_context()
