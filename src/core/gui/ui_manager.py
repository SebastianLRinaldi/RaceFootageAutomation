from PyQt6.QtCore import *
from PyQt6.QtWidgets import * 
from PyQt6.QtGui import *

from typing import Literal

Orientation = Literal["horizontal", "vertical"]
LayoutType = Literal["group", "splitter", "tabs", "grid", "stacked"]

# class Component():
#     def __init__(self):
#         super().__init__()
#         self.layout = Layout()
#         self.logic = Logic(self.layout)
#         self.connection = Connections(self.layout, self.logic)


class UiManager(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("App UI")
        # self.resize(1000, 600)
        self.setup_stylesheets()
        self.widget_layout = None

    def build_layout(self, data) -> QWidget | QLayout:
        # if isinstance(data, str):
        #     return getattr(self, data)  # user widgets expected here
        if isinstance(data, QWidget):
            return data
        elif isinstance(data, str):
            return getattr(self, data)


        if isinstance(data, list):
            layout = QVBoxLayout()
            for item in data:
                w = self.build_layout(item)
                if isinstance(w, QWidget):
                    layout.addWidget(w)
                else:
                    layout.addLayout(w)
            return layout

        if isinstance(data, dict):
            if "group" in data:
                info = data["group"]
                orient = info.get("orientation", "vertical")
                children = info.get("children", [])

                layout = QVBoxLayout() if orient == "vertical" else QHBoxLayout()
                for item in children:
                    w = self.build_layout(item)
                    if isinstance(w, QWidget):
                        layout.addWidget(w)
                    else:
                        layout.addLayout(w)

                return layout

            if "box" in data:
                info = data["box"]
                title = info.get("title", "")
                orient = info.get("orientation", "vertical")
                children = info.get("children", [])
                
                groupbox = QGroupBox(title) 
                layout = QVBoxLayout() if orient == "vertical" else QHBoxLayout()
                for item in children:
                    w = self.build_layout(item)
                    if isinstance(w, QWidget):
                        layout.addWidget(w,  stretch=1)
                    else:
                        container = QWidget()
                        container.setLayout(w)
                        layout.addWidget(container, stretch=1)

                # layout.setContentsMargins(0, 0, 0, 0)
                # layout.setSpacing(0)
                # groupbox.setFlat(True)  # Optional: removes border if you want
                # groupbox.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

                groupbox.setLayout(layout)

                return groupbox

            if "splitter" in data:
                info = data["splitter"]
                orient = Qt.Orientation.Vertical if info.get("orientation") == "vertical" else Qt.Orientation.Horizontal
                splitter = QSplitter(orient)
                for item in info["children"]:
                    w = self.build_layout(item)
                    if isinstance(w, QWidget):
                        splitter.addWidget(w)
                    else:
                        container = QWidget()
                        container.setLayout(w)
                        splitter.addWidget(container)

                return splitter

            if "tabs" in data:
                info = data["tabs"]
                tab_labels = info.get("tab_labels", [])  # Expecting a list
                tabs = QTabWidget()
                for idx, item in enumerate(info["children"]):
                    w = self.build_layout(item)
                    if not isinstance(w, QWidget):
                        container = QWidget()
                        container.setLayout(w)
                        w = container
                    if tab_labels is not None:
                        title = tab_labels[idx] if idx < len(tab_labels) else f"Tab {idx + 1}"
                        tabs.addTab(w, title)


                return tabs

            if "grid" in data:
                info = data["grid"]
                layout = QGridLayout()
                children = info["children"]
                rows = info.get("rows", 1)
                cols = info.get("columns", len(children))
                for i, item in enumerate(children):
                    w = self.build_layout(item)
                    if isinstance(w, QWidget):
                        layout.addWidget(w, i // cols, i % cols)
                    else:
                        container = QWidget()
                        container.setLayout(w)
                        layout.addWidget(container, i // cols, i % cols)
                return layout

            if "stacked" in data:
                info = data["stacked"]
                layout = QStackedLayout()
                for item in info["children"]:
                    w = self.build_layout(item)
                    if isinstance(w, QWidget):
                        layout.addWidget(w)
                    else:
                        container = QWidget()
                        container.setLayout(w)
                        layout.addWidget(container)
                container = QWidget()
                container.setLayout(layout)
                return container


            if "form" in data:
                info = data["form"]
                layout = QFormLayout()
                for label, widget_name in info["children"]:
                    # widget = getattr(self, widget_name)
                    widget = self.build_layout(widget_name)
                    layout.addRow(label, widget)
                return layout


            if "scroll" in data:
                info = data["scroll"]
                child_spec = info["child"]
                w = self.build_layout(child_spec)

                scroll_area = QScrollArea()
                scroll_area.setFrameShape(QFrame.Shape.NoFrame)
                scroll_area.setWidgetResizable(True)

                if isinstance(w, QWidget):
                    scroll_area.setWidget(w)
                else:
                    container = QWidget()
                    container.setLayout(w)
                    scroll_area.setWidget(container)

                return scroll_area

        raise TypeError("Invalid layout data (Check for self.widgetName)")



    def apply_layout(self, layout_data):
        layout_or_widget = self.build_layout(layout_data)

        if isinstance(layout_or_widget, QWidget):
            # If it's already a widget with its own layout, set it as central widget
            self.setLayout(QVBoxLayout())  # force minimal root layout if needed
            self.layout().addWidget(layout_or_widget)
            # self.layout().setContentsMargins(0, 0, 0, 0)
            # self.layout().setSpacing(0)
        else:
            layout_or_widget.setContentsMargins(0, 0, 0, 0)
            # layout_or_widget.setSpacing(0)
            self.setLayout(layout_or_widget)
            

    def group(self, orientation: Orientation = None, children: list | None = None):
        return {
            "group": {
                "orientation": orientation,
                "children": children
            }
        }

    def box(self, orientation: Orientation = None, title: str | None = None,children: list | None = None):
        return {
            "box": {
                "title":title,
                "orientation": orientation,
                "children": children
            }
        }

    def splitter(self, orientation: Orientation = None, children: list | None = None):
        return {
            "splitter": {
                "orientation": orientation,
                "children": children
            }
        }

    def tabs(self, tab_labels: list = None, children: list | None = None):
        return {
            "tabs": {
                "tab_labels": tab_labels,
                "children": children
            }
        }

    def grid(self, children: list | None = None, rows=1, columns=None):
        return {
            "grid": {
                "children": children,
                "rows": rows,
                "columns": columns or len(children)
            }
        }

    def stacked(self, children: list | None = None):
        return {
            "stacked": {
                "children": children
            }
        }

    def form(self, children: list[tuple[str, str]]):
        return {
            "form": {
                "children": children
            }
        }

    def scroll(self, child):
        return {
            "scroll": {
                "child": child
            }
        }



    def show_window(self):
        self.show()

    def setup_stylesheets(self):

        self.setStyleSheet("""
            QMainWindow {
                background-color: #1a0d1c;
            }
            QLabel {
                background-color: #AAAAAA;
            }

        """)
    def print_margins_recursive(self, widget: QWidget):
        layout = widget.layout()
        if layout:
            margins = layout.contentsMargins()
            print(f"{widget.__class__.__name__} margins:", margins.left(), margins.top(), margins.right(), margins.bottom(), "spacing:", layout.spacing())
            for i in range(layout.count()):
                item = layout.itemAt(i)
                child = item.widget()
                if child:
                    self.print_margins_recursive(child)