from pathlib import Path
from tkinter import filedialog, Tk


# Init tkinter browser
ROOT_TK = Tk()

# Ensure the tkinter main window is hidden
ROOT_TK.withdraw()

# Ensure that the file browser will appear in front on Windows
ROOT_TK.wm_attributes("-topmost", 1)

LAST_DIRECTORY = None


def open_file(title=None, initial_dir=None):

    if initial_dir is None:
        # Default to the last directory
        initial_dir = LAST_DIRECTORY

    if initial_dir is None:
        # default to the user's home directory
        initial_dir = Path.home()

    kwargs = {
        "title": title,
        "initialdir": initial_dir,
    }
    return filedialog.askopenfile(**kwargs)
