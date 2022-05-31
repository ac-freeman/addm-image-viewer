# This is a sample Python script.

# Press Ctrl+F5 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import sys
import struct
from tkinter import *

import numpy as np
from PIL import ImageTk, Image

def show_image(filename):
    # Use a breakpoint in the code line below to debug your script.
    data = open(filename, "rb").read()

    (height, width, depth) = struct.unpack("<III", data[0:12])

    root = Tk()
    root.title("Image Viewer")
    root.geometry("700x700")

    # TODO: embed this in file header
    ref_time = 5000
    max_intensity = 255

    if depth == 1:
        image_arr = np.empty((height, width))
        dt_arr = np.empty((height, width))
    else:
        image_arr = np.empty((height, width, depth))
        dt_arr = np.empty((height, width, depth))
    data_idx = 12

    for idy, y in enumerate(image_arr):
        for idx, x in enumerate(y):
            if depth == 1:
                (d, delta_t) = struct.unpack("<II", data[data_idx:data_idx + 8])
                d = d & 0x000000FF
                y[idx] = ((1 << d) / max_intensity) * (ref_time / delta_t) * 255
                dt_arr[idy][idx] = delta_t
                data_idx = data_idx + 8

            else:
                # Color ADDER images are in BGR arrangement, but PIL doesn't support that cleanly
                (d, delta_t) = struct.unpack("<II", data[data_idx:data_idx + 8])
                d = d & 0x000000FF
                x[2] = ((1 << d) / max_intensity) * (ref_time / delta_t) * 255
                data_idx = data_idx + 8
                (d, delta_t) = struct.unpack("<II", data[data_idx:data_idx + 8])
                d = d & 0x000000FF
                x[1] = ((1 << d) / max_intensity) * (ref_time / delta_t) * 255
                data_idx = data_idx + 8
                (d, delta_t) = struct.unpack("<II", data[data_idx:data_idx + 8])
                d = d & 0x000000FF
                x[0] = ((1 << d) / max_intensity) * (ref_time / delta_t) * 255
                data_idx = data_idx + 8
            # x[1] = x[2]
            # x[0] = x[2]

    if depth == 1:
        im = Image.fromarray(np.uint8(image_arr), mode="L")
    else: 
        im = Image.fromarray(np.uint8(image_arr), mode="RGB")
    im.show()

    ## For showing the inverse delta_t image
    # dt_r_max = np.max(dt_arr[:, :])
    # dt_r = (1 - (dt_arr[:, :] / dt_r_max)) * 255
    # norm_dt = Image.fromarray(np.uint8(dt_r), mode="L")
    # norm_dt.show()



    print("done")

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    filename = sys.argv[1]
    show_image(filename)

