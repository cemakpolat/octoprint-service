import glob


def read_printable_models():
    pfiles = []
    for file in glob.glob("*.txt"):
        pfiles.append(file)
    return pfiles
