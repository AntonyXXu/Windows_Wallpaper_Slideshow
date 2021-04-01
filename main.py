"""
Required API:
Python Image Library (install via "pip install Pillow")
"""
import time
import os
import ctypes as ct
import shutil
from PIL import Image
from random import shuffle

from photo_init import get_images


#Initialize ctypes functionality
user32 = ct.windll.user32

#Set up global variables:
PATH = os.getcwd()
TIMER_MIN = 1

#Structure RECT for use in pulling monitor data
class RECT(ct.Structure):
     _fields_ = [
        ('left', ct.c_long),
        ('top', ct.c_long),
        ('right', ct.c_long),
        ('bottom', ct.c_long)
     ]
     def get_fields(self):
        return [self.left, self.top, self.right, self.bottom]

class Monitor:
    def __init__(self, monitor_data):
        self.left = monitor_data[0]
        self.top = monitor_data[1]
        self.right = monitor_data[2]
        self.bottom = monitor_data[3]
        self.horizontal = True if self.width() >= self.height() else False
    def width(self):
        return abs(self.right - self.left)
    def height(self):
        return abs(self.bottom - self.top)

class TotalScreen(Monitor):
    def __init__(self, monitor = [0,0,0,0]):
        super().__init__(monitor)
    def update(self, new_monitor):
        if new_monitor.left < self.left:
            self.left = new_monitor.left
        if new_monitor.top < self.top:
            self.top = new_monitor.top
        if new_monitor.right > self.right:
            self.right = new_monitor.right
        if new_monitor.bottom > self.bottom:
            self.bottom = new_monitor.bottom
        return

def enum_display_monitors():
    #Windows function to get monitor size
    monitor_list = []
    monitor_enum_proc = ct.WINFUNCTYPE(ct.c_int, ct.c_ulong, ct.c_ulong, ct.POINTER(RECT), ct.c_double)
    def callback_func(hdc, lprcClip, lpfnEnum, dwData):
        #get_fields returns a list of monitor left, top, bottom coordinates
        new_monitor = Monitor(lpfnEnum.contents.get_fields())
        monitor_list.append(new_monitor)
        return True
    callback = monitor_enum_proc(callback_func)
    temp = user32.EnumDisplayMonitors(0, 0, callback , 0)
    return monitor_list

def get_curr_screen_geometry():
    screensize = user32.GetSystemMetrics(78), user32.GetSystemMetrics(79)
    return screensize

def get_monitor_num():
    #Code 80 for number of monitors SM_CMONITORS
    return user32.GetSystemMetrics(80)

def update_background(photo_path):
    #Code 20 for setting desktop background SPI_SETDESKWALLPAPER
    user32.SystemParametersInfoW(20, 0, photo_path, 1)

def main():
    # Get images
    h_imgs, v_imgs = get_images(PATH)
    h_index = 0
    v_index = 0
    # Get monitor list with screen size
    monitor_list = enum_display_monitors()
    screen = TotalScreen()
    for monitor in monitor_list:
        screen.update(monitor)
    # print(screen.left, screen.top, screen.right, screen.bottom, screen.width(), screen.height())
    # for i in monitor_list:
    #     print(i.left, i.right, i.top, i.bottom, i.horizontal)
    # print(get_curr_screen_geometry())
    # print((screen.width(), screen.height()))
    

    # Default 
    wallpaper = Image.new("RGB", (screen.width(), screen.height()), (92, 233, 92))
    for monitor in monitor_list:
        if monitor.horizontal:
            wallpaper.paste(h_imgs[h_index], )
            h_index = (h_index + 1)%len(h_imgs)
        else:
            wallpaper.paste(v_imgs[v_index])
            v_index = (v_index + 1)%len(v_imgs)

    wallpaper.save("wallpaper.jpg")
    
    
    

    

if __name__ == "__main__":
    main()