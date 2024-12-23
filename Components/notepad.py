# notepadwindow.py
import sys
import random
import pymysql
from PyQt5.QtWidgets import (
    QMainWindow, QTextEdit, QFileDialog, QMenu, QAction, QVBoxLayout, QWidget, QGridLayout, QWidget, QLineEdit, QPushButton, QMessageBox, QLabel, QApplication,
    QTextEdit, QTableWidget, QTableWidgetItem
)
from PyQt5.QtPrintSupport import QPrinter, QPrintDialog
from PyQt5.QtCore import Qt

    
class NotepadWindow(QMainWindow):
    # def __init__(self):
    #     super().__init__()
    #     self.setWindowTitle("Notepad")
    #     self.setGeometry(100, 100, 800, 600)
    #     self.setStyleSheet("background-color: #FFF9C4;")

    #     # Notepad setup
    #     self.text_area = QTextEdit(self)
    #     self.setCentralWidget(self.text_area)

    #     # File menu
    #     self.create_menu()

    # def create_menu(self):
    #     menubar = self.menuBar()
    #     file_menu = menubar.addMenu("File")

    #     new_action = QAction("New", self)
    #     new_action.triggered.connect(self.new_file)

    #     open_action = QAction("Open...", self)
    #     open_action.triggered.connect(self.open_file)

    #     save_action = QAction("Save", self)
    #     save_action.triggered.connect(self.save_file)

    #     exit_action = QAction("Exit", self)
    #     exit_action.triggered.connect(self.close)

    #     file_menu.addAction(new_action)
    #     file_menu.addAction(open_action)
    #     file_menu.addAction(save_action)
    #     file_menu.addAction(exit_action)

    # def new_file(self):
    #     self.text_area.clear()

    # def open_file(self):
    #     options = QFileDialog.Options()
    #     file_path, _ = QFileDialog.getOpenFileName(self, "Open File", "", "Text Files (*.txt);;All Files (*)", options=options)
    #     if file_path:
    #         with open(file_path, 'r') as f:
    #             content = f.read()
    #         self.text_area.setText(content)

    # def save_file(self):
    #     file_path, _ = QFileDialog.getSaveFileName(self, "Save File", "", "Text Files (*.txt);;All Files (*)")
    #     if file_path:
    #         with open(file_path, 'w') as f:
    #             f.write(self.text_area.toPlainText())



    def __init__(self):
        super().__init__()

        # Main Window Config
        self.setWindowTitle("SQL Query Application")
        self.setGeometry(100, 100, 800, 600)

        # Central Widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Layout
        self.layout = QVBoxLayout(self.central_widget)

        # Input Field for SQL Query
        self.query_input = QTextEdit(self)
        self.query_input.setPlaceholderText("Enter your SQL query here...")
        self.layout.addWidget(self.query_input)

        # Execute Button
        self.execute_button = QPushButton("Execute Query")
        self.execute_button.clicked.connect(self.execute_query)
        self.layout.addWidget(self.execute_button)

        # Table Widget for Displaying Results
        self.result_table = QTableWidget(self)
        self.layout.addWidget(self.result_table)

        # Connection Config
        self.connection = None
        self.connect_to_database()

    def connect_to_database(self):
        """Establish a connection to the remote database."""
        try:
            self.connection = pymysql.connect(
                host="172.31.67.76",  # Example: your server's IP address
                user="prabhJot2025",     # Example: remote user
                password="dakshK@2025",  # Example: your password
                database="majorproject2025",  # Database name
                port=3306  # Default MySQL port
            )
            print("Connection successful!")
        except Exception as e:
            self.query_input.setPlainText(f"Error connecting to database: {str(e)}")
            print(f"Error: {str(e)}")

    def execute_query(self):
        """Execute the SQL query entered by the user."""
        query = self.query_input.toPlainText()
        if not self.connection:
            self.query_input.setPlainText("Not connected to the database.")
            return

        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query)
                if query.strip().upper().startswith("SELECT"):
                    results = cursor.fetchall()
                    headers = [desc[0] for desc in cursor.description]
                    self.populate_table(results, headers)
                else:
                    self.connection.commit()
                    self.query_input.setPlainText("Query executed successfully.")
        except Exception as e:
            self.query_input.setPlainText(f"Error executing query: {str(e)}")

    def populate_table(self, data, headers):
        """Display query results in the table widget."""
        self.result_table.clear()
        self.result_table.setRowCount(len(data))
        self.result_table.setColumnCount(len(headers))
        self.result_table.setHorizontalHeaderLabels(headers)

        for row_idx, row_data in enumerate(data):
            for col_idx, cell_data in enumerate(row_data):
                self.result_table.setItem(row_idx, col_idx, QTableWidgetItem(str(cell_data)))





    

    
    