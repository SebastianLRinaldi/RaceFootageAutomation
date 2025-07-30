# # from PyQt6.QtWidgets import (
# #     QApplication, QWidget, QMainWindow, QVBoxLayout, QHBoxLayout,
# #     QGroupBox, QScrollArea, QLabel, QPushButton, QLineEdit,
# #     QSpinBox, QFormLayout, QSizePolicy
# # )
# # import sys

# # class SettingsPanel(QWidget):
# #     def __init__(self):
# #         super().__init__()
# #         layout = QVBoxLayout()
# #         layout.setSpacing(20)

# #         for i in range(5):  # simulate multiple settings boxes
# #             box = QGroupBox(f"Settings Box {i + 1}")
# #             form = QFormLayout()
# #             form.addRow("Name:", QLineEdit())
# #             form.addRow("Value:", QSpinBox())
# #             box.setLayout(form)
# #             layout.addWidget(box)

# #         layout.addStretch()
# #         self.setLayout(layout)

# # class TestDashboard(QWidget):
# #     def __init__(self):
# #         super().__init__()
# #         layout = QVBoxLayout()
# #         layout.addWidget(QLabel("Dashboard Panel"))
# #         layout.addWidget(QPushButton("Start"))
# #         layout.addWidget(QPushButton("Stop"))
# #         layout.addWidget(QPushButton("Reset"))
# #         layout.addStretch()
# #         self.setLayout(layout)

# # class MainWindow(QMainWindow):
# #     def __init__(self):
# #         super().__init__()
# #         self.setWindowTitle("Settings + Dashboard")
# #         self.resize(900, 500)

# #         central = QWidget()
# #         hbox = QHBoxLayout(central)

# #         # Settings (Scrollable)
# #         scroll_area = QScrollArea()
# #         scroll_area.setWidgetResizable(True)
# #         settings_widget = SettingsPanel()
# #         scroll_area.setWidget(settings_widget)
# #         scroll_area.setMinimumWidth(300)

# #         # Dashboard
# #         dashboard = TestDashboard()
# #         dashboard.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

# #         # Add to layout
# #         hbox.addWidget(scroll_area)
# #         hbox.addWidget(dashboard)

# #         self.setCentralWidget(central)

# # if __name__ == "__main__":
# #     app = QApplication(sys.argv)
# #     win = MainWindow()
# #     win.show()
# #     sys.exit(app.exec())
# from PyQt6.QtWidgets import (
#     QApplication, QWidget, QMainWindow, QVBoxLayout, QHBoxLayout,
#     QGroupBox, QScrollArea, QLabel, QPushButton, QLineEdit,
#     QSpinBox, QFormLayout, QTabWidget, QTextEdit, QSizePolicy
# )
# import sys

# class SettingsPanel(QWidget):
#     def __init__(self):
#         super().__init__()
#         layout = QVBoxLayout()
#         layout.setSpacing(20)

#         for i in range(5):
#             box = QGroupBox(f"Settings Box {i + 1}")
#             form = QFormLayout()
#             form.addRow("Name:", QLineEdit())
#             form.addRow("Value:", QSpinBox())
#             box.setLayout(form)
#             layout.addWidget(box)

#         layout.addStretch()
#         self.setLayout(layout)

# class LogsPanel(QWidget):
#     def __init__(self):
#         super().__init__()
#         layout = QVBoxLayout()
#         log_output = QTextEdit()
#         log_output.setReadOnly(True)
#         log_output.setText("Log output goes here...")
#         layout.addWidget(log_output)
#         self.setLayout(layout)

# class TestDashboard(QWidget):
#     def __init__(self):
#         super().__init__()
#         layout = QVBoxLayout()
#         layout.addWidget(QLabel("Dashboard Panel"))
#         layout.addWidget(QPushButton("Start"))
#         layout.addWidget(QPushButton("Stop"))
#         layout.addWidget(QPushButton("Reset"))
#         layout.addStretch()
#         self.setLayout(layout)

