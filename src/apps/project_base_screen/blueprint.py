from PyQt6.QtCore import *
from PyQt6.QtWidgets import * 
from PyQt6.QtGui import *

from src.components import *

class Blueprint:
    project_list: QListWidget
    open_project_btn: QPushButton
    new_project_btn: QPushButton

    directory_search: PathInputWidget

    project_tree: QTreeView

    def _map_widgets(self, source):
        """
        Copy existing widget instances from source to self.
        """
        # source is some object that already has the widgets as attributes
        for name in self.__annotations__:
            setattr(self, name, getattr(source, name))

    def _init_widgets(self):
        """
        Instantiate all widgets defined in type hints.
        Call this manually when you want actual widget instances.
        """
        for name, typ in self.__annotations__.items():
            try:
                setattr(self, name, typ())
            except Exception as e:
                # exc_file = e.__traceback__.tb_frame.f_code.co_filename
                # exc_line = e.__traceback__.tb_lineno
                raise RuntimeError(
                    f"{name} | {typ} failed to load: \n"
                    # f'  File "{exc_file}", line {exc_line}\n'
                    f'{e}'
                ) from None
                