# Windows_Wallpaper_Slideshow

Windows screens do not support background image cycling for multiple monitors, this python program allows for a background slideshow. \
It first detects monitor sizes and total screen size, then creates a new image equal to the total screen size with individual resized images pasted into the new background image \
Slideshow changes on timer, and also checks if screen resolution, monitor number, or photos have changed. Photo changes are tested with os.stat(path).st_mtime to avoid querying the entire folder. \
Note vertical screens in parallel with horizontal screen setups do not work. \

Requirements:
Python Image Library (install via "pip install Pillow")

Considerations:
Stacks were considered for the list of photos to pop into the wallpaper, but may be inefficient when all photos are cycled through and it would have to be repopulated. Arrays were ultimately selected for ease of use, with an index to move through each photo, where photos are resized as they get inserted into the background image (resizing all the photos for the monitors isn't space efficient) \
I initially wanted to put all of the images in the photos folder, but realized the images had to be processed each time to check if they are horizontal or vertical on initialization. Instead, it would be faster to sort them on start into separate folders and avoid some repeated work \
Coordinates are based on the main monitor location, so it caused some issues for creating the wallpaper. \
