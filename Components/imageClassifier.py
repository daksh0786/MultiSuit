# classifierwindow.py
from PyQt5.QtWidgets import QMainWindow, QPushButton, QLabel, QVBoxLayout, QFileDialog, QWidget
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import pickle
import cv2
import numpy as np
from skimage.feature import local_binary_pattern

class ClassifierWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Image Classifier")
        self.setGeometry(100, 100, 500, 400)
        self.setStyleSheet("background-color: #EDE7F6;")

        # Load model
        with open('model_saved_ear_LBP.unknown', 'rb') as f:
            self.model = pickle.load(f)

        self.classnames = ['ali', 'daksh', 'khan', 'prath', 'raj']

        # Layout and widgets
        layout = QVBoxLayout()
        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.image_label)

        self.open_button = QPushButton("Open Image", self)
        self.open_button.clicked.connect(self.open_image)
        layout.addWidget(self.open_button)

        self.result_label = QLabel("Predicted Class: ", self)
        self.result_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.result_label)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def open_image(self):
        options = QFileDialog.Options()
        self.image_path, _ = QFileDialog.getOpenFileName(self, "Open Image", "", "Image Files (*.png *.jpg *.jpeg)", options=options)
        if self.image_path:
            pixmap = QPixmap(self.image_path)
            self.image_label.setPixmap(pixmap.scaled(300, 300, Qt.KeepAspectRatio))
            self.classify_image()

    def preprocess_image(self, image_path):
        image = cv2.imread(image_path)
        image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        image = cv2.resize(image, (150, 150))
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
        histogram = self.preprocess_image(self.image_path)
        prediction = self.model.predict(histogram)
        predicted_class = self.classnames[prediction[0]]
        self.result_label.setText(f"Predicted Class: {predicted_class}")
