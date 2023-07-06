import sys
from PySide2.QtWidgets import QApplication, QTabWidget, QVBoxLayout, QWidget, QPushButton, QFileDialog

import os
import sys
from PySide2.QtCore import Qt
from PySide2.QtWidgets import QApplication, QFileDialog, QWidget, QVBoxLayout, QHBoxLayout, QAbstractItemView, QPushButton, QLineEdit, QListWidget, QListWidgetItem

from opentimelineview.timeline_widget import Timeline
import opentimelineio as otio

import otio_export as oe

class TabExample(QWidget):
    def __init__(self):
        super().__init__()

        # Create a QTabWidget instance
        self.tabs = QTabWidget()

        layout = QVBoxLayout(self)
        layout.addWidget(self.tabs)

        self.otio_export_widget = oe.otio_export()

        # Initially, the timeline is empty
        self.otio_view_widget = Timeline(None)

        # Create a widget for the import tab
        self.import_tab = QWidget()
        self.import_layout = QVBoxLayout(self.import_tab)

        # Create a QLineEdit to display the selected filepath
        self.file_path_edit = QLineEdit()
        self.file_path_edit.setReadOnly(True)

        # Create a QHBoxLayout for the QLineEdit and the QPushButton
        self.file_select_layout = QHBoxLayout()
        self.file_select_layout.addWidget(self.file_path_edit)

        # Add a button to the import tab that opens a file dialog
        self.file_button = QPushButton("Select AAF file")
        self.file_button.clicked.connect(self.open_file_dialog)
        self.file_select_layout.addWidget(self.file_button)

        # Add the QHBoxLayout and the Timeline to the QVBoxLayout
        self.import_layout.addLayout(self.file_select_layout)
        self.import_layout.addWidget(self.otio_view_widget)

        self.tabs.addTab(self.otio_export_widget, "Export")
        self.tabs.addTab(self.import_tab, "Import")

        self.setLayout(layout)

        self.setWindowTitle("AAF Master")
        self.resize(600, 400)

    def open_file_dialog(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "", "AAF Files (*.aaf)", options=options)
        if file_name:
            self.load_timeline(file_name)

    def load_timeline(self, file_path):
        # Load the timeline from the AAF file
        timeline = otio.adapters.read_from_file(file_path)
        self.file_path_edit.setText(file_path)

        # Update the widget
        self.otio_view_widget.set_timeline(timeline)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TabExample()
    window.show()
    sys.exit(app.exec_())

# import sys
# from PySide2.QtWidgets import QApplication, QTabWidget, QVBoxLayout, QWidget, QPushButton, QFileDialog

# import os
# import sys
# from PySide2.QtCore import Qt
# from PySide2.QtWidgets import QApplication, QFileDialog, QWidget, QVBoxLayout, QHBoxLayout, QAbstractItemView, QPushButton, QLineEdit, QListWidget, QListWidgetItem

# from opentimelineview.timeline_widget import Timeline
# import opentimelineio as otio

# import otio_export as oe

# class TabExample(QWidget):
#     def __init__(self):
#         super().__init__()

#         # Create a QTabWidget instance
#         self.tabs = QTabWidget()

#         # Create tabs
#         self.tab1 = QWidget()
#         self.tab2 = QWidget()

#         layout = QVBoxLayout(self)
#         layout.addWidget(self.tabs)


#         self.otio_export_widget = oe.otio_export()

#         # Add a button to the export tab that opens a file dialog
#         self.file_button = QPushButton("Select AAF file", self.tab1)
#         self.file_button.clicked.connect(self.open_file_dialog)
#         self.otio_export_widget.layout().addWidget(self.file_button)

#         # Initially, the timeline is empty
#         self.otio_view_widget = Timeline(None)

#         self.tabs.addTab(self.otio_export_widget, "Export")
#         self.tabs.addTab(self.otio_view_widget, "Import")

#         self.setLayout(layout)

#         self.setWindowTitle("AAF Master")
#         self.resize(600, 400)

#     def open_file_dialog(self):
#         options = QFileDialog.Options()
#         file_name, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "", "AAF Files (*.aaf)", options=options)
#         if file_name:
#             self.load_timeline(file_name)

#     def load_timeline(self, file_path):
#         # Load the timeline from the AAF file
#         timeline = otio.adapters.read_from_file(file_path)

#         # Update the widget
#         self.otio_view_widget.set_timeline(timeline)

# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = TabExample()
#     window.show()
#     sys.exit(app.exec_())

# import sys
# from PySide2.QtWidgets import QApplication, QTabWidget, QVBoxLayout, QWidget

# import os
# import sys
# from PySide2.QtCore import Qt

# # from opentimelineview.console import TimelineWidget
# from opentimelineview.timeline_widget import Timeline


# import otio_export as oe

# class TabExample(QWidget):
#     def __init__(self):
#         super().__init__()

#         # Create a QTabWidget instance
#         self.tabs = QTabWidget()

#         # Create two tabs
#         self.tab2 = QWidget()

#         layout = QVBoxLayout(self)
#         layout.addWidget(self.tabs)


#         self.otio_export_widget = oe.otio_export()
#         self.otio_view_widget = Timeline()
#         self.tabs.addTab(self.otio_export_widget, "Export")
#         self.tabs.addTab(self.otio_view_widget, "Import")

#         self.setLayout(layout)

#         self.setWindowTitle("AAF Master")
#         self.resize(600, 400)

# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = TabExample()
#     window.show()
#     sys.exit(app.exec_())



