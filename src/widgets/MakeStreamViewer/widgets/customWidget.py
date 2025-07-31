from PyQt6.QtCore import *
from PyQt6.QtWidgets import * 
from PyQt6.QtGui import *
from PyQt6.QtMultimedia import *
from PyQt6.QtMultimediaWidgets import *


from src.core.GUI.UiManager import *

"""
Something to Override a Known widgte
"""
# class ChunkHolder(QListWidget):

#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("Chunk Holder")


"""
If you just need another window with complexlayout in the app
"""
# class ChunkInput(UiManager):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("Media Controls")