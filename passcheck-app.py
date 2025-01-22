import sys
import os
import random
import string
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QMessageBox, QVBoxLayout, QWidget, QDialog, QHBoxLayout
)
from PyQt5.QtGui import QFont, QIcon, QColor
from PyQt5.QtCore import Qt


class PasswordCheckerApp(QMainWindow):
    def __init__(self):
        super().__init__()

        # Get the path to the bundled icon
        self.icon_path = self.get_bundled_path("pass.ico")
        self.setWindowTitle("Password Checker")
        self.setGeometry(100, 100, 450, 350)
        self.setWindowIcon(QIcon(self.icon_path))  # Use the bundled icon

        # Main layout
        layout = QVBoxLayout()

        # Title label
        title_label = QLabel("Password Checker", self)
        title_label.setStyleSheet("font-size: 20px; font-weight: bold; text-align: center;")
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)

        # Check Password Strength Button
        self.check_button = QPushButton("Check Password Strength", self)
        self.check_button.setFont(QFont("Arial", 12))
        self.check_button.setFixedHeight(40)
        self.check_button.clicked.connect(self.check_password_strength)
        layout.addWidget(self.check_button)

        # Generate Strong Password Button
        self.generate_button = QPushButton("Generate Strong Password", self)
        self.generate_button.setFont(QFont("Arial", 12))
        self.generate_button.setFixedHeight(40)
        self.generate_button.clicked.connect(self.generate_password)
        layout.addWidget(self.generate_button)

        # Exit Button
        self.exit_button = QPushButton("Exit", self)
        self.exit_button.setFont(QFont("Arial", 12))
        self.exit_button.setFixedHeight(40)
        self.exit_button.clicked.connect(self.close)
        layout.addWidget(self.exit_button)

        # Set layout to central widget
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def get_bundled_path(self, relative_path):
        """Get the absolute path to a resource, whether bundled or running from source."""
        if hasattr(sys, "_MEIPASS"):
            # PyInstaller creates a temporary folder _MEIPASS and stores resources there
            return os.path.join(sys._MEIPASS, relative_path)
        return os.path.join(os.path.abspath("."), relative_path)

    def check_password_strength(self):
        dialog = PasswordInputDialog("Enter your password:", self.icon_path)
        if dialog.exec_() == QDialog.Accepted:
            password = dialog.get_input_text()
            if password:
                strength, suggestions = self.get_password_strength(password)
                result = f"Password Strength: {strength}\n"
                if suggestions:
                    result += "Suggestions:\n" + "\n".join("- " + s for s in suggestions)

                QMessageBox.information(self, "Password Strength", result)

    def generate_password(self):
        dialog = NumberInputDialog("Enter password length (8-32):", 12, 8, 32, self.icon_path)
        if dialog.exec_() == QDialog.Accepted:
            length = dialog.get_input_number()
            if length:
                password = self.generate_strong_password(length)
                dialog = PasswordDialog(password, self.icon_path, self)
                dialog.exec_()

    @staticmethod
    def get_password_strength(password):
        strength = "Weak"
        suggestions = []
        if len(password) < 8:
            suggestions.append("Password should be at least 8 characters long.")
        elif len(password) >= 12:
            strength = "Strong"
        else:
            strength = "Moderate"

        has_uppercase = any(char.isupper() for char in password)
        has_lowercase = any(char.islower() for char in password)
        has_numbers = any(char.isdigit() for char in password)
        has_symbols = any(char in "!@#$%^&*()" for char in password)

        if strength == "Strong":
            if not (has_uppercase and has_lowercase and has_numbers and has_symbols):
                suggestions.append("Include uppercase, lowercase, numbers, and symbols.")
        elif strength == "Moderate":
            if not (has_uppercase or has_lowercase) or not (has_numbers or has_symbols):
                suggestions.append("Use at least two types: letters, numbers, or symbols.")

        if password.lower() in ["password", "123456", "qwerty"]:
            suggestions.append("Avoid common or guessable passwords.")

        return strength, suggestions

    @staticmethod
    def generate_strong_password(length=12):
        uppercase = string.ascii_uppercase
        lowercase = string.ascii_lowercase
        digits = string.digits
        symbols = "!@#$%^&*()"
        all_characters = uppercase + lowercase + digits + symbols
        return ''.join(random.choice(all_characters) for _ in range(length))


