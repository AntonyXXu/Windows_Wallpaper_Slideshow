#########################################################
#   Module to move photos into horizontal and vertical
#   folders from the photos folder
#   Returns an array of horizontal or vertical images
#
#   Initially I had thought to check the sizes
#   whenever the script is run, but sorting it by size 
#   is much more efficient. 
#########################################################
import os
import shutil
from PIL import Image

def filter_jpg(array):
    return [image for image in array if image.lower().endswith(".jpg")]

def get_images(path):
    #initialize image list with vertical and horizontal photos
    img_dir = path + "\\photos"

    #create horizontal and vertical image folders
    files = os.listdir(img_dir)
    files = filter_jpg(files)
    try:
        os.mkdir(img_dir+"\\horizontal")
    except OSError as error:
        print(error)
    try:
        os.mkdir(img_dir+"\\vertical")
    except OSError as error:
        print(error)

    #move photos to their appropriate directories
    for photo in files:
        image = Image.open(img_dir + "\\"+ photo)
        if image.size[0] >= image.size[1]:
            image.close()
            shutil.move(img_dir+"\\"+ photo, img_dir+"\\horizontal")
        else:
            image.close()
            shutil.move(img_dir+"\\"+photo, img_dir + "\\vertical")
    
    #create a list of vertical and horizontal images
    hori_path = img_dir+"\\horizontal"
    hori_imgs = os.listdir(hori_path)
    vert_path = img_dir+"\\vertical"
    vert_imgs = os.listdir(vert_path)
    return [filter_jpg(hori_imgs), filter_jpg(vert_imgs)]


