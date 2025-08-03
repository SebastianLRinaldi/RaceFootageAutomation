from PyQt6.QtCore import QObject, pyqtSignal, QEvent, Qt

class EnterKeyHandler(QObject):
    enterPressed = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

    def eventFilter(self, obj, event):
        if event.type() == QEvent.Type.KeyPress and event.key() in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
            self.enterPressed.emit()
            return True  # stop further processing if needed
        return False
