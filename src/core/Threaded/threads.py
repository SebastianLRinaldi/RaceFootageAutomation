import requests
import re
import html
import random

from PyQt6.QtCore import *
from PyQt6.QtWidgets import * 
from PyQt6.QtGui import *



class Fetcher(QObject):
    finished = pyqtSignal(object)  # emit whatever the function returns

    def __init__(self, func, *args, **kwargs):
        super().__init__()
        self.func = func
        self.args = args
        self.kwargs = kwargs

    def run(self):
        result = self.func(*self.args, **self.kwargs)
        self.finished.emit(result)


def fetch_then_give(self, func, callback):
    thread = QThread()
    fetcher = Fetcher(func)
    fetcher.moveToThread(thread)

    def cleanup():
        fetcher.deleteLater()
        thread.deleteLater()
        self._threads.remove((thread, fetcher))

    thread.started.connect(fetcher.run)
    fetcher.finished.connect(callback)
    fetcher.finished.connect(thread.quit)
    thread.finished.connect(cleanup)

    if not hasattr(self, '_threads'):
        self._threads = []
    self._threads.append((thread, fetcher))

    thread.start()


"""
Might also need a thing where we need to wait for multiple slow process 
    then send results once all are done, 
        so multiple funcs to 1 call back once they all finish
"""
def update_nouns_random(self):
    pass
    # arg 1 is slow function we wait for, arg 2 is function that needs to wait for slow function
    # self.fetch_then_give(self.get_nouns, self.set_random_nouns)