class PasswordInputDialog(QDialog):
    def __init__(self, prompt, icon_path, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Check Password Strength")
        self.setWindowIcon(QIcon(icon_path))  # Use the bundled icon
        self.setGeometry(200, 200, 400, 150)

        layout = QVBoxLayout()
        label = QLabel(prompt, self)
        label.setFont(QFont("Arial", 12))
        layout.addWidget(label)

        self.input_field = QLineEdit(self)
        self.input_field.setEchoMode(QLineEdit.Password)
        self.input_field.setFont(QFont("Arial", 12))
        layout.addWidget(self.input_field)

        button_layout = QHBoxLayout()
        ok_button = QPushButton("OK", self)
        ok_button.setFont(QFont("Arial", 12))
        ok_button.clicked.connect(self.accept)
        button_layout.addWidget(ok_button)

        cancel_button = QPushButton("Cancel", self)
        cancel_button.setFont(QFont("Arial", 12))
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(cancel_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)

    def get_input_text(self):
        return self.input_field.text()


class NumberInputDialog(QDialog):
    def __init__(self, prompt, default, minimum, maximum, icon_path, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Generate Password")
        self.setWindowIcon(QIcon(icon_path))  # Use the bundled icon
        self.setGeometry(200, 200, 400, 150)

        layout = QVBoxLayout()
        label = QLabel(prompt, self)
        label.setFont(QFont("Arial", 12))
        layout.addWidget(label)

        self.input_field = QLineEdit(self)
        self.input_field.setFont(QFont("Arial", 12))
        self.input_field.setText(str(default))
        layout.addWidget(self.input_field)

        button_layout = QHBoxLayout()
        ok_button = QPushButton("OK", self)
        ok_button.setFont(QFont("Arial", 12))
        ok_button.clicked.connect(self.accept)
        button_layout.addWidget(ok_button)

        cancel_button = QPushButton("Cancel", self)
        cancel_button.setFont(QFont("Arial", 12))
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(cancel_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)

    def get_input_number(self):
        try:
            return int(self.input_field.text())
        except ValueError:
            return None


class PasswordDialog(QDialog):
    def __init__(self, password, icon_path, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Generated Password")
        self.setWindowIcon(QIcon(icon_path))  # Use the bundled icon
        self.setGeometry(200, 200, 400, 200)

        layout = QVBoxLayout()
        label = QLabel(f"Your strong password:\n{password}", self)
        label.setFont(QFont("Arial", 12))
        label.setWordWrap(True)
        layout.addWidget(label)

        button_layout = QHBoxLayout()
        copy_button = QPushButton("Copy", self)
        copy_button.setFont(QFont("Arial", 12))
        copy_button.clicked.connect(lambda: self.copy_to_clipboard(password))
        button_layout.addWidget(copy_button)

        ok_button = QPushButton("OK", self)
        ok_button.setFont(QFont("Arial", 12))
        ok_button.clicked.connect(self.accept)
        button_layout.addWidget(ok_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)

    def copy_to_clipboard(self, text):
        clipboard = QApplication.clipboard()
        clipboard.setText(text)
        QMessageBox.information(self, "Copied", "Password copied to clipboard!")


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Enable dark mode
    app.setStyle("Fusion")
    dark_palette = app.palette()
    dark_palette.setColor(app.palette().Window, QColor(53, 53, 53))
    dark_palette.setColor(app.palette().WindowText, QColor(255, 255, 255))
    dark_palette.setColor(app.palette().Base, QColor(35, 35, 35))
    dark_palette.setColor(app.palette().AlternateBase, QColor(53, 53, 53))
    dark_palette.setColor(app.palette().Text, QColor(255, 255, 255))
    dark_palette.setColor(app.palette().Button, QColor(53, 53, 53))
    dark_palette.setColor(app.palette().ButtonText, QColor(255, 255, 255))
    app.setPalette(dark_palette)

    window = PasswordCheckerApp()
    window.show()
    sys.exit(app.exec_())
