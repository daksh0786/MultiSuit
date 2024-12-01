# notepadwindow.py
from PyQt5.QtWidgets import QMainWindow, QTextEdit, QFileDialog, QMenu, QAction, QVBoxLayout, QWidget
from PyQt5.QtPrintSupport import QPrinter, QPrintDialog

class NotepadWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Notepad")
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet("background-color: #FFF9C4;")

        # Notepad setup
        self.text_area = QTextEdit(self)
        self.setCentralWidget(self.text_area)

        # File menu
        self.create_menu()

    def create_menu(self):
        menubar = self.menuBar()
        file_menu = menubar.addMenu("File")

        new_action = QAction("New", self)
        new_action.triggered.connect(self.new_file)

        open_action = QAction("Open...", self)
        open_action.triggered.connect(self.open_file)

        save_action = QAction("Save", self)
        save_action.triggered.connect(self.save_file)

        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)

        file_menu.addAction(new_action)
        file_menu.addAction(open_action)
        file_menu.addAction(save_action)
        file_menu.addAction(exit_action)

    def new_file(self):
        self.text_area.clear()

    def open_file(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Open File", "", "Text Files (*.txt);;All Files (*)", options=options)
        if file_path:
            with open(file_path, 'r') as f:
                content = f.read()
            self.text_area.setText(content)

    def save_file(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Save File", "", "Text Files (*.txt);;All Files (*)")
        if file_path:
            with open(file_path, 'w') as f:
                f.write(self.text_area.toPlainText())
