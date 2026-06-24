"""
main.py
-------
SAGE - Cyber AI Assistant (GUI-Based)

Entry point of the application. Built with PyQt5.

Architecture (matches resume claim of "modular architecture"):
    main.py        -> GUI layer (login window + chat window)
    auth.py        -> authentication logic
    security.py    -> input validation / sanitization
    nlp_engine.py   -> intent matching / response generation
    logger.py      -> activity logging

Run:
    python main.py

First run will prompt you to set up a local username/password
(stored as a SHA-256 hash in credentials.json).
"""

import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QTextEdit, QMessageBox, QInputDialog
)
from PyQt5.QtCore import Qt

import auth
import security
import nlp_engine
import logger


class LoginWindow(QWidget):
    """First screen shown to the user: simple username/password gate."""

    def __init__(self, on_success):
        super().__init__()
        self.on_success = on_success
        self.setWindowTitle("SAGE - Login")
        self.setFixedSize(320, 180)
        self._build_ui()

        if not auth.credentials_exist():
            self._first_time_setup()

    def _build_ui(self):
        layout = QVBoxLayout()

        title = QLabel("SAGE Cyber AI Assistant")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-weight: bold; font-size: 14px;")
        layout.addWidget(title)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")
        layout.addWidget(self.username_input)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_input)

        login_btn = QPushButton("Login")
        login_btn.clicked.connect(self._attempt_login)
        layout.addWidget(login_btn)

        self.setLayout(layout)

    def _first_time_setup(self):
        QMessageBox.information(
            self, "First-time Setup",
            "No credentials found. Let's create a local login."
        )
        username, ok1 = QInputDialog.getText(self, "Setup", "Choose a username:")
        if not ok1 or not username:
            sys.exit(0)

        password, ok2 = QInputDialog.getText(
            self, "Setup", "Choose a password:", QLineEdit.Password
        )
        if not ok2 or not password:
            sys.exit(0)

        auth.set_initial_credentials(username, password)
        logger.log_event("SYSTEM", "Initial credentials created")
        QMessageBox.information(self, "Setup Complete", "You can now log in.")

    def _attempt_login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        if auth.verify_login(username, password):
            logger.log_event("LOGIN_SUCCESS", f"user={username}")
            self.on_success()
            self.close()
        else:
            logger.log_event("LOGIN_FAILED", f"attempted_user={username}")
            QMessageBox.warning(self, "Login Failed", "Invalid username or password.")


class ChatWindow(QWidget):
    """Main assistant window: chat-style interaction after successful login."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("SAGE - Cyber AI Assistant")
        self.setMinimumSize(480, 420)
        self._build_ui()
        self._display_message("SAGE", "Hello! Type 'help' to see what I can do.")

    def _build_ui(self):
        layout = QVBoxLayout()

        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        layout.addWidget(self.chat_display)

        input_row = QHBoxLayout()
        self.input_box = QLineEdit()
        self.input_box.setPlaceholderText("Type a message...")
        self.input_box.returnPressed.connect(self._handle_user_input)
        input_row.addWidget(self.input_box)

        send_btn = QPushButton("Send")
        send_btn.clicked.connect(self._handle_user_input)
        input_row.addWidget(send_btn)

        layout.addLayout(input_row)
        self.setLayout(layout)

    def _display_message(self, sender: str, message: str):
        self.chat_display.append(f"<b>{sender}:</b> {message}")

    def _handle_user_input(self):
        raw_text = self.input_box.text()
        self.input_box.clear()

        if not raw_text.strip():
            return

        self._display_message("You", raw_text)

        # Step 1: validate input (security.py)
        is_safe, reason = security.validate_input(raw_text)

        if not is_safe:
            logger.log_event("INPUT_BLOCKED", f"input={raw_text!r} reason={reason}")
            self._display_message("SAGE", f"⚠ Input blocked. {reason}")
            return

        # Step 2: sanitize input
        clean_text = security.sanitize_input(raw_text)
        logger.log_event("USER_INPUT", clean_text)

        # Step 3: generate response (nlp_engine.py)
        response = nlp_engine.generate_response(clean_text)

        if response == "__EXIT__":
            self._display_message("SAGE", "Goodbye!")
            logger.log_event("SYSTEM", "User exited application")
            QApplication.quit()
            return

        if response == "__SHOW_LOG__":
            recent = logger.read_recent_logs(10)
            log_text = "".join(recent) if recent else "No log entries yet."
            self._display_message("SAGE", f"<pre>{log_text}</pre>")
            return

        self._display_message("SAGE", response)


def main():
    app = QApplication(sys.argv)

    chat_window = ChatWindow()

    def show_chat():
        chat_window.show()

    login_window = LoginWindow(on_success=show_chat)
    login_window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