# class MainWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("Settings + Dashboard + Logs")
#         self.resize(1000, 500)

#         central = QWidget()
#         hbox = QHBoxLayout(central)

#         # Tab widget with Settings and Logs
#         tabs = QTabWidget()
#         tabs.setMinimumWidth(350)

#         # Settings (inside scroll)
#         settings_scroll = QScrollArea()
#         settings_scroll.setWidgetResizable(True)
#         settings_scroll.setWidget(SettingsPanel())

#         # Logs
#         logs_widget = LogsPanel()

#         tabs.addTab(settings_scroll, "Settings")
#         tabs.addTab(logs_widget, "Logs")

#         # Dashboard on right
#         dashboard = TestDashboard()
#         dashboard.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

#         # Add widgets to main layout
#         hbox.addWidget(tabs)
#         hbox.addWidget(dashboard)

#         self.setCentralWidget(central)

# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     win = MainWindow()
#     win.show()
#     sys.exit(app.exec())



from typing import TypedDict, List, Union, Optional, Literal
from PyQt6.QtCore import *
from PyQt6.QtWidgets import * 
from PyQt6.QtGui import *
from PyQt6.QtCore import Qt
import sys

Orientation = Literal["horizontal", "vertical"]
LayoutType = Literal["group", "splitter", "tabs", "grid", "stacked", "box", "form", "scroll"]
WidgetSpec = Union[str, dict]

class GroupSpec(TypedDict, total=False):
    orientation: Orientation
    children: List[WidgetSpec]

class BoxSpec(GroupSpec, total=False):
    title: str

class SplitterSpec(TypedDict, total=False):
    orientation: Orientation
    children: List[WidgetSpec]

class TabsSpec(TypedDict, total=False):
    tab_labels: List[str]
    children: List[WidgetSpec]

class GridSpec(TypedDict, total=False):
    children: List[WidgetSpec]
    rows: int
    columns: int

class StackedSpec(TypedDict, total=False):
    children: List[WidgetSpec]

class FormSpec(TypedDict):
    children: List[tuple[str, str]]  # (label, widget_name)

class ScrollSpec(TypedDict):
    child: WidgetSpec

