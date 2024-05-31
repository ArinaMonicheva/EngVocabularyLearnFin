import copy
import json

import numpy as np

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

import argostranslate.package
import argostranslate.translate

from_code = "en"
to_code = "ru"

# Download and install Argos Translate package
argostranslate.package.update_package_index()
available_packages = argostranslate.package.get_available_packages()
package_to_install = next(
    filter(
        lambda x: x.from_code == from_code and x.to_code == to_code, available_packages
    )
)
argostranslate.package.install_from_path(package_to_install.download())


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
list_boxes = []
last_rpl=[]
idx = 0
lines = [["sfskv vk njf nds,jfn d,", [0, 0], [500, 30]], ["rewgwrwgs gs grts gh", [0, 40], [500, 70]]]
WINDOW_WIDTH=1000
WINDOW_HEIGHT=1000
file_rect = open('./data.rect', 'r')
rp=file_rect.readlines()
lines_back=[]
rtopx=int(rp[0])
rtopy=int(rp[1])
rWIDTH=int(rp[2])-int(rp[0])
rHEIGHT=int(rp[1])-int(rp[3])
selection=[[386,720],[537,119]]
selection=[[rtopx,rtopy],[rWIDTH,rHEIGHT]]
title_pos=[[0,0],[1000,1000]]
wp=[[0,0],[500,300]]
DISPLACE_X=0
DISPLACE_Y=-20
import nltk

nltk.download('averaged_perceptron_tagger')




#selection=[[selection[0][0]-wp[0][0],selection[0][1]-wp[0][1]],selection[1]]

# Load base English grammar dictionary
with open('base_english_grammar.txt', 'r', encoding='utf-8') as file:
    base_grammar = set(word.strip().lower() for word in file.readlines())

# Load or initialize dynamic dictionary
try:
    with open('dynamic_dictionary.json', 'r', encoding='utf-8') as file:
        dynamic_dictionary = json.load(file)
except FileNotFoundError:
    dynamic_dictionary = {}

DICTADD_TREASHHOLD=0.4
# DICTADD_TREASHHOLD=0.2 очень похожие контексты попадают в словарь
# DICTADD_TREASHHOLD=0.9 даже существенно отличающиеся контексты в словарь не попадают
def translate_and_filter(text, translator_function, context):
    global DICTADD_TREASHHOLD
    translated_text = translator_function(text)
    words = text.split()

    for word in words:
        word_lower = word.lower()
        if word_lower not in base_grammar:
            if word_lower in dynamic_dictionary:
                if context not in dynamic_dictionary[word_lower]:
                    ds=list(map(lambda  x:PASTE_DIST.normalized_distance(x, context), dynamic_dictionary[word_lower]))
                    if np.max(ds)>DICTADD_TREASHHOLD:
                        dynamic_dictionary[word_lower].append(context)
            else:
                dynamic_dictionary[word_lower] = [context]

    # Сохранение обновленного динамического словаря
    with open('dynamic_dictionary.json', 'w', encoding='utf-8') as file:
        json.dump(dynamic_dictionary, file, ensure_ascii=True, indent=4)

    # Filter out words in the base grammar dictionary
    filtered_words = [word for word in words if word.lower() not in base_grammar]
    return ' '.join(filtered_words)


def line_repos(l):
    global selection,DISPLACE_Y,DISPLACE_X,title_pos,rtopx,rtopy
    getrect(HWND)
    n_selection=copy.deepcopy(selection)
    n_selection[0][0]=selection[0][0]+rtopx
    n_selection[1][0]=selection[1][0]+rtopx

    n_selection[0][1]=selection[0][1]+rtopy
    n_selection[1][1]=selection[1][1]+rtopy
    rect=l[0]
    print(l)
    print(rect)
    print(title_pos)
    rect=[[c[0]+selection[0][0]-title_pos[0][0],c[1]+selection[0][1]-title_pos[0][1]] for c in rect]

    DISPLACE_Y=-1*(rect[2][1]-rect[1][1])

    w=rect[1][0]-rect[0][0]+DISPLACE_X
    h=17#rect[2][1]-rect[1][1]

    l[0]=[rect[0],[w,-h]]
    ratios=get_word_ratios(l[1][0])
    #spaces=len(("xgdsfg sgtasrg grg srg grs f").split()) - 1
    wths=list(map(lambda x:x*w,ratios))
    i=rect[0][0]
    j=0
    posxs=[]
    for www in wths:
        posxs.append(i)
        j=j+2
        i=i+www+5+j

    tokens = nltk.word_tokenize(l[1][0])
    pos_tags = nltk.pos_tag(tokens)
    [x[0] for x in list(filter(lambda x: x[1] in ["NOUN","ADV", "VERB" ], pos_tags))]

    wds=l[1][0].split(" ")

    i=0
    res=[]
    def translator(w):
        return argostranslate.translate.translate(w,"en","ru")

    for wd in wds:
        ruwd=translate_and_filter(wd,translator," ".join(wds))
        if(len(ruwd.strip())>0):
            pos=[posxs[i]+DISPLACE_X,rect[0][1]+DISPLACE_Y]
            res.append([ruwd,pos, [pos[0]+wths[i],pos[1]+h]])
        i=i+1

    print(res)
    return res

