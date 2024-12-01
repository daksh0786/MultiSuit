import sys
import os
import math
import cv2
import numpy as np
import pickle
from skimage.feature import local_binary_pattern
from PyQt5.QtWidgets import QApplication, QPushButton, QMainWindow, QLabel, QWidget, QHBoxLayout, QVBoxLayout, QLineEdit, QTextEdit, QFileDialog, QSlider, QAction, QGridLayout
from PyQt5.QtGui import QPixmap, QFont, QImageWriter, QImage, QIcon
from PyQt5.QtCore import Qt
from PyQt5.QtPrintSupport import QPrinter, QPrintDialog

# Main Window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set window title and geometry
        self.setWindowTitle("Multi-App Frame")
        self.setGeometry(300, 300, 750, 250)

        # Set pastel background color for the main window
        self.setStyleSheet("background-color: #FFEBEE;")  # Light pastel pink

        # Create icon labels for Calculator, Notepad, and Image Compressor apps
        self.calc_icon = QLabel(self)
        self.notepad_icon = QLabel(self)
        self.image_compressor_icon = QLabel(self)
        self.classifier_icon = QLabel(self)

        # Load icons using QPixmap
        self.calc_pixmap = QPixmap('calculator_icon.png') 
        self.notepad_pixmap = QPixmap('notepad_icon.png')
        self.image_compressor_pixmap = QPixmap('compressor_icon.png')  
        self.classifier_pixmap = QPixmap('Ear Recognition.png')

        # Set icons in the labels
        self.calc_icon.setPixmap(self.calc_pixmap)
        self.notepad_icon.setPixmap(self.notepad_pixmap)
        self.image_compressor_icon.setPixmap(self.image_compressor_pixmap)
        self.classifier_icon.setPixmap(self.classifier_pixmap)
        
        # Set fixed size for each icon
        icon_width = 150  # Define the desired width
        icon_height = 150  # Define the desired height

        # Load and fit images into QLabel containers
        calc_pixmap = QPixmap("calculator_icon.png").scaled(icon_width, icon_height, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        notepad_pixmap = QPixmap("notepad_icon.png").scaled(icon_width, icon_height, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        image_compressor_pixmap = QPixmap("compressor_icon.png").scaled(icon_width, icon_height, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        classifier_pixmap = QPixmap("Ear Recognition.png").scaled(icon_width, icon_height, Qt.KeepAspectRatio, Qt.SmoothTransformation)

        # Set the scaled pixmaps to the labels
        self.calc_icon.setPixmap(calc_pixmap)
        self.notepad_icon.setPixmap(notepad_pixmap)
        self.image_compressor_icon.setPixmap(image_compressor_pixmap)
        self.classifier_icon.setPixmap(classifier_pixmap)

        # Add borders and padding to the icons
        self.calc_icon.setStyleSheet("""
            QLabel {
                border: 4px solid #C8E6C9;  /* Strong pastel green border */
                border-radius: 10px;
                padding: 10px;
                background-color: #E8F5E9;  /* Light pastel background for the label */
            }
        """)
        self.notepad_icon.setStyleSheet("""
            QLabel {
                border: 4px solid #42A5F5;  /* Strong pastel blue border */
                border-radius: 10px;
                padding: 10px;
                background-color: #F0F8FF;  /* Light pastel background for the label */
            }
        """)
        self.image_compressor_icon.setStyleSheet("""
            QLabel {
                border: 4px solid #FFCDD2;  /* Strong pastel red border */
                border-radius: 10px;
                padding: 10px;
                background-color: #FFEBEE;  /* Light pastel pink background */
            }
        """)
        
        self.classifier_icon.setStyleSheet("""
            QLabel {
                border: 4px solid #B39DDB;  /* Strong pastel purple border */
                border-radius: 10px;
                padding: 10px;
                background-color: #EDE7F6;  /* Light pastel background */
            }
        """)

        # Set alignment for the icons
        self.calc_icon.setAlignment(Qt.AlignCenter)
        self.notepad_icon.setAlignment(Qt.AlignCenter)
        self.image_compressor_icon.setAlignment(Qt.AlignCenter)
        self.classifier_icon.setAlignment(Qt.AlignCenter)

        # Add click events for the icons
        self.calc_icon.mousePressEvent = self.open_calculator
        self.notepad_icon.mousePressEvent = self.open_notepad
        self.image_compressor_icon.mousePressEvent = self.open_image_compressor
        self.classifier_icon.mousePressEvent = self.open_classifier  # Add click event for the classifier


        # Layout to organize the icons horizontally
        layout = QHBoxLayout()
        layout.addWidget(self.calc_icon)
        layout.addWidget(self.notepad_icon)
        layout.addWidget(self.image_compressor_icon)
        layout.addWidget(self.classifier_icon)  # Add classifier icon to the layout


        # Set layout into a container
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    # Open Calculator app
    def open_calculator(self, event):
        self.calc_window = CalculatorWindow()
        self.calc_window.show()

    # Open Notepad app
    def open_notepad(self, event):
        self.notepad_window = NotepadWindow()
        self.notepad_window.show()

    # Open Image Compressor app
    def open_image_compressor(self, event):
        self.image_compressor_window = ImageCompressorWindow()
        self.image_compressor_window.show()
        
    # Open Image Classifier app
    def open_classifier(self, event):
        self.classifier_window = ClassifierWindow()
        self.classifier_window.show()
        


class ClassifierWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Image Classifier")
        self.setGeometry(100, 100, 500, 400)

        # Set pastel color for the classifier window
        self.setStyleSheet("background-color: #EDE7F6;")  # Light pastel purple

        # Load the pre-trained model from the pickle file
        with open('model_saved_ear_LBP.unknown', 'rb') as f:
            self.model = pickle.load(f)

        # Classnames corresponding to the labels in the model
        self.classnames = ['ali', 'daksh', 'khan', 'prath', 'raj']

        # Create a layout to hold UI components
        layout = QVBoxLayout()

        # Create a label to display the selected image
        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.image_label)

        # Create a button to open an image file
        self.open_button = QPushButton("Open Image", self)
        self.open_button.clicked.connect(self.open_image)
        layout.addWidget(self.open_button)

        # Create a label to display the classification result
        self.result_label = QLabel("Predicted Class: ", self)
        self.result_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.result_label)

        # Set layout into a container widget
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.image_path = ""

    def open_image(self):
        # Open a file dialog to select the image
        options = QFileDialog.Options()
        self.image_path, _ = QFileDialog.getOpenFileName(self, "Open Image", "", "Image Files (*.png *.jpg *.jpeg)", options=options)

        if self.image_path:
            # Display the selected image in the label
            pixmap = QPixmap(self.image_path)
            self.image_label.setPixmap(pixmap.scaled(300, 300, Qt.KeepAspectRatio))

            # Preprocess and classify the image
            self.classify_image()

    def preprocess_image(self, image_path):
        image = cv2.imread(image_path)
        image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        image = cv2.resize(image, (150, 150))

        # Extract LBP features
        lbp = local_binary_pattern(image, P=8, R=1)
        histogram = self.create_histogram(lbp, sub_images_num=3, bins_per_sub_images=64)
        return histogram.reshape(1, -1)

    def create_histogram(self, image, sub_images_num, bins_per_sub_images):
        grid = np.arange(0, image.shape[1] + 1, image.shape[1] // sub_images_num)
        sub_image_histograms = []
        for i in range(1, len(grid)):
            for j in range(1, len(grid)):
                sub_image = image[grid[i - 1]:grid[i], grid[j - 1]:grid[j]]
                sub_image_histogram = np.histogram(sub_image, bins=bins_per_sub_images)[0]
                sub_image_histograms.append(sub_image_histogram)
        return np.array(sub_image_histograms).flatten()

    def classify_image(self):
        # Preprocess the image and predict the class label
        histogram = self.preprocess_image(self.image_path)
        prediction = self.model.predict(histogram)
        predicted_class = self.classnames[prediction[0]]

        # Display the predicted class label
        self.result_label.setText(f"Predicted Class: {predicted_class}")

class CalculatorWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Scientific Calculator")
        self.setGeometry(100, 100, 400, 480)  # Starting size

        # Set pastel color for the calculator window
        self.setStyleSheet("background-color: #C8E6C9;")  # Light pastel green

        # Main widget container
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Main layout (vertical layout for input display and buttons)
        main_layout = QVBoxLayout(central_widget)

        # Create a QLineEdit widget for the display
        self.display = QLineEdit(self)
        self.display.setReadOnly(True)
        self.display.setStyleSheet("background-color: #FFFFFF; font-size: 18px; color: #000000;")  # White display
        self.display.setFont(QFont('Arial', 20))
        self.display.setAlignment(Qt.AlignRight)
        self.display.setMinimumHeight(60)  # Adjusted input box height

        # Add display to the main layout
        main_layout.addWidget(self.display)

        # Create a grid layout for buttons
        self.create_buttons(main_layout)

        # This will store the current operation
        self.current_operation = None

    # Function to create buttons in a grid layout
    def create_buttons(self, layout):
        button_labels = [
            '7', '8', '9', '/', 'sin', 'cos', 'tan', 'log',
            '4', '5', '6', '*', 'sqrt', '^', '(', ')',
            '1', '2', '3', '-', 'pi', 'exp', 'ln', '%',
            '0', 'C', '=', '+', 'e', 'mod', '.', '!'
        ]

        # Grid layout for buttons
        button_layout = QGridLayout()

        positions = [(i, j) for i in range(5) for j in range(8)]  # 5 rows, 8 columns
        for position, label in zip(positions, button_labels):
            button = QPushButton(label, self)  # Create a button
            button.setStyleSheet("""
                QPushButton {
                    background-color: #FFCCBC;  /* Pastel orange background */
                    font-size: 18px; 
                    border: 2px solid #FF6F61;  /* Strong border */
                    border-radius: 8px;  /* Curved edges */
                    padding: 10px;
                    color: #000000;
                }
                QPushButton:pressed {
                    background-color: #FF8A65;  /* Darker orange when pressed */
                }
            """)
            button.setFont(QFont('Arial', 14))
            button.clicked.connect(self.on_button_click)  # Connect button click event
            button_layout.addWidget(button, *position)  # Add button to grid layout

        # Add the button grid layout to the main layout
        layout.addLayout(button_layout)

    # Button click event handler
    def on_button_click(self):
        sender = self.sender()
        text = sender.text()

        # Clear the display
        if text == 'C':
            self.display.clear()
            self.current_operation = None

        # Handle operations
        elif text == '=':
            try:
                if self.current_operation:
                    result = self.perform_operation()
                    self.display.setText(str(result))
                    self.current_operation = None
                else:
                    result = eval(self.display.text())
                    self.display.setText(str(result))
            except Exception as e:
                self.display.setText("Error")
        
        # Set the current operation (sin, cos, tan, etc.)
        elif text in ['sin', 'cos', 'tan', 'log', 'sqrt', 'exp', 'ln', 'pi', 'e', '%', '^', 'mod', '!']:
            self.current_operation = text
            current_text = self.display.text()
            self.display.setText(current_text + text)
            # self.display.clear()

        # Handle mathematical functions like sin, cos, etc.
        elif text in ['pi', 'e', '.', '%', '!', '^']:
            if text == 'pi':
                self.display.setText(str(math.pi))
            elif text == 'e':
                self.display.setText(str(math.e))
            elif text == '.':
                current_text = self.display.text()
                if '.' not in current_text:
                    self.display.setText(current_text + '.')
            elif text == '%':
                try:
                    current_text = float(self.display.text())
                    self.display.setText(str(current_text / 100))
                except ValueError:
                    self.display.setText("Error")
            elif text == '^':
                current_text = self.display.text()
                self.display.setText(current_text + '')
            elif text == '!':
                try:
                    current_text = int(self.display.text())
                    result = math.factorial(current_text)
                    self.display.setText(str(result))
                except ValueError:
                    self.display.setText("Error")

        # Standard numbers and operators
        else:
            current_text = self.display.text()
            self.display.setText(current_text + text)

    def evaluate_expression(self):
        """ Evaluate the mathematical expression from the display. """
        expression = self.display.text()
        expression+=')'
        print(expression)

        # Replace parentheses for easier evaluation
        expression = expression.replace("sin", "math.sin")
        expression = expression.replace("cos", "math.cos")
        expression = expression.replace("tan", "math.tan")
        expression = expression.replace("log", "math.log10")
        expression = expression.replace("sqrt", "math.sqrt")
        expression = expression.replace("exp", "math.exp")
        expression = expression.replace("ln", "math.log")
        expression = expression.replace("pi", str(math.pi))
        expression = expression.replace("e", str(math.e))
        expression = expression.replace("^", "")
        expression = expression.replace("mod", "%")

        try:
            # Evaluate the expression and return the result
            result = eval(expression)
            return result
        except Exception as e:
          return "Good"
# class CalculatorWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Scientific Calculator")
        self.setGeometry(100, 100, 400, 480)  # Starting size

        # Set pastel color for the calculator window
        self.setStyleSheet("background-color: #C8E6C9;")  # Light pastel green

        # Main widget container
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Main layout (vertical layout for input display and buttons)
        main_layout = QVBoxLayout(central_widget)

        # Create a QLineEdit widget for the display
        self.display = QLineEdit(self)
        self.display.setReadOnly(False)  # Make the input editable
        self.display.setStyleSheet("background-color: #FFFFFF; font-size: 18px; color: #000000;")  # White display
        self.display.setFont(QFont('Arial', 20))
        self.display.setAlignment(Qt.AlignRight)
        self.display.setMinimumHeight(60)  # Adjusted input box height

        # Add display to the main layout
        main_layout.addWidget(self.display)

        # Create a grid layout for buttons
        self.create_buttons(main_layout)

        # This will store the current operation
        self.current_operation = None

    # Function to create buttons in a grid layout
    def create_buttons(self, layout):
        button_labels = [
            '7', '8', '9', '/', 'sin', 'cos', 'tan', 'log',
            '4', '5', '6', '*', 'sqrt', '^', '(', ')',
            '1', '2', '3', '-', 'pi', 'exp', 'ln', '%',
            '0', 'C', '=', '+', 'e', 'mod', '.', '!'
        ]

        # Grid layout for buttons
        button_layout = QGridLayout()

        positions = [(i, j) for i in range(5) for j in range(8)]  # 5 rows, 8 columns
        for position, label in zip(positions, button_labels):
            button = QPushButton(label, self)  # Create a button
            button.setStyleSheet("""
                QPushButton {
                    background-color: #FFCCBC;  /* Pastel orange background */
                    font-size: 18px; 
                    border: 2px solid #FF6F61;  /* Strong border */
                    border-radius: 8px;  /* Curved edges */
                    padding: 10px;
                    color: #000000;
                }
                QPushButton:pressed {
                    background-color: #FF8A65;  /* Darker orange when pressed */
                }
            """)
            button.setFont(QFont('Arial', 14))
            button.clicked.connect(self.on_button_click)  # Connect button click event
            button_layout.addWidget(button, *position)  # Add button to grid layout

        # Add the button grid layout to the main layout
        layout.addLayout(button_layout)

    # Button click event handler
    def on_button_click(self):
        sender = self.sender()
        text = sender.text()

        # Clear the display
        if text == 'C':
            self.display.clear()
            self.current_operation = None

        # Handle operations
        elif text == '=':
            try:
                result = self.evaluate_expression()
                self.display.setText(str(result))
            except Exception as e:
                self.display.setText("Error")
        
        # Set the current operation (sin, cos, tan, etc.)
        elif text in ['sin', 'cos', 'tan', 'log', 'sqrt', 'exp', 'ln', 'pi', 'e', '%', '!', '^', 'mod']:
            self.current_operation = text
            current_text = self.display.text()
            if current_text == "":
                self.display.setText(text + "(")  # Append function with opening parenthesis
            else:
                self.display.setText(current_text + text + "(")  # Append function with opening parenthesis

        # Handle mathematical functions like sin, cos, etc.
        elif text in ['pi', 'e', '.', '%', '!', '^']:
            if text == 'pi':
                self.display.setText(self.display.text() + str(math.pi))
            elif text == 'e':
                self.display.setText(self.display.text() + str(math.e))
            elif text == '.':
                current_text = self.display.text()
                if '.' not in current_text:
                    self.display.setText(current_text + '.')
            elif text == '%':
                try:
                    current_text = float(self.display.text())
                    self.display.setText(str(current_text / 100))
                except ValueError:
                    self.display.setText("Error")
            elif text == '^':
                current_text = self.display.text()
                self.display.setText(current_text + '')
            elif text == '!':
                try:
                    current_text = int(self.display.text())
                    result = math.factorial(current_text)
                    self.display.setText(str(result))
                except ValueError:
                    self.display.setText("Error")

        # Standard numbers and operators
        else:
            current_text = self.display.text()
            self.display.setText(current_text + text)

    def evaluate_expression(self):
        """ Evaluate the mathematical expression from the display. """
        expression = self.display.text()

        # Replace parentheses for easier evaluation
        expression = expression.replace("sin", "math.sin")
        expression = expression.replace("cos", "math.cos")
        expression = expression.replace("tan", "math.tan")
        expression = expression.replace("log", "math.log10")
        expression = expression.replace("sqrt", "math.sqrt")
        expression = expression.replace("exp", "math.exp")
        expression = expression.replace("ln", "math.log")
        expression = expression.replace("pi", str(math.pi))
        expression = expression.replace("e", str(math.e))
        expression = expression.replace("^", "")
        expression = expression.replace("mod", "%")

        try:
            # Evaluate the expression and return the result
            result = eval(expression)
            return result
        except Exception as e:
            return "Error"
# Notepad Window
class NotepadWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Notepad")
        self.setGeometry(100, 100, 800, 600)

        # Set pastel color for the notepad window
        self.setStyleSheet("background-color: #FFF9C4;")  # Light pastel yellow

        # Create a QTextEdit widget for the notepad
        self.text_area = QTextEdit(self)

        # Apply strong border to the text area
        self.text_area.setStyleSheet("""
            QTextEdit {
                border: 3px solid #42A5F5;  /* Strong pastel blue border */
                background-color: #FFFFFF;  /* White text area */
                padding: 10px;
                border-radius: 4px;
            }
        """)
        self.setCentralWidget(self.text_area)

        # Initialize a variable to store the file path
        self.file_path = None

        # Create menu and toolbar
        self.create_menu()

    def create_menu(self):
        # Create a menu bar
        menubar = self.menuBar()

        # File menu
        file_menu = menubar.addMenu("File")
        
        # New file
        new_action = QAction("New", self)
        new_action.setShortcut("Ctrl+N")
        new_action.triggered.connect(self.new_file)

        # New Window
        new_window_action = QAction("New Window", self)
        new_window_action.setShortcut("Ctrl+Shift+N")
        new_window_action.triggered.connect(self.new_window)

        # Open file
        open_action = QAction("Open...", self)
        open_action.setShortcut("Ctrl+O")
        open_action.triggered.connect(self.open_file)

        # Save file
        save_action = QAction("Save", self)
        save_action.setShortcut("Ctrl+S")
        save_action.triggered.connect(self.save_file)

        # Save As
        save_as_action = QAction("Save As...", self)
        save_as_action.setShortcut("Ctrl+Shift+S")
        save_as_action.triggered.connect(self.save_file_as)

        # Page Setup (Placeholder - No direct dialog in Qt)
        page_setup_action = QAction("Page Setup...", self)

        # Print
        print_action = QAction("Print...", self)
        print_action.setShortcut("Ctrl+P")
        print_action.triggered.connect(self.print_file)

        # Exit
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)

        file_menu.addAction(new_action)
        file_menu.addAction(new_window_action)
        file_menu.addAction(open_action)
        file_menu.addAction(save_action)
        file_menu.addAction(save_as_action)
        file_menu.addAction(page_setup_action)
        file_menu.addAction(print_action)
        file_menu.addAction(exit_action)

    def new_file(self):
        self.text_area.clear()
        self.file_path = None
        self.setWindowTitle("Notepad - New File")

    def new_window(self):
        new_notepad = NotepadWindow()
        new_notepad.show()

    def open_file(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Open File", "", "Text Files (.txt);;All Files ()", options=options)
        if file_path:
            with open(file_path, 'r') as f:
                content = f.read()
            self.text_area.setText(content)
            self.file_path = file_path
            self.setWindowTitle(f"Notepad - {file_path}")

    def save_file(self):
        if self.file_path is None:
            self.save_file_as()
        else:
            with open(self.file_path, 'w') as f:
                f.write(self.text_area.toPlainText())
            self.setWindowTitle(f"Notepad - {self.file_path}")

    def save_file_as(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(self, "Save File As", "", "Text Files (.txt);;All Files ()", options=options)
        if file_path:
            self.file_path = file_path
            self.save_file()

    def print_file(self):
        printer = QPrinter()
        print_dialog = QPrintDialog(printer, self)
        if print_dialog.exec_() == QPrintDialog.Accepted:
            self.text_area.print_(printer)


# Image Compressor Window
class ImageCompressorWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Image Compressor")
        self.setGeometry(100, 100, 500, 450)

        # Set a light pastel background color for a professional feel
        self.setStyleSheet("background-color: #F5F5F5;")  # Light grey

        # Create a layout to hold UI components
        layout = QVBoxLayout()

        # Create a label to display the selected image
        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setFixedSize(300, 300)
        self.image_label.setStyleSheet("""
            QLabel {
                border: 2px solid #B0BEC5;
                border-radius: 10px;
                background-color: #ECEFF1; /* Light grey */
            }
        """)
        layout.addWidget(self.image_label)

        # Create a button to open image file
        self.open_button = QPushButton("Open Image", self)
        self.open_button.clicked.connect(self.open_image)
        self.open_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;  /* Green */
                color: white;
                font-size: 16px;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45A049;
            }
        """)
        layout.addWidget(self.open_button)

        # Create a label to display compression percentage
        self.percentage_label = QLabel("Compression Quality: 80%", self)
        self.percentage_label.setAlignment(Qt.AlignCenter)
        self.percentage_label.setFont(QFont("Arial", 14))
        layout.addWidget(self.percentage_label)

        # Create a slider to control compression quality
        self.slider = QSlider(Qt.Horizontal, self)
        self.slider.setRange(1, 100)
        self.slider.setValue(80)  # Default quality
        self.slider.setStyleSheet("""
            QSlider::groove:horizontal {
                height: 6px;
                background: #D3D3D3;
                border-radius: 3px;
            }
            QSlider::handle:horizontal {
                background: #FF5722;  /* Orange */
                border: 1px solid #FF7043;
                width: 14px;
                height: 14px;
                margin: -4px 0;
                border-radius: 7px;
            }
        """)
        self.slider.valueChanged.connect(self.update_percentage)
        layout.addWidget(self.slider)

        # Create a button to save the compressed image
        self.compress_button = QPushButton("Compress Image", self)
        self.compress_button.clicked.connect(self.compress_image)
        self.compress_button.setStyleSheet("""
            QPushButton {
                background-color: #FF5722;  /* Orange */
                color: white;
                font-size: 16px;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #E64A19;
            }
        """)
        layout.addWidget(self.compress_button)

        # Set layout into a container widget
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.image_path = ""

    def open_image(self):
        options = QFileDialog.Options()
        self.image_path, _ = QFileDialog.getOpenFileName(self, "Open Image", "", "Image Files (*.png *.jpg *.jpeg)", options=options)

        if self.image_path:
            # Display the selected image in the label
            pixmap = QPixmap(self.image_path)
            self.image_label.setPixmap(pixmap.scaled(300, 300, Qt.KeepAspectRatio))

    def update_percentage(self):
        quality = self.slider.value()
        self.percentage_label.setText(f"Compression Quality: {quality}%")

    def compress_image(self):
        if not self.image_path:
            return

        # Get the quality from the slider
        quality = self.slider.value()

        # Get the directory where the script is located
        current_directory = os.path.dirname(os.path.abspath(__file__))

        # Save the compressed image in the same directory
        compressed_image_path = os.path.join(current_directory, 'compressed_image.jpg')

        # Compress the image
        image = QImage(self.image_path)
        image_writer = QImageWriter(compressed_image_path)
        image_writer.setQuality(quality)
        image_writer.write(image)

        # Show the compressed image in the label
        pixmap = QPixmap(compressed_image_path)
        self.image_label.setPixmap(pixmap.scaled(300, 300, Qt.KeepAspectRatio))

# Main entry point
if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Create and show the main window
    main_window = MainWindow()
    main_window.show()

    sys.exit(app.exec_())