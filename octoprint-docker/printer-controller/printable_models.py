import glob
import os


def read_printable_models():
    pfiles = []
    for file in glob.glob("../models/*.gcode"):
        pfiles.append(file)
    return pfiles


def get_printable_models():
    print(" get models")
    files = os.listdir("../models/")
    flist = []
    for f in files:
        if f.startswith(".") is False and f.endswith(".gcode"):
            flist.append(f)
    return flist