from PyQt6.QtGui import QIcon, QIntValidator, QClipboard
from PyQt6.QtWidgets import (QMainWindow, QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit,
                             QMessageBox, QLayout, QGridLayout, QPushButton)
from PyQt6.QtCore import Qt
import sys
import random
import string


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Password Genie")
        self.setMinimumSize(400, 200)
        self.setWindowIcon(QIcon("Icon.png"))

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        layout = QGridLayout()
        pass_len = QLabel("Password Length: ")
        self.pass_edit = QLineEdit()
        self.pass_edit.setValidator(QIntValidator(0, 255))
        layout.addWidget(pass_len, 0, 0)
        layout.addWidget(self.pass_edit, 0, 1)

        num_count = QLabel("Amount of Numbers:")
        self.num_edit = QLineEdit()
        self.num_edit.setValidator(QIntValidator(0, 300))
        layout.addWidget(num_count, 1, 0)
        layout.addWidget(self.num_edit, 1, 1)

        special_char = QLabel("Amount of special characters: ")
        self.special_edit = QLineEdit()
        self.special_edit.setValidator(QIntValidator(0, 255))
        layout.addWidget(special_char, 2, 0)
        layout.addWidget(self.special_edit, 2, 1)

        char_count = QLabel("Amount of Alphabets: ")
        self.char_Edit = QLineEdit()
        self.char_Edit.setValidator(QIntValidator(0, 255))
        layout.addWidget(char_count, 3, 0)
        layout.addWidget(self.char_Edit, 3, 1)

        submit_button = QPushButton("Submit")
        layout.addWidget(submit_button, 4, 0, 1, 2, Qt.AlignmentFlag.AlignCenter)
        submit_button.clicked.connect(self.generate_password)

        # Add Copy to Clipboard Button (Initially hidden)
        self.copy_button = QPushButton("Copy to Clipboard")
        self.copy_button.setVisible(False)  # Hide the button initially
        layout.addWidget(self.copy_button, 6, 0, 1, 2, Qt.AlignmentFlag.AlignCenter)
        self.copy_button.clicked.connect(self.copy_to_clipboard)

        # Add Clear Button
        clear_button = QPushButton("Clear")
        layout.addWidget(clear_button, 7, 0, 1, 2, Qt.AlignmentFlag.AlignCenter)
        clear_button.clicked.connect(self.clear_fields)

        self.output = QLabel("")
        layout.addWidget(self.output, 5, 0, 1, 2, Qt.AlignmentFlag.AlignCenter)

        central_widget.setLayout(layout)
        self.resize(400, 200)
        self.setCentralWidget(central_widget)

    def generate_password(self):
        try:
            pass_len = int(self.pass_edit.text())
            num_len = int(self.num_edit.text())
            spec_len = int(self.special_edit.text())
            char_len = int(self.char_Edit.text())
        except ValueError:
            QMessageBox.warning(self, "ValueError", "PLEASE ENTER VALUES CORRECTLY!!!")
            return
        total_count = num_len + spec_len + char_len
        if total_count > pass_len:
            QMessageBox.warning(self, "Input Error", "Total Length is more than Password length.")
            return

        numbers = [str(random.randint(1, 9)) for _ in range(num_len)]
        special_Chars = [random.choice(string.punctuation) for _ in range(spec_len)]
        letters = [random.choice(string.ascii_letters) for _ in range(char_len)]

        remaining_count = pass_len - total_count
        letters += [random.choice(string.ascii_letters) for _ in range(remaining_count)]

        password_list = numbers + special_Chars + letters
        random.shuffle(password_list)

        password = "".join(password_list)

        self.output.setText(password)

        # Make the Copy button visible after password generation
        self.copy_button.setVisible(True)

    def copy_to_clipboard(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.output.text())  # Copy the generated password to the clipboard

    def clear_fields(self):
        # Clear all input fields and the generated password label
        self.pass_edit.clear()
        self.num_edit.clear()
        self.special_edit.clear()
        self.char_Edit.clear()
        self.output.clear()

        # Hide the Copy to Clipboard button again
        self.copy_button.setVisible(False)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec())
