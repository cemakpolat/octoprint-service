import glob
import os

models_path = "../models"


def read_printable_models():
    #file_dir = os.path.dirname(os.path.realpath('__file__'))
    pfiles = []
    for file in glob.glob(models_path+"/*.gcode"):
        pfiles.append(file)
    return pfiles


def get_printable_models():
    files = os.listdir(models_path)
    flist = []
    for f in files:
        if not f.startswith(".") and f.endswith(".gcode"):
            flist.append(f.split(".gcode")[0])
    return flist