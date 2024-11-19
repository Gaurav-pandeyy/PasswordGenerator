from PyQt6.QtGui import QIcon, QIntValidator, QClipboard
from PyQt6.QtWidgets import (QMainWindow, QApplication, QWidget, QLabel, QLineEdit, QVBoxLayout, QCheckBox,
                             QMessageBox, QGridLayout, QPushButton)
from PyQt6.QtCore import Qt
import sys
import random
import string

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Password Genie")
        self.setMinimumSize(400, 300)
        self.setWindowIcon(QIcon("Icon.png"))

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        layout = QGridLayout()

        # Password Length
        pass_len = QLabel("Password Length: ")
        self.pass_edit = QLineEdit()
        self.pass_edit.setValidator(QIntValidator(0, 255))
        layout.addWidget(pass_len, 0, 0)
        layout.addWidget(self.pass_edit, 0, 1)

        # Number of digits
        num_count = QLabel("Amount of Numbers:")
        self.num_edit = QLineEdit()
        self.num_edit.setValidator(QIntValidator(0, 300))
        layout.addWidget(num_count, 1, 0)
        layout.addWidget(self.num_edit, 1, 1)

        # Number of special characters
        special_count = QLabel("Amount of Special Characters:")
        self.special_edit = QLineEdit()
        self.special_edit.setValidator(QIntValidator(0, 300))
        layout.addWidget(special_count, 2, 0)
        layout.addWidget(self.special_edit, 2, 1)

        # Number of alphabets
        char_count = QLabel("Amount of Alphabets:")
        self.char_edit = QLineEdit()
        self.char_edit.setValidator(QIntValidator(0, 300))
        layout.addWidget(char_count, 3, 0)
        layout.addWidget(self.char_edit, 3, 1)

        # Character Set Customization
        self.include_uppercase = QCheckBox("Include Uppercase Letters")
        self.include_lowercase = QCheckBox("Include Lowercase Letters")
        self.include_digits = QCheckBox("Include Digits")
        self.include_special = QCheckBox("Include Special Characters")
        self.exclude_chars = QLineEdit()
        self.exclude_chars.setPlaceholderText("Exclude characters (e.g., 0, O, l)")

        layout.addWidget(self.include_uppercase, 4, 0, 1, 2)
        layout.addWidget(self.include_lowercase, 5, 0, 1, 2)
        layout.addWidget(self.include_digits, 6, 0, 1, 2)
        layout.addWidget(self.include_special, 7, 0, 1, 2)
        layout.addWidget(QLabel("Exclude characters(doesn't work for numbers):"), 8, 0)
        layout.addWidget(self.exclude_chars, 8, 1)

        # Submit Button
        submit_button = QPushButton("Submit")
        layout.addWidget(submit_button, 9, 0, 1, 2, Qt.AlignmentFlag.AlignCenter)
        submit_button.clicked.connect(self.generate_password)

        # Output
        self.output = QLabel("")
        layout.addWidget(self.output, 10, 0, 1, 2, Qt.AlignmentFlag.AlignCenter)

        central_widget.setLayout(layout)
        self.resize(400, 300)

    def generate_password(self):
        """
        Generates a password based on user input, including customizations and exclusions.
        """
        try:
            pass_len = int(self.pass_edit.text())
            num_len = int(self.num_edit.text())
            spec_len = int(self.special_edit.text())
            char_len = int(self.char_edit.text())
        except ValueError:
            QMessageBox.warning(self, "ValueError", "Please enter valid integer values!")
            return

        # Ensure that password length and character types are valid
        total_count = num_len + spec_len + char_len
        if total_count > pass_len:
            QMessageBox.warning(self, "Input Error", "Total character length exceeds password length.")
            return

        # Get user preferences for character sets
        available_sets = string.ascii_letters  # Start with all alphabetic characters
        if self.include_digits.isChecked():
            available_sets += string.digits
        if self.include_special.isChecked():
            available_sets += string.punctuation

        # Exclude user-specified characters
        exclude = self.exclude_chars.text()
        available_sets = ''.join(c for c in available_sets if c not in exclude)

        # Ensure password has at least the required amount of each character set
        numbers = [str(random.randint(0, 9)) for _ in range(num_len)] if self.include_digits.isChecked() else []
        special_chars = [random.choice(string.punctuation) for _ in range(spec_len)] if self.include_special.isChecked() else []
        letters = [random.choice(string.ascii_letters) for _ in range(char_len)]

        # Fill remaining characters with random selections from available sets
        remaining_count = pass_len - total_count
        filler = [random.choice(available_sets) for _ in range(remaining_count)]

        # Combine and shuffle all parts
        password_list = numbers + special_chars + letters + filler
        random.shuffle(password_list)

        # Join the list into a string to form the final password
        password = "".join(password_list)

        # Display the generated password
        self.output.setText(password)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec())