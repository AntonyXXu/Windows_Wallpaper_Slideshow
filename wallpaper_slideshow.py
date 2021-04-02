import time
import os
import ctypes as ct
import shutil
from PIL import Image
from img_functions.img_manager import get_images, resize_img

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

# Monitor class
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

# Screen class for sum of multiple monitors
class TotalScreen(Monitor):
    def __init__(self, monitor = [0,0,0,0]):
        super().__init__(monitor)
    def update(self, new_monitor):
        self.left = min(new_monitor.left, self.left)
        self.top = min(new_monitor.top, self.top)
        self.right = max(new_monitor.right, self.right)
        self.bottom = max(new_monitor.bottom, self.bottom)    

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

def update_monitor_list():
    monitor_list = enum_display_monitors()
    screen = TotalScreen()
    for monitor in monitor_list:
        screen.update(monitor)
    return monitor_list, screen

def get_curr_screen_geometry():
    screensize = user32.GetSystemMetrics(78), user32.GetSystemMetrics(79)
    return screensize

def get_monitor_num():
    #Code 80 for number of monitors SM_CMONITORS
    return user32.GetSystemMetrics(80)

def check_folder_time(old_time, path):
    new_time = [
        os.stat(path+"\\photos").st_mtime,
        os.stat(path+"\\photos\\horizontal").st_mtime,
        os.stat(path+"\\photos\\vertical").st_mtime
    ]
    if old_time != new_time:
        for i in range(len(old_time)):
            old_time[i] = new_time[i]
        return False
    else:
        return True

def update_background(photo_path):
    #Code 20 for setting desktop background SPI_SETDESKWALLPAPER
    user32.SystemParametersInfoW(20, 0, photo_path, 1)

def main():
    h_index = 0
    v_index = 0
    last_update = [0, 0, 0]
    # Get images, update folder time
    h_imgs, v_imgs = get_images(PATH)
    check_folder_time(last_update, PATH)
    # Get monitor list with screen size
    monitor_list, screen = update_monitor_list()


    
    while True:
        # Check total number of monitors and screen resolution. 
        # If it has changed, update monitor_list and screen instances
        if len(monitor_list) != get_monitor_num() or (screen.width(), screen.height()) != get_curr_screen_geometry():
            monitor_list, screen = update_monitor_list()

        # Check if new photos were added in photos directory based on modified by stamp
        if not check_folder_time(last_update, PATH):
            h_imgs, v_imgs = get_images(PATH)
            h_index = 0
            v_index = 0
                    
        # Create wallpaper of images and save
        wallpaper = Image.new("RGB", (screen.width(), screen.height()), (92, 233, 92))
        for monitor in monitor_list:
            if monitor.horizontal:
                if not h_imgs:
                    print("Error - No horizontal images in photos folder")
                    return
                resized_img = resize_img(h_imgs[h_index], monitor, PATH)
                h_index = (h_index + 1) % len(h_imgs)
            else:
                if not v_imgs:
                    print("Error - No vertical images in photos folder")
                    return
                resized_img = resize_img(v_imgs[v_index], monitor, PATH)
                v_index = (v_index + 1) % len(v_imgs)
            # Screen coordinates can be negative, paste images based on relative position
            wallpaper.paste(resized_img, (
                monitor.left - screen.left, 
                monitor.top - screen.top
                ))
        wallpaper.save("wallpaper.jpg")

        update_background(PATH+"\\wallpaper.jpg")

        time.sleep(TIMER_MIN*60)

if __name__ == "__main__":
    main()