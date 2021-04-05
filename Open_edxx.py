import tkinter as tk
from tkinter import filedialog
import tkfilebrowser as tkfb
import os
import sys
# sys.coinit_flags = 2  # COINIT_APARTMENTTHREADED

def open_edxx_file():
    root = tk.Tk()
    root.withdraw()
    file_name_edxx = filedialog.askopenfilename(filetypes=[("Edxx files", ".edxx")], multiple=False)
    # directory_edxx = os.path.split(file)[0]
    # file_name_edxx = os.path.split(file)[1]
    # file_name_edxx = file_name_edxx.replace("edxx", "dcm")
    # return directory_edxx, file_name_edxx
    return file_name_edxx


def open_file_in_folder():
    tempdir = ""
    root = tk.Tk()
    root.withdraw()
    # tempdir = tkfb.askopendirname(initialdir="C:\\", title='Please select a directory')
    tempdir = filedialog.askdirectory(parent=root, initialdir="C:\\", title='Please select a directory')
    if tempdir == "":
        tempdir = "C:\\"
    file_names_edxx = list()
    for file in os.listdir(tempdir):
        if file.endswith(".edxx"):
            file_names_edxx.append(os.path.join(tempdir, file))
    return file_names_edxx