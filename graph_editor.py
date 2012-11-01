#-*-conding:utf-8 -*-
from Tkinter import Tk
import os
import json

from gui import MainWindow


root = Tk()
root.title("Graph Editor")
app = MainWindow(root)
root.mainloop()