import os
import subprocess
import sys
import otio_extensions
from urllib.parse import quote
from PySide2.QtCore import Qt, QSize, QTimer
from PySide2.QtGui import QIcon, QPixmap
from PySide2.QtWidgets import QSizePolicy, QSpacerItem, QApplication, QFileDialog, QCheckBox, QWidget, QVBoxLayout, QHBoxLayout, QAbstractItemView, QPushButton, QLineEdit, QListWidget, QListWidgetItem, QMenu, QAction, QLabel, QDialog
from pathlib import Path



os.environ["PATH"] += os.pathsep + "C:/Users/Asus/ffmpeg-master-latest-win64-gpl/bin/"

class otio_export(QWidget):
    def __init__(self):
        super().__init__()

        main_layout = QVBoxLayout(self)
        self.resize(600, 450)
        top_layout = QHBoxLayout()
        mid_layout = QHBoxLayout()
        bottom_layout = QHBoxLayout()
        spacer = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)
        

        # cancel_btn = QPushButton("Cancel")
        export_btn = QPushButton("Export")
        export_btn.setFixedSize(50, 25)
        self.browse_btn = QPushButton("Select file")

        self.line_edit = QLineEdit()
        self.list_widget = QListWidget()
        self.list_widget.setDragDropMode(QListWidget.InternalMove)
        self.list_widget.setSelectionMode(QAbstractItemView.ExtendedSelection)

        # cancel_btn.clicked.connect(self.close)
        self.browse_btn.clicked.connect(self.get_file_path)
        export_btn.clicked.connect(self.export_trigger)
        
        settings_btn = QPushButton()
        settings_btn.setMenu(self.create_menu())
        settings_btn.setFixedSize(25, 23)
        settings_btn.setIcon(QIcon('C:\\Users\\Asus\\Desktop\\OTIO test - Copy\\settings-gear-svgrepo-com.png'))


        main_layout.addLayout(top_layout)
        top_layout.addWidget(self.line_edit)
        top_layout.addWidget(self.browse_btn)
        top_layout.addWidget(settings_btn)


        main_layout.addLayout(mid_layout)
        mid_layout.addWidget(self.list_widget)
        

        main_layout.addLayout(bottom_layout)
        # bottom_layout.addWidget(cancel_btn)
        bottom_layout.addSpacerItem(spacer)
        bottom_layout.addWidget(export_btn)

    # class HoverLabel(QLabel):
    #     def __init__(self, image_path, parent=None):
    #         super(otio_export.HoverLabel, self).__init__(parent)
    #         image_path = "C:\\Users\\Asus\\Desktop\\OTIO test - Copy\\settings-gear-svgrepo-com.png"
    #         self.setPixmap(QPixmap(image_path).scaled(30, 30, Qt.KeepAspectRatio))  # set the small image and scale it
    #         self.setToolTip('<img src="{}" width="30" height="30"/>'.format(image_path))  # set the large image as a tooltip and scale it
    #         self.setToolTipDuration(10000)  # tooltip duration in ms, -1 for indefinitely
    #         self.setFixedSize(30, 30)  # set the size of the widget

    #     def enterEvent(self, event):
    #         self.setAttribute(Qt.WA_AlwaysShowToolTips, True)

    #     def leaveEvent(self, event):
    #         self.setAttribute(Qt.WA_AlwaysShowToolTips, False)


    # class ImageListWidget(QListWidget):
    #     def __init__(self, images, parent=None):
    #         super(otio_export.ImageListWidget, self).__init__(parent)
    #         self.images = images

    #         for image_path in self.images:
    #             list_item = QListWidgetItem(self)
    #             item_widget = QWidget()
    #             layout = QHBoxLayout(item_widget)
    #             checkbox = QCheckBox()
    #             hover_label = otio_export.HoverLabel(image_path, item_widget)
    #             file_name = QLabel(image_path, item_widget)

    #             layout.addWidget(checkbox)
    #             layout.addWidget(hover_label)
    #             layout.addWidget(file_name)
    #             layout.addStretch()

    #             list_item.setSizeHint(item_widget.sizeHint())
    #             self.setItemWidget(list_item, item_widget)

    # class HoverItem(QListWidgetItem):
    #     def __init__(self, parent=None):
    #         super(otio_export.HoverItem, self).__init__(parent)

    #         self.setSizeHint(QSize(100, 30))  # Initial size
    #         self.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)

    #     def hoverEnterEvent(self, event):
    #         self.setSizeHint(QSize(100, 100))  # Hover size

    #     def hoverLeaveEvent(self, event):
    #         self.setSizeHint(QSize(100, 30))  # Original size

    # class ImageWidget(QWidget):
    #     def __init__(self, imagePath, parent=None):
    #         super().__init__(parent)
    #         self.imageLabel = QLabel(self)
    #         layout = QVBoxLayout(self)
    #         layout.addWidget(self.imageLabel)
    #         self.setLayout(layout)

    #         # Load image
    #         self.originalPixmap = QPixmap(imagePath)

    #         if self.originalPixmap.isNull():
    #             print(f"Failed to load image at {imagePath}")
    #             return

    #         # Scale image down for thumbnail
    #         self.thumbnailPixmap = self.originalPixmap.scaled(30, 30, Qt.KeepAspectRatio)

    #         self.imageLabel.setPixmap(self.thumbnailPixmap)
    #         self.imageLabel.setScaledContents(True)
    #         self.imageLabel.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)


    class ImageWidget(QWidget):
        def __init__(self, imagePath, parent=None):
            # imagePath = "C:\\Users\\Asus\\Desktop\\OTIO test - Copy\\settings-gear-svgrepo-com.png"
            super().__init__(parent)
            self.imageLabel = QLabel(self)
            layout = QVBoxLayout(self)
            layout.addWidget(self.imageLabel)
            self.setLayout(layout)
            # self.setToolTip('<img src="C:\\Users\\Asus\\Desktop\\OTIO test - Copy\\settings-gear-svgrepo-com.png" width="150" height="100"/>')
            # self.setIcon(QIcon("/path/to/image.png")) 
            self.setToolTip('<img src="{}" width="150" height="100"/>'.format(imagePath))

            # Load image
            self.originalPixmap = QPixmap(imagePath)

            if self.originalPixmap.isNull():
                print(f"Failed to load image at {imagePath}")
                return
            
            # Scale image down for thumbnail
            self.thumbnailPixmap = self.originalPixmap.scaled(30, 30, Qt.KeepAspectRatio)

            self.imageLabel.setPixmap(self.thumbnailPixmap)
            self.imageLabel.setScaledContents(True)
            self.imageLabel.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)

        def enterEvent(self, event):
            # When the mouse enters the widget, scale the image up
            self.imageLabel.setPixmap(self.originalPixmap)
            self.update()

        def leaveEvent(self, event):
            # When the mouse leaves the widget, scale the image back down
            self.imageLabel.setPixmap(self.thumbnailPixmap)
            self.update()

    from PySide2.QtCore import QSize

    class CheckableWidgetItem(QListWidgetItem):
        def __init__(self, text, full_file_path, list_widget):
            super().__init__(text)
            imagePath = full_file_path
            # imagePath = "C:\\Users\\Asus\\Desktop\\OTIO test - Copy\\settings-gear-svgrepo-com.png"
            
            self.list_widget = list_widget
            self.setFlags(self.flags() | Qt.ItemIsUserCheckable)
            self.setCheckState(Qt.Unchecked)
            self.setIcon(QIcon(imagePath)) 
            self.setToolTip('<img src="{}" width="150" height="100"/>'.format(imagePath))
            # self.setIcon(QIcon("C:\\Users\\Asus\\Desktop\\OTIO test - Copy\\settings-gear-svgrepo-com.png")) 
            # self.setToolTip('<img src="{}" width="150" height="100"/>'.format(imagePath))
        def setData(self, role, value):
            super().setData(role, value)
            if role == Qt.CheckStateRole:
                if value == Qt.Checked:
                    self.list_widget.setCurrentItem(self)
                else:
                    self.list_widget.setCurrentItem(None)

    # class CheckableWidgetItem(QListWidgetItem):
    #     def __init__(self, text, imagePath, list_widget):
    #         super().__init__(text)
    #         self.list_widget = list_widget
    #         self.setFlags(self.flags() | Qt.ItemIsUserCheckable)
    #         self.setCheckState(Qt.Unchecked)
            
    #         self.widget = otio_export.ImageWidget(imagePath)
    #         self.setSizeHint(QSize(self.widget.sizeHint().width(), 30)) # set the height to 30 pixels

    #         # self.setIcon(QIcon("C:\\Users\\Asus\\Desktop\\OTIO test - Copy\\settings-gear-svgrepo-com.png")) 

    #     def setData(self, role, value):
    #         super().setData(role, value)
    #         if role == Qt.CheckStateRole:
    #             if value == Qt.Checked:
    #                 self.list_widget.setCurrentItem(self)
    #             else:
    #                 self.list_widget.setCurrentItem(None)


    def export_trigger(self,):
        self.export_aaf(self.get_checked_file_paths())
    
    def image_to_mxf(self, input_image, output_mxf=None):
        # print(input_image, "MXF-ing")
        # print(os.path.basename(input_image).split(".")[0]+".mxf")
        # need a var 
        # print(os.getenv("HOMEm"),"home"*80)
        if not os.getenv("MXF_OUTPUT_PATH"):
            # output_folder = os.getenv("MXF_PATH"),"home"*80
            output_folder = f"{self.line_edit.text()}/MXF"
        else:
            output_folder = os.getenv("MXF_OUTPUT_PATH")
            print("can't ffind it lol")
        # print(output_folder,"%"*80)
        # output_folder = "C:/Users/Asus/Desktop/OTIO test/mxf_hold"

        basename = os.path.splitext(os.path.basename(input_image))[0]
        # print(basename,"basename"*10)
        os.makedirs(output_folder, exist_ok=True)

        # output_mxf = os.path.join(output_folder, f"{basename}.mxf")
        # print(output_mxf,"^"*80)
        # output_mxf = f"C:/Users/Asus/Desktop/OTIO TEST/mxf_hold/{os.path.basename(input_image).split('.')[0]+'.mxf'}"


        # if not os.path.exists(output_mxf):
        #     os.makedirs(output_mxf)

        # command = [
        #     "ffmpeg",
        #     "-loop", "1",
        #     "-i", input_image,
        #     "-c:v", "mpeg2video",
        #     "-t", "5",# add ui that allows custom values
        #     "-r", "24",
        #     "-pix_fmt", "yuv420p",
        #     output_mxf
        # ]

        # subprocess.run(command, check=True)
        # filename = input_image.split(".")[0]
        output = basename+".mxf"
        output_file = os.path.join(output_folder, output)
        # print(output_file,"what is that!!")
        # subprocess.run(["ffmpeg","-i", input_image, output])
        subprocess.run(["ffmpeg","-i", input_image, output_file],stdout=subprocess.DEVNULL)
        # subprocess.run(["ffmpeg","-i", input_image, output_mxf])
        # subprocess.run(["ffmpeg","-i", input_image, "-f", "mxf_opatom", output])
        # return output
        return output_file

    def find_mxf_file(self, image_file_name, folder_path=None):
        mxf_file_name = os.path.splitext(image_file_name)[0] + '.mxf'
        for root, _, files in os.walk(folder_path):
            for file in files:
                if file == mxf_file_name:
                    return os.path.join(root, file)
        return None

    def export_aaf(self, files):
        from opentimelineio import schema, opentime
        import opentimelineio as otio

        track = otio.schema.Track(kind="Video")

        for image_path in files:
            base_img_path = Path(image_path)
            # print(image_path.replace("\\", "/"), "HERE IS A FILE")
            image_path = self.image_to_mxf(image_path.replace("\\", "/"))
            # print(image_path, "WTFFFF")
            if not os.path.exists(image_path):
                print(f"File does not exist: {image_path}")
                continue

            clip_name = os.path.basename(image_path).split(".")[0]
            image_path = f"file:///{os.path.abspath(image_path)}"
            # print(image_path, "#-"*80)
            media_reference = schema.ExternalReference(target_url=image_path,
                                                    available_range=opentime.TimeRange(
                                                            start_time=opentime.RationalTime(value=0, rate=24),
                                                            duration=opentime.RationalTime(value=1, rate=24)
                                                        )
            )
            # print(media_reference, "media ref")
            source_range = opentime.TimeRange(
                start_time=opentime.RationalTime(value=0, rate=24),
                duration=opentime.RationalTime(value=48, rate=24)
            )

            clip = schema.Clip(name=clip_name, media_reference=media_reference, source_range=source_range)
            track.append(clip)

        timeline = otio.schema.Timeline()
        timeline.tracks.append(track)
        # change name of AAF to be the same as the parent DIR or ask Tom

        # print(os.path.dirname(base_img_path),"BIG-IMG"*80)
        if not os.getenv("AAF_OUTPUT_PATH"):

            AAF_file = Path(os.path.dirname(base_img_path)).name
            # print(AAF_file)
            AAF_folder = os.path.join(os.path.dirname(base_img_path),"AAF")
            # print(AAF_folder)

            os.makedirs(AAF_folder, exist_ok=True)
            # print(AAF_folder,"AAFFILE"*80)

            # AAF_output = os.path.join(os.path.dirname(base_img_path),"AAF")
            AAF_output = os.path.join(AAF_folder, AAF_file+".aaf")
        else:
            print("make env var AAF_output")
        # otio.adapters.write_to_file(timeline, "example.aaf", adapter_name="AAF",use_empty_mob_ids=True)
        otio.adapters.write_to_file(timeline, AAF_output, adapter_name="AAF",use_empty_mob_ids=True)
        
       
    
    def mxf_output_function(self,):
        directory = QFileDialog.getExistingDirectory(self, "Select Directory")
        if directory: 
            os.environ['MXF_OUTPUT_PATH'] = directory
            self.mxf_action.setToolTip(directory)
            

    def aaf_output_function(self,):
        directory = QFileDialog.getExistingDirectory(self, "Select Directory")
        if directory: 
            os.environ['AAF_OUTPUT_PATH'] = directory
            self.aaf_action.setToolTip(directory)
            

    def create_menu(self):
            menu = QMenu(self)

            self.mxf_action = QAction('set MXF output filepath', self)
            self.mxf_action.triggered.connect(self.mxf_output_function)
            menu.addAction(self.mxf_action)

            self.aaf_action = QAction('set AAF output filepath', self)
            self.aaf_action.triggered.connect(self.aaf_output_function)
            menu.addAction(self.aaf_action)

            return menu
    
    def get_checked_file_paths(self):
        base_path = self.line_edit.text()
        checked_item_names = []
        for i in range(self.list_widget.count()):
            item = self.list_widget.item(i)
            if item.checkState() == Qt.Checked:
                checked_item_names.append(item.text())
        file_paths = [os.path.normpath(os.path.join(base_path, name)) for name in checked_item_names]
        return file_paths

    def get_file_path(self,):
        
        file_path = QFileDialog.getExistingDirectory()
        if file_path:
            # print(file_path,"###")
            self.line_edit.setText(file_path)
            self.populate_file_view(file_path)

    def rename_file(self, item):
        old_file_path = item.data(Qt.UserRole)  # Assumes file path was stored in the UserRole data role
        new_file_name = item.text()  # The new name is the text of the item
        new_file_path = os.path.join(os.path.dirname(old_file_path), new_file_name)
        # print(item.toolTip())

        try:
            os.rename(old_file_path, new_file_path)
            item.setData(Qt.UserRole, new_file_path)  # Update the stored file path
            item.setToolTip('<img src="{}" width="150" height="100"/>'.format(new_file_path))
        except OSError as e:
            print(f"Error renaming file: {e}")

    def populate_file_view(self, file_path):
        all_files = []
        self.list_widget.clear()
        self.list_widget.itemChanged.connect(self.on_item_changed)
        for file in os.listdir(file_path):
            
            if file.endswith((".png", ".jpg", ".PNG", ".JPG", ".JPEG")):
                full_file_path = os.path.join(file_path, file)
                item = otio_export.CheckableWidgetItem(file, full_file_path, self.list_widget)
                item.setText(file)
                item.setData(Qt.UserRole, full_file_path)
                item.setFlags(item.flags() | Qt.ItemIsEditable)
                item.setCheckState(Qt.Checked)
                

                self.list_widget.addItem(item)
                # self.list_widget.setItemWidget(item, item.widget)

                if os.path.isfile(full_file_path):
                    all_files.append(full_file_path)
        self.list_widget.itemChanged.connect(self.rename_file)

        return all_files

    def on_item_changed(self, item):
        if item.checkState() == Qt.Checked:
            item.setSelected(True)
        else:
            item.setSelected(False)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = otio_export()
    ex.show()
    sys.exit(app.exec_())

