import sys
import os
import subprocess
from PySide2.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QFileDialog


class OTIOViewer(QWidget):
    def __init__(self):
        super(OTIOViewer, self).__init__()

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.file_label = QLabel("No file selected")
        layout.addWidget(self.file_label)

        open_button = QPushButton("Select File")
        open_button.clicked.connect(self.open_file_dialog)
        layout.addWidget(open_button)

        export_button = QPushButton("Open File")
        export_button.clicked.connect(self.export_file)
        layout.addWidget(export_button)

        self.setLayout(layout)

    def open_file_dialog(self):
        options = QFileDialog.Options()
        print(options,"1")
        options |= QFileDialog.ReadOnly
        print(options,"2")
        file_name, _ = QFileDialog.getOpenFileName(self, "Open a file", "", "All Files (*)", options=options)
        if file_name:
            self.file_label.setText(file_name)
    def export_file(self):
        if self.file_label.text() != "No file selected":
            # command = ["python", "opentimelineview/console.py", self.file_label.text()]
            command = ["python", "opentimelineview/example_console.py", os.path.basename(self.file_label.text())]
            subprocess.run(command, check=True)
        else:
            print("No file selected")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = OTIOViewer()
    window.show()
    sys.exit(app.exec_())