def hide_ui():
    dpg.hide_item("ovlwin")
   # v = dpg.get_item_state("ovlwin").visible
   # while (v):
   #     v = dpg.get_item_state("ovlwin").visible


def show_ui():
    dpg.show_item("ovlwin")

'''
def hide_ui():
    global list_boxes
    for itm in list_boxes:
        dpg.hide_item(itm)
    t=list_boxes[len(list_boxes)-1]
    v=dpg.get_item_state(t).visible
    while(v):
        v=dpg.get_item_state(t).visible
    pyautogui.screenshot("./straight_to_disk.png", region=(rtopx, rtopy, rWIDTH, rHEIGHT))

def show_ui():
    global list_boxes
    for itm in list_boxes:
        dpg.show_item(itm)
'''


def get_word_ratios(s):
    l=len(' '.join(s.split(" ")))
    r=list(map(lambda x:(len(x))/l, s.split(" ")))
    return r
# lines=[["мама мыла раму",[0,0],[400,30]],  ["долго из крмана",[0,35],[400,65]] ]

def clear_ui(a, b):
    global list_boxes
#    dpg.delete_item(list_boxes[0])
    for itm in list_boxes:
        dpg.delete_item(itm)
    list_boxes.clear()
    #timer.kill_timer(a)
    #external_overlay.show_demo()


def subs_str_clr():
    global list_boxes
    #dpg.delete_item(list_boxes[0])
    for itm in list_boxes:
        dpg.delete_item(itm)
    list_boxes.clear()
    lines.clear()


def rand_string():
    s = ''
    lns = [''.join(random.choices(string.ascii_letters + string.digits, k=random.randint(5, 8))) for i in
           range(0, random.randint(3, 8))]
    return ' '.join(lns)


def outtext(dpg, txt, pos, size):
    print(txt)
    print(pos)
    print(size)
    global list_boxes,idx
    #idx = int(len(list_boxes) / 2)
    txt_label = ("line_" + str(idx))
    box_label = ("box_" + str(idx))
    idx=idx+1
    #dpg.draw_rectangle(l[0], l[1], rounding=0.5, parent='ovlwin', color=[0, 255, 0, 20], tag=box_label,fill=[0, 255, 0, 255])
    dpg.draw_rectangle(list(pos), list(size), rounding=0.5, parent='ovlwin', color=[0, 255, 0, 60], tag=box_label,
                       fill=[0, 255, 0, 255])

    try:
        dsp=(size[0]-pos[0]-dpg.get_text_size(txt)[0])/2
    except:
        dsp=1
    dpg.draw_text([pos[0]+dsp,pos[1]], parent='ovlwin', text=txt, tag=txt_label, color=[255, 0, 0, 255], size=17)
    list_boxes.append(box_label)
    list_boxes.append(txt_label)

def draw_back(dpg):
    global list_boxes, idx,lines_back,rtopx,rtopy
    return
    for l in lines_back:
        box_label = ("box_" + str(idx))
        l[0][0]+=rtopx
        l[1][0]+=rtopx
        l[0][1]+=rtopy-12
        l[1][1]+=rtopy-6
        dpg.draw_rectangle(l[0], l[1], rounding=0.5, parent='ovlwin', color=[0, 255, 0, 20], tag=box_label, fill=[0, 255, 0, 255])
        idx = idx + 1
        list_boxes.append(box_label)


def repaint(a,b):
    wi = 0
    cursor = [[0, 0], [0, 0]]
    lns = rand_string().split(' ')
    subs_str_clr()
    sizes = [dpg.get_text_size(l) for l in lns]
    print(lns)
    print(sizes)
    for l in lns:

        lru=" ".join(list(map((lambda x: argostranslate.translate.translate(x, "en", "ru"), l.split(" ")))))
        print(lru)
        #cursor = [cursor[1][0], wi * 30], [cursor[1][0]+5+sizes[wi][0]*1.7, 25 + wi * 30]
        cursor = [cursor[1][0]+15, 30], [cursor[1][0]+sizes[wi][0]*1.7, 25 + 30]
        if cursor[1][0]>WINDOW_WIDTH:
            cursor=[[0,cursor[0][1]+25],[sizes[wi][0]+15,cursor[0][1]+25+30]]
        lines.append([lru, cursor[0], cursor[1]])
        wi = wi + 1

    print(lines)
    [outtext(dpg, l[0], l[1], l[2]) for l in lines]


def _log(sender, app_data, user_data):
    print(f"sender: {sender}, \t app_data: {app_data}, \t user_data: {user_data}")


def ui(tar_hwnd=None):
    global list_boxes, idx, lines,WINDOW_WIDTH,rp
    #   with dpg.font("D:\\_d3_js\\node\_videotranslate\\videocr-PaddleOCR-master\\external-ovl\\font\\Anonymous Pro.ttf", 18, default_font=True):
    with dpg.window(tag='ovlwin', no_background=True, no_title_bar=True, pos=(0, 0), width=WINDOW_WIDTH, height=WINDOW_HEIGHT):
        [outtext(dpg, l[0], l[1], l[2]) for l in lines]

    with dpg.font_registry():
        with dpg.font("notomono-regular.ttf", 13, default_font=True, tag="Default font") as f:
            dpg.add_font_range_hint(dpg.mvFontRangeHint_Cyrillic)
        dpg.bind_font("Default font")

        '''
    def on_key_la(sender, app_data):
        repaint(dpg)

    with dpg.handler_registry():
        dpg.add_key_press_handler(dpg.mvKey_F2, callback=on_key_la)
        '''
        #threading.Timer(3, get_screen).start()
        #timer.set_timer(5000,repaint)
        get_screen()

# timer.set_timer(5000,fillui)
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



def show_ui_after(a,b):
    show_ui()
    timer.kill_timer(a)

def save_screen():
    global rtopx, rtopy, rWIDTH, rHEIGHT, lines_back
    hide_ui()
   # clear_ui(0,0)

    pyautogui.screenshot("./straight_to_disk.png", region=(rtopx, rtopy, rWIDTH, rHEIGHT))
    show_ui()
    out=ocr.ocr("./straight_to_disk.png")
    lines_back=[[p[0][0], p[0][2]] for p in out[0]]
    return out


def intersection(lst1, lst2):
    return list(set(lst1) & set(lst2))


def get_screen():
    global fname,lines,last_rpl
    r=save_screen()
    s=""
    outfile = open(fname, 'a')
    print(str(r),file=outfile)
    outfile.close()
    global PREVIOUS_FRAME_TXT
    r[0]=list(filter(lambda x:((x[1][1]>=0.9) and (len(intersection(last_rpl,x[1][0].split(" ")))<len(x[1][0].split(" "))/2)) ,r[0]))
    txts=list(map(lambda e: e[1][0], r[0]))
    dist=PASTE_DIST.normalized_distance(" ".join(txts), PREVIOUS_FRAME_TXT)
    #print(dist)
    if dist > 0.3:
        PREVIOUS_FRAME_TXT=" ".join(txts)
        clear_ui(0, 0)
        if len(r[0]) > 0:
            rpl=[line_repos(e) for e in r[0]]  # sum([line_repos(e) for e in r], [])
            #print(rpl)
            last_rpl=sum(rpl,[])
           # draw_back(dpg)
            [outtext(dpg, e[0], e[1], e[2]) for e in last_rpl]
            last_rpl=[e[0] for e in last_rpl]
        print(PREVIOUS_FRAME_TXT)
    threading.Timer(1, get_screen).start()






'''
if (len(sys.argv) >= 5):
    topx, topy, WIDTH, HEIGHT = list(map(lambda x: int(x), sys.argv[2:]))
else:
    topx, topy, WIDTH, HEIGHT = list([0, 0, 1900, 1080])
'''
HWND=int(sys.argv[2])
getrect(HWND)

overlay = ExternalOverlay(sys.argv[1], ui)
overlay.start()
