from PyQt6.QtCore import pyqtSignal, Qt, QEvent, QObject

class DeleteKeyHandler(QObject):
    deletePressed = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

    def eventFilter(self, obj, event):
        if event.type() == QEvent.Type.KeyPress and event.key() == Qt.Key.Key_Delete:
            self.deletePressed.emit()
            return True
        return False