# mainwindow.py
from PyQt5.QtWidgets import QMainWindow, QLabel, QPushButton, QHBoxLayout, QVBoxLayout, QFileDialog, QWidget
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from Components.notepad import NotepadWindow
from Components.imageClassifier import ClassifierWindow
from Components.calculator import CalculatorWindow
from Components.imageCompress import ImageCompressorWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Window setup
        self.setWindowTitle("Multi-App Frame")
        self.setGeometry(300, 300, 750, 250)
        self.setStyleSheet("background-color: #FFEBEE;")

        # Icons setup
        self.setup_icons()

        # Layout
        layout = QHBoxLayout()
        layout.addWidget(self.calc_icon)
        layout.addWidget(self.notepad_icon)
        layout.addWidget(self.image_compressor_icon)
        layout.addWidget(self.classifier_icon)

        # Set layout to container
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def setup_icons(self):
        icon_width = 150
        icon_height = 150
        
        self.calc_icon = QLabel(self)
        self.notepad_icon = QLabel(self)
        self.image_compressor_icon = QLabel(self)
        self.classifier_icon = QLabel(self)

        # Set icons and style
        self.set_icon(self.calc_icon, 'resources/calculator_icon.png', icon_width, icon_height)
        self.set_icon(self.notepad_icon, 'resources/notepad_icon.png', icon_width, icon_height)
        self.set_icon(self.image_compressor_icon, 'resources/compressor_icon.png', icon_width, icon_height)
        self.set_icon(self.classifier_icon, 'resources/ear_recognition.png', icon_width, icon_height)

        # Mouse events for icons
        self.calc_icon.mousePressEvent = self.open_calculator
        self.notepad_icon.mousePressEvent = self.open_notepad
        self.image_compressor_icon.mousePressEvent = self.open_image_compressor
        self.classifier_icon.mousePressEvent = self.open_classifier

    def set_icon(self, label, pixmap_path, width, height):
        pixmap = QPixmap(pixmap_path).scaled(width, height, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        label.setPixmap(pixmap)
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("""
            QLabel {
                border: 4px solid #C8E6C9;
                border-radius: 10px;
                padding: 10px;
                background-color: #E8F5E9;
            }
        """)

    def open_calculator(self, event):
        self.calc_window = CalculatorWindow()
        self.calc_window.show()

    def open_notepad(self, event):
        self.notepad_window = NotepadWindow()
        self.notepad_window.show()

    def open_image_compressor(self, event):
        self.image_compressor_window = ImageCompressorWindow()
        self.image_compressor_window.show()

    def open_classifier(self, event):
        self.classifier_window = ClassifierWindow()
        self.classifier_window.show()
