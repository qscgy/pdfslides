#!/usr/bin/env python3
# Sam Ehrenstein (sie3@case.edu)

from itertools import cycle
import tkinter as tk
from wand.image import Image
from PIL import Image as Img
from PIL import ImageTk
from os.path import isdir, join
from os import getcwd, makedirs, listdir
import argparse

"""
This script can convert PDFs to images, and then display images in a looped slideshow.
"""


# Takes a list of PDF file names (must be in the same directory as this script)  and converts them to images.
# For each PDF name:
#   Precondition: There is no directory called images_<PDF name>, or this method has been called already
#   Postcondition: images_<PDF name> exists, and if it had to be created, it has an image for each page of the PDF
# Note that this method does not check if all files are in the directory, just that the directory exists.
def convert_pdfs(pdf_list):
    for pdf in pdf_list:
        if not isdir("images"):
            makedirs(join(getcwd(), 'images'))  # Make the images/ directory
        if not isdir(join(getcwd(), "images/%s" % pdf[:-4])):
            makedirs(join(getcwd(), "images/%s" % pdf[:-4]))
            im = Image(filename=pdf, resolution=300)
            for i, page in enumerate(im.sequence):
                with Image(page) as page_img:
                    page_img.alpha_channel = False
                    page_img.save(filename="images/%s/%d.png" % (pdf[:-4], i))


class App(tk.Tk):
    def __init__(self, image_files, delay):
        tk.Tk.__init__(self)
        root = tk.Tk()
        w_width = root.winfo_screenwidth()
        w_height = root.winfo_screenheight()
        maxsize = (w_width, w_height)
        # self.geometry('{0}x{0}+0+0'.format(root.winfo_screenwidth(), root.winfo_screenheight()))

        self.configure(background='black')
        self.geometry('+0+0')
        self.delay = delay
        pics_list = []
        for image in image_files:
            tmp = Img.open(image)
            # Rescale so that whichever image dimension needs more scaling gets the whole screen in that direction
            # In other words, maximize the size of the image while fitting on the screen
            scale = min(w_width/tmp.size[0], w_height/tmp.size[1])
            tmp = tmp.resize((int(tmp.size[0]*scale), int(tmp.size[1]*scale)), Img.ANTIALIAS)
            pics_list.append((ImageTk.PhotoImage(tmp), image))
        self.pictures = cycle(pics_list)
        self.picture_display = tk.Label(self)
        self.picture_display.pack()
        self.state = True
        # self.bind('<F11>', self.toggle_fullscreen)
        self.bind('<Control-R>', self.quit)

    def show_slides(self):
        img_object, image_name = next(self.pictures)
        self.picture_display.config(image=img_object)
        self.title(image_name)
        self.after(self.delay, self.show_slides)

    def run(self):
        self.mainloop()

    def toggle_fullscreen(self, event=None):
        self.state = not self.state
        self.attributes("-fullscreen", self.state)
        return "break"

    def end_fullscreen(self, event=None):
        self.state = False
        self.attributes("-fullscreen", False)
        return "break"

    def quit(self, event=None):
        self.destroy()


parser = argparse.ArgumentParser(description='Display a looping slideshow of images.')
parser.add_argument('--delay', '-d', type=int, default='1000', help='Delay between slides, in ms')
args = parser.parse_args()
delay = 1000
if args.delay:
    delay = args.delay

pdfs = [f for f in listdir(getcwd()) if f[-4:] == '.pdf']   # all .pdf files in cwd
convert_pdfs(pdfs)

# Collect all image files into a list. Page order within directories will be preserved.
image_files = []
for dir in sorted(listdir(join(getcwd(), 'images'))):
    # print(dir)
    tmp_images = []
    for file in listdir(join(getcwd(), 'images', dir)):
        number = int(file[:-4])     # get page number
        tmp_images.append((join(getcwd(), 'images', dir, file), number))      # add with the page number
        tmp_images = sorted(tmp_images, key=lambda img: img[1])     # sort by number
    image_files.extend([img[0] for img in tmp_images])  # add the images in order

app = App(image_files, delay)
app.attributes('-fullscreen', True)
app.show_slides()
app.run()
