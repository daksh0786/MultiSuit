# -*- coding: utf-8 -*-

# Import necessary modules from PyQt5
from PyQt5 import QtCore, QtGui, QtWidgets

# Define the main UI class
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        """
        Set up the UI components of the main window.
        """
        # Configure main window properties
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1112, 722)
        
        # Set global font for the window
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        MainWindow.setFont(font)
        
        # Set the background color of the main window
        MainWindow.setStyleSheet("background-color: #ECEBDE;")  # Light gray background

        # Initialize the central widget
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # Create a main vertical layout
        self.main_layout = QtWidgets.QVBoxLayout(self.centralwidget)

        # Title Label
        self.label = QtWidgets.QLabel("APP SUITE", self.centralwidget)
        title_font = QtGui.QFont()
        title_font.setFamily("Segoe UI Symbol")
        title_font.setPointSize(14)
        self.label.setFont(title_font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.main_layout.addWidget(self.label)

        # Create a grid layout for buttons and labels
        self.grid_layout = QtWidgets.QGridLayout()
        self.grid_layout.setHorizontalSpacing(40)  # Set horizontal spacing
        self.grid_layout.setVerticalSpacing(10)    # Set vertical spacing
        self.grid_layout.setContentsMargins(10, 10, 10, 10)  # Set layout margins


        # Add buttons with icons to the grid and different colors for each button
        self.pushButton = self.create_icon_button("icons/calculator.png", "Calculator", "#D0E8C5")
        self.pushButton_2 = self.create_icon_button("icons/image_compressor.png", "Image Compressor", "#FFE3E3")
        self.pushButton_3 = self.create_icon_button("icons/ear_recognition.png", "Ear Recognition", "#C6E7FF")
        self.pushButton_4 = self.create_icon_button("icons/notepad.png", "NotePad", "#EF9C66")
        self.pushButton_5 = self.create_icon_button("icons/sudoku.png", "Sudoku", "#B3D9FF")
        self.pushButton_6 = self.create_icon_button("icons/image.png", "Image", "#FFCC99")
        self.pushButton_7 = self.create_icon_button("icons/start.png", "Start", "#FFD700")
        self.pushButton_8 = self.create_icon_button("icons/start.png", "Start", "#D3D3D3")

        # Add corresponding labels for the apps
        self.label_3 = self.create_label("Calculator", font_size=12)
        self.label_4 = self.create_label("Image Compressor", font_size=12)
        self.label_5 = self.create_label("Ear Recognition", font_size=12)
        self.label_6 = self.create_label("NotePad", font_size=12)
        self.label_7 = self.create_label("Sudoku", font_size=12)
        self.label_8 = self.create_label("Image", font_size=12)
        self.label_9 = self.create_label("Start", font_size=12)
        self.label_10 = self.create_label("Start", font_size=12)

        # Arrange buttons and labels in the grid layout
        self.add_to_grid(0, 0, self.pushButton, self.label_3)
        self.add_to_grid(0, 1, self.pushButton_2, self.label_4)
        self.add_to_grid(0, 2, self.pushButton_3, self.label_5)
        self.add_to_grid(0, 3, self.pushButton_4, self.label_6)
        self.add_to_grid(1, 0, self.pushButton_5, self.label_7)
        self.add_to_grid(1, 1, self.pushButton_6, self.label_8)
        self.add_to_grid(1, 2, self.pushButton_7, self.label_9)
        self.add_to_grid(1, 3, self.pushButton_8, self.label_10)

        # Add the grid layout to the main layout
        self.main_layout.addLayout(self.grid_layout)

        # Footer Label
        self.label_2 = QtWidgets.QLabel("© 2024", self.centralwidget)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.main_layout.addWidget(self.label_2)

        # Set the central widget and its layout
        MainWindow.setCentralWidget(self.centralwidget)

        # Connect signals and slots
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
    
    def create_label(self, text, font_size=10):
        """
        Helper function to create a label with customizable font size.
        """
        label = QtWidgets.QLabel(text)
        label.setAlignment(QtCore.Qt.AlignCenter)
        label.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)

        # Set the font for the label with the specified size
        font = QtGui.QFont()
        font.setPointSize(font_size)
        label.setFont(font)

        return label
    
    def create_icon_button(self, icon_path, tooltip, bg_color):
        """
        Helper function to create a button with an icon.
        """
        button = ResizableIconButton(icon_path, tooltip, bg_color)  # Use the custom button class
        return button

    def add_to_grid(self, row, col, button, label):
        """
        Helper function to add a button and label to the grid layout.
        """
        self.grid_layout.addWidget(button, row * 2, col)
        self.grid_layout.addWidget(label, row * 2 + 1, col)


class ResizableIconButton(QtWidgets.QPushButton):
    def __init__(self, icon_path, tooltip, bg_color, parent=None):
        """
        Custom QPushButton with a resizable icon and minimal padding.
        """
        super().__init__(parent)
        self.icon_path = icon_path
        self.setToolTip(tooltip)

        # Set the icon for the button
        self.setIcon(QtGui.QIcon(self.icon_path))

        # Set the initial icon size
        self.setIconSize(QtCore.QSize(64, 64))  # Default size

        # Set the button style to minimize padding and apply background color
        self.setStyleSheet(f"""
            QPushButton {{
                border: 1px solid black;  /* Thin black border around the button */
                padding: 2px;  /* Thin padding around the icon */
                border-radius: 5px;  /* Optional: rounded corners */
                background-color: {bg_color};  /* Set background color */
            }}
            QPushButton:focus {{
                outline: none; /* Remove focus outline */
            }}
        """)

        # Ensure the button has an expanding size policy
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

    def resizeEvent(self, event):
        """
        Override resizeEvent to adjust icon size dynamically and make it edge-to-edge.
        """
        super().resizeEvent(event)

        # Set icon size based on button dimensions with minimal padding
        size = int(min(self.width() * 0.6, self.height()) * 0.6)  # 90% of button size for a thin padding
        self.setIconSize(QtCore.QSize(size, size))


# Main program entry point
if __name__ == "__main__":
    import sys
    # Create the application object
    app = QtWidgets.QApplication(sys.argv)
    
    # Create the main window
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    
    # Display the main window
    MainWindow.show()
    
    # Execute the application event loop
    sys.exit(app.exec_())
