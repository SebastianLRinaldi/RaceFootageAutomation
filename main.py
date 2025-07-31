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
import sys
import os

# os.environ['QTWEBENGINE_CHROMIUM_FLAGS'] = '--use-gl=angle --gpu --gpu-launcher --in-process-gpu --ignore-gpu-blacklist --ignore-gpu-blocklist'

# Add the root directory of your project to the sys.path
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from src.core.Connect.AppConnector import *


import importlib
import os

from src.core.GUI import UiManager

def load_apps():
    base_path = "src.apps"
    app_dir = os.path.join(os.path.dirname(__file__), "src", "apps")
    pages = []

    for name in os.listdir(app_dir):
        app_path = os.path.join(app_dir, name)
        if not os.path.isdir(app_path):
            continue
        if name.startswith("__") or name.lower() == "widgets":
            continue

        try:
            layout_mod = importlib.import_module(f"{base_path}.{name}.Layout")
            logic_mod = importlib.import_module(f"{base_path}.{name}.Functions")
            conn_mod = importlib.import_module(f"{base_path}.{name}.Connections")
        except ModuleNotFoundError as e:
            print(f"[WARNING] Missing module for {name}: {e}")
            continue

        try:
            layout_cls = getattr(layout_mod, "Layout")
            logic_cls = getattr(logic_mod, "Logic")
            conn_cls = getattr(conn_mod, "Connections")
        except AttributeError as e:
            print(f"[WARNING] Missing class for {name}: {e}")
            continue

        pages.append((name, layout_cls, logic_cls, conn_cls))

    if not pages:
        print("[ERROR] No valid apps found in src/apps")

    return pages

    
class Dashboard(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("UI")
        self.resize(800, 480)
        self.setup_stylesheets()

        self.stack = QStackedWidget()
        self.apps = {}
        self.logic = {}
        self.page_controllers = {}

        # Load your app pages (layout, logic, controller classes)
        pages = load_apps()

        for name, layout_class, logic_class, controller_class in pages:
            widget = layout_class()

            scroll_area = QScrollArea()
            scroll_area.setFrameShape(QFrame.Shape.NoFrame)
            scroll_area.setWidgetResizable(True)
            scroll_area.setWidget(widget)

            self.stack.addWidget(scroll_area)
            self.apps[name] = widget
            self.logic[name] = logic_class(widget)
            self.page_controllers[name] = controller_class(widget, self.logic[name])

        self.controller = AppConnector(self.apps, self.logic)

        # Menu bar
        menubar = QMenuBar(self)
        app_menu = menubar.addMenu("Apps")

        for name in self.apps:
            action = QAction(name.capitalize(), self)
            action.triggered.connect(lambda _, n=name: self.switch_to(n))
            app_menu.addAction(action)

        self.setMenuBar(menubar)

        # Layout
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.addWidget(self.stack)
        self.setCentralWidget(container)

        self.switch_to("ProjectBaseScreen")

    def switch_to(self, app_name):
        try:
            # Find the scroll area that contains the widget
            for i in range(self.stack.count()):
                scroll_area = self.stack.widget(i)
                if scroll_area.widget() == self.apps[app_name]:
                    self.stack.setCurrentIndex(i)
                    break
        except KeyError:
            print(f"Invalid app name: {app_name}")
            print("Valid app names are:", list(self.apps.keys()))

    def setup_stylesheets(self):
        self.setStyleSheet(""" """)






# ----- Entry Point -----
if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Dashboard()
    win.show()
    sys.exit(app.exec())
