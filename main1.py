from PyQt6.QtGui import QIcon, QIntValidator, QClipboard
from PyQt6.QtWidgets import (QMainWindow, QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit,
                             QMessageBox, QLayout, QGridLayout, QPushButton)
from PyQt6.QtCore import Qt
import sys
import random
import string

class MainWindow(QMainWindow):
    """
    MainWindow class for creating the Password Genie application.
    Inherits from QMainWindow to provide window functionalities.
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Password Genie")  # Set the window title
        self.setMinimumSize(400, 200)  # Set the minimum size of the window
        self.setWindowIcon(QIcon("Icon.png"))  # Set the window icon

        central_widget = QWidget(self)  # Create a central widget
        self.setCentralWidget(central_widget)  # Set central widget to the window

        layout = QGridLayout()  # Create a grid layout for the main window

        # Password Length input field
        pass_len = QLabel("Password Length: ")  # Label for password length
        self.pass_edit = QLineEdit()  # Input field for password length
        self.pass_edit.setValidator(QIntValidator(0, 255))  # Validator to accept only integers
        layout.addWidget(pass_len, 0, 0)  # Add label to grid layout
        layout.addWidget(self.pass_edit, 0, 1)  # Add input field to grid layout

        # Number of digits input field
        num_count = QLabel("Amount of Numbers:")
        self.num_edit = QLineEdit()
        self.num_edit.setValidator(QIntValidator(0, 300))
        layout.addWidget(num_count, 1, 0)
        layout.addWidget(self.num_edit, 1, 1)

        # Number of special characters input field
        special_char = QLabel("Amount of special characters: ")
        self.special_edit = QLineEdit()
        self.special_edit.setValidator(QIntValidator(0, 255))
        layout.addWidget(special_char, 2, 0)
        layout.addWidget(self.special_edit, 2, 1)

        # Number of alphabets input field
        char_count = QLabel("Amount of Alphabets: ")
        self.char_Edit = QLineEdit()
        self.char_Edit.setValidator(QIntValidator(0, 255))
        layout.addWidget(char_count, 3, 0)
        layout.addWidget(self.char_Edit, 3, 1)

        # Submit button to generate password
        submit_button = QPushButton("Submit")
        layout.addWidget(submit_button, 4, 0, 1, 2, Qt.AlignmentFlag.AlignCenter)  # Center the button
        submit_button.clicked.connect(self.generate_password)  # Connect button to password generation method

        # Copy to Clipboard button (initially hidden)
        self.copy_button = QPushButton("Copy to Clipboard")
        self.copy_button.setVisible(False)  # Initially hide the button
        layout.addWidget(self.copy_button, 6, 0, 1, 2, Qt.AlignmentFlag.AlignCenter)  # Add to layout
        self.copy_button.clicked.connect(self.copy_to_clipboard)  # Connect button to clipboard method

        # Clear button to reset all fields
        clear_button = QPushButton("Clear")
        layout.addWidget(clear_button, 7, 0, 1, 2, Qt.AlignmentFlag.AlignCenter)  # Add to layout
        clear_button.clicked.connect(self.clear_fields)  # Connect button to clear method

        # Output label to display the generated password
        self.output = QLabel("")
        layout.addWidget(self.output, 5, 0, 1, 2, Qt.AlignmentFlag.AlignCenter)  # Add label to layout

        central_widget.setLayout(layout)  # Set layout for central widget
        self.resize(400, 200)  # Set initial window size
        self.setCentralWidget(central_widget)  # Set central widget to the window

    def generate_password(self):
        """
        Generates a password based on user input and displays it in the output label.
        """
        try:
            # Get user inputs for password length, number of digits, special chars, and alphabets
            pass_len = int(self.pass_edit.text())
            num_len = int(self.num_edit.text())
            spec_len = int(self.special_edit.text())
            char_len = int(self.char_Edit.text())
        except ValueError:
            # Display error message if user inputs are not integers
            QMessageBox.warning(self, "ValueError", "PLEASE ENTER VALUES CORRECTLY!!!")
            return

        # Check if the total of numbers, special characters, and alphabets exceeds the password length
        total_count = num_len + spec_len + char_len
        if total_count > pass_len:
            QMessageBox.warning(self, "Input Error", "Total Length is more than Password length.")
            return

        # Generate random numbers, special characters, and alphabets based on user input
        numbers = [str(random.randint(1, 9)) for _ in range(num_len)]
        special_Chars = [random.choice(string.punctuation) for _ in range(spec_len)]
        letters = [random.choice(string.ascii_letters) for _ in range(char_len)]

        # Fill remaining characters with random letters
        remaining_count = pass_len - total_count
        letters += [random.choice(string.ascii_letters) for _ in range(remaining_count)]

        # Combine all parts into a single list and shuffle to randomize the order
        password_list = numbers + special_Chars + letters
        random.shuffle(password_list)

        # Join the list into a string to form the final password
        password = "".join(password_list)

        # Display the generated password in the output label
        self.output.setText(password)

        # Make the Copy button visible after password generation
        self.copy_button.setVisible(True)

    def copy_to_clipboard(self):
        """
        Copies the generated password to the system clipboard.
        """
        clipboard = QApplication.clipboard()  # Access the system clipboard
        clipboard.setText(self.output.text())  # Set the clipboard content to the generated password

    def clear_fields(self):
        """
        Clears all input fields and the generated password output.
        Hides the Copy to Clipboard button.
        """
        # Clear all input fields
        self.pass_edit.clear()
        self.num_edit.clear()
        self.special_edit.clear()
        self.char_Edit.clear()

        # Clear the generated password output
        self.output.clear()

        # Hide the Copy to Clipboard button
        self.copy_button.setVisible(False)


if __name__ == '__main__':
    # Initialize and run the application
    app = QApplication(sys.argv)
    main = MainWindow()  # Create an instance of the MainWindow class
    main.show()  # Show the main window
    sys.exit(app.exec())  # Execute the application and exit when it's closed
