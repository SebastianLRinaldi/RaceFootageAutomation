"""
pyqt6 - v. 6.7 (G) || 6.9 (G)
pyqt6-webengine - v. 6.7 (G)
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

from application.FrontEnd.E_combiner.PageController import *
from application.apps.mediaView.mediaViewConnections import MediaViewConnections
from application.apps.raceStats.raceStatsConnections import RaceStatsConnections
from application.apps.myThirdWindow.myThirdPageConnections import ThirdPageConnections

class Dashboard(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("UI")
        self.resize(1571, 731)

        self.stack = QStackedWidget()

        # Your dynamic page creation
        # Define pages with: name, UI class, Logic class, Controller class
        pages = [
            ("first", MediaViewLayout, MediaViewLogic, MediaViewConnections),
            ("second", RaceStatsLayout, RaceStatsLogic, RaceStatsConnections),
            ("third", My_Third_Page, ThirdPageLogic, ThirdPageConnections),
        ]

        # Step 1: Create UIs
        self.apps = {name: page_class() for name, page_class, *_ in pages}

        # Step 2: Create Logic
        self.logic = {name: logic_class(self.apps[name]) for name, _, logic_class, _ in pages}

        # Step 3: Create Per-Page Controllers
        self.page_controllers = {
            name: controller_class(self.apps[name], self.logic[name])
            for name, _, _, controller_class in pages
        }

        # Add pages to the stack
        for page in self.apps.values():
            self.stack.addWidget(page)

        # Create the controller
        self.controller = PageController(self.logic)


        menubar = QMenuBar(self)
        app_menu = menubar.addMenu("Apps")

        for name in self.apps:
            action = QAction(name.capitalize(), self)
            action.triggered.connect(lambda _, n=name: self.switch_to(n))
            app_menu.addAction(action)

        self.setMenuBar(menubar)

        # Main container setup
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.addWidget(self.stack)
        self.setCentralWidget(container)

        self.switch_to("second")

    def switch_to(self, app_name):
        self.stack.setCurrentWidget(self.apps[app_name])


# ----- Entry Point -----
if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Dashboard()
    win.show()
    sys.exit(app.exec())