class UiManager(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TypedDict Layout Example")
        self.widget1 = QLabel("Widget 1")
        self.widget2 = QLabel("Widget 2")
        self.widget3 = QLabel("Widget 3")

    def build_layout(self, data: Union[dict, str, list]) -> QWidget | QLayout:
        if isinstance(data, str):
            return getattr(self, data)

        if isinstance(data, list):
            layout = QVBoxLayout()
            for item in data:
                w = self.build_layout(item)
                if isinstance(w, QWidget):
                    layout.addWidget(w)
                else:
                    container = QWidget()
                    container.setLayout(w)
                    layout.addWidget(container)
            return layout

        if isinstance(data, dict):
            if "group" in data:
                info: GroupSpec = data["group"]
                return self.build("group", **info)
            if "box" in data:
                info: BoxSpec = data["box"]
                return self.build("box", **info)
            if "splitter" in data:
                info: SplitterSpec = data["splitter"]
                return self.build("splitter", **info)
            if "tabs" in data:
                info: TabsSpec = data["tabs"]
                return self.build("tabs", **info)
            if "grid" in data:
                info: GridSpec = data["grid"]
                return self.build("grid", **info)
            if "stacked" in data:
                info: StackedSpec = data["stacked"]
                return self.build("stacked", **info)
            if "form" in data:
                info: FormSpec = data["form"]
                return self.build("form", **info)
            if "scroll" in data:
                info: ScrollSpec = data["scroll"]
                return self.build("scroll", **info)

        raise TypeError("Invalid layout data")

    def build(self, layout_type: LayoutType, *,
              orientation: Orientation = "vertical",
              title: str = "",
              children: List[WidgetSpec] = None,
              tab_labels: List[str] = None,
              rows: int = 1,
              columns: int = 0,
              child: WidgetSpec = None,
              form_children: List[tuple[str, str]] = None) -> QWidget | QLayout:

        children = children or []
        tab_labels = tab_labels or []
        form_children = form_children or []

        is_vert = orientation == "vertical"
        LayoutCls = QVBoxLayout if is_vert else QHBoxLayout

        if layout_type == "group":
            layout = LayoutCls()
            for item in children:
                w = self.build_layout(item)
                if isinstance(w, QWidget):
                    layout.addWidget(w)
                else:
                    container = QWidget()
                    container.setLayout(w)
                    layout.addWidget(container)
            return layout

        if layout_type == "box":
            layout = LayoutCls()
            for item in children:
                w = self.build_layout(item)
                if isinstance(w, QWidget):
                    layout.addWidget(w)
                else:
                    container = QWidget()
                    container.setLayout(w)
                    layout.addWidget(container)
            group = QGroupBox(title)
            group.setLayout(layout)
            return group

        if layout_type == "splitter":
            qt_orient = Qt.Orientation.Vertical if is_vert else Qt.Orientation.Horizontal
            splitter = QSplitter(qt_orient)
            for item in children:
                w = self.build_layout(item)
                if isinstance(w, QWidget):
                    splitter.addWidget(w)
                else:
                    container = QWidget()
                    container.setLayout(w)
                    splitter.addWidget(container)
            return splitter

        if layout_type == "tabs":
            tabs = QTabWidget()
            for idx, item in enumerate(children):
                w = self.build_layout(item)
                if not isinstance(w, QWidget):
                    container = QWidget()
                    container.setLayout(w)
                    w = container
                label = tab_labels[idx] if idx < len(tab_labels) else f"Tab {idx+1}"
                tabs.addTab(w, label)
            return tabs

        if layout_type == "grid":
            layout = QGridLayout()
            columns = columns or max(1, len(children))
            for i, item in enumerate(children):
                w = self.build_layout(item)
                if not isinstance(w, QWidget):
                    container = QWidget()
                    container.setLayout(w)
                    w = container
                layout.addWidget(w, i // columns, i % columns)
            return layout

        if layout_type == "stacked":
            layout = QStackedLayout()
            for item in children:
                w = self.build_layout(item)
                if not isinstance(w, QWidget):
                    container = QWidget()
                    container.setLayout(w)
                    w = container
                layout.addWidget(w)
            container = QWidget()
            container.setLayout(layout)
            return container

        if layout_type == "form":
            layout = QFormLayout()
            for label, widget_name in form_children:
                widget = getattr(self, widget_name)
                layout.addRow(label, widget)
            return layout

        if layout_type == "scroll":
            scroll_area = QScrollArea()
            scroll_area.setWidgetResizable(True)
            w = self.build_layout(child)
            if not isinstance(w, QWidget):
                container = QWidget()
                container.setLayout(w)
                w = container
            scroll_area.setWidget(w)
            return scroll_area

        raise ValueError(f"Unknown layout type: {layout_type}")

    def apply_layout(self, layout_data):
        root = self.build_layout(layout_data)
        if isinstance(root, QWidget):
            self.setLayout(QVBoxLayout())
            self.layout().addWidget(root)
        else:
            self.setLayout(root)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = UiManager()

    # Autocomplete-friendly layout spec using TypedDicts
    tabs_layout: TabsSpec = {
        
    }

    box_layout: BoxSpec = {
        "title": "My Group Box",
        "orientation": "vertical",
        "children": [
            "widget3",
            {"tabs": tabs_layout}
        ]
    }

    layout_data = {"box": box_layout}

    ui.apply_layout(layout_data)
    ui.resize(400, 300)
    ui.show()
    sys.exit(app.exec())
