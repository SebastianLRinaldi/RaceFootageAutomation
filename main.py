"""
pyqt6 - v. 6.7 (G) || 6.9 (G)
pyqt6-webengine - v. 6.7 (G)
PyQt6-WebEngine==6.7
"""
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtPrintSupport import *
from PyQt6.QtWebEngineWidgets import *
from PyQt6.QtWebEngineCore import *

import importlib
import pkgutil
from pathlib import Path

import sys
import os

# os.environ['QTWEBENGINE_CHROMIUM_FLAGS'] = '--use-gl=angle --gpu --gpu-launcher --in-process-gpu --ignore-gpu-blacklist --ignore-gpu-blocklist'

# Add the root directory of your project to the sys.path
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from src.core.connect.app_connector import *


def load_apps():
    base = "src.apps"
    path = os.path.join(os.path.dirname(__file__), "src", "apps")
    widgets = {}

    for name in os.listdir(path):
        if name.startswith("__") or name.lower() == "widgets":
            continue

        full_path = os.path.join(path, name)
        if not os.path.isdir(full_path):
            continue

        try:
            comp = importlib.import_module(f"{base}.{name}").Component()
            for attr in comp.__class__.__annotations__:
                if not hasattr(comp, attr):
                    raise AttributeError(f"{base}.{name}.Component missing '{attr}'")
            widgets[name] = comp
        except Exception as e:
            raise RuntimeError(f"Error in {base}.{name}: {e}")

    return widgets




class Dashboard(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Widget Dashboard")
        self.resize(800, 600)

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        self.apps = load_apps()

        for name, widget in self.apps.items():
            self.stack.addWidget(widget.layout)

        self.setup_menu()

        self.controller = AppConnector(self, self.apps)

        self.switch_to("project_base_screen")

    def setup_menu(self):
        menubar = QMenuBar(self)
        app_menu = menubar.addMenu("Apps")

        for name in self.apps:
            action = QAction(name.capitalize(), self)
            action.triggered.connect(lambda _, n=name: self.switch_to(n))
            app_menu.addAction(action)

        self.setMenuBar(menubar)

    def switch_to(self, app_name):
        widget = self.apps.get(app_name)
        if widget:
            self.stack.setCurrentWidget(widget.layout)
        else:
            print(f"Invalid app name: {app_name}")
            print("Valid apps:", list(self.apps.keys()))

    def setup_stylesheets(self):
        self.setStyleSheet(""" """)

# ----- Entry Point -----
if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Dashboard()
    win.show()
    sys.exit(app.exec())
