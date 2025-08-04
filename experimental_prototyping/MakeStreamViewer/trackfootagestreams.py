import sys
import subprocess
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QTextEdit

class FFProbeApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Select Video & Run ffprobe")
        self.resize(600, 400)

        layout = QVBoxLayout()

        self.btn = QPushButton("Select Video File")
        self.btn.clicked.connect(self.open_file_dialog)
        layout.addWidget(self.btn)

        self.output = QTextEdit()
        self.output.setReadOnly(True)
        layout.addWidget(self.output)

        self.setLayout(layout)

    def open_file_dialog(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Video File", "", "Video Files (*.mp4 *.mov *.mkv)")
        if file_path:
            self.run_ffprobe(file_path)

    def run_ffprobe(self, file_path):
        try:
            result = subprocess.run(
                ["ffprobe", "-v", "error", "-show_streams", file_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=True
            )
            self.output.setPlainText(result.stdout)
        except subprocess.CalledProcessError as e:
            self.output.setPlainText(f"ffprobe error:\n{e.stderr}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FFProbeApp()
    window.show()
    sys.exit(app.exec())

