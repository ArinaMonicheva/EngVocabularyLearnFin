import subprocess

import psutil
from subprocess import Popen, PIPE
import win32gui
processlist = list()
win_list = []
import dearpygui.dearpygui as dpg




global list_boxes,idx,lines
list_boxes=[]
idx=0
lines=[["sfskv vk njf nds,jfn d,",[0,0],[500,30]],  ["rewgwrwgs gs grts gh",[0,40],[500,70]] ]
#lines=[["мама мыла раму",[0,0],[400,30]],  ["долго из крмана",[0,35],[400,65]] ]


def callback(hwnd, strings):
    if win32gui.IsWindowVisible(hwnd):
        window_title = win32gui.GetWindowText(hwnd)
        left, top, right, bottom = win32gui.GetWindowRect(hwnd)
        if window_title and right-left and bottom-top:
            #strings.append('0x{:08x}: "{}"'.format(hwnd, window_title))
            strings.append(str(hwnd)+" "+window_title)
    return True

def enumw(win_list):
      # list of strings containing win handles and window titles
    win32gui.EnumWindows(callback, win_list)  # populate list

    for window in win_list:  # print results
        print(window)
enumw(win_list)

for process in psutil.process_iter():
        processlist.append(process)

def mwtitle(pid):
    process = Popen(['powershell', '.\mainwindowtitle.ps1',str(pid)], stdout=PIPE, stderr=PIPE)
    stdout, notused = process.communicate()
    return stdout.splitlines()[0].decode(encoding="oem")



def _log(sender, app_data, user_data):
    print(f"sender: {sender}, \t app_data: {app_data}, \t user_data: {user_data}")

def get_mwtitle(sender, app_data, user_data):
 #  pp=processlist[[p.name() for p in processlist].index(app_data)]
 #  title=mwtitle(pp.pid)
 #  print(title)
 #  return title
 #print(app_data.split(" ")[0])
     print(app_data)
     make_ovl(app_data)

dpg.create_context()
dpg.create_viewport(title="process list", width=500, height=300, decorated=True, always_on_top=True)
#dpg.get_item_info()
def ferreshpr():
    enumw(win_list)


with dpg.window(no_background=False, no_title_bar=False, tag="pwindow", pos=(300, 300), width=500, height=300):
    dpg.add_listbox([p for p in win_list], tag="prc_list", label="process to attach",  num_items=12, callback=get_mwtitle)


with dpg.font_registry():
    with dpg.font("notomono-regular.ttf", 13, default_font=True, tag="Default font") as f:
        dpg.add_font_range_hint(dpg.mvFontRangeHint_Cyrillic)


with dpg.handler_registry(show=False, tag="__demo_keyboard_handler"):
    k_down = dpg.add_key_down_handler(key=dpg.mvKey_0,callback=_log)
    k_release = dpg.add_key_release_handler(key=dpg.mvKey_0,callback=_log)
    k_press = dpg.add_key_press_handler(key=dpg.mvKey_0,callback=_log)
dpg.bind_font("Default font")

def make_ovl(t):
    subprocess.Popen(['python', './main.py'," ".join(t.split(" ")[1:]), t.split(" ")[0]])
    #sys.exit()



dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("pwindow", True)
dpg.start_dearpygui()
dpg.destroy_context()
