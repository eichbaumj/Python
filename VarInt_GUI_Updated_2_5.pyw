from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QGridLayout, QPushButton, QLineEdit, QLabel, QMenuBar, QMenu, QAction, QTextEdit, QDialog, QStackedWidget, QHBoxLayout)
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt
import sys
import base64
import time


class VarIntCalculator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("VarInt Calculator")
        self.setWindowIcon(QIcon("icon.ico"))
        self.setFixedSize(400, 380)

        # Main widget and layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout()
        self.central_widget.setLayout(self.main_layout)

        # Input field
        self.entry = QLineEdit()
        self.entry.setPlaceholderText("Enter value here...")
        self.entry.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.entry.setFixedHeight(40)
        self.main_layout.addWidget(self.entry)

        # Button grid layout
        self.button_grid = QGridLayout()
        buttons = [
            ("A", 1, 0), ("1", 1, 1), ("2", 1, 2), ("3", 1, 3),
            ("B", 2, 0), ("4", 2, 1), ("5", 2, 2), ("6", 2, 3),
            ("C", 3, 0), ("7", 3, 1), ("8", 3, 2), ("9", 3, 3),
            ("D", 4, 0), ("E", 4, 1), ("F", 4, 2), ("0", 4, 3),
            ("Clear", 5, 0), ("VarInt", 5, 1), ("Integer", 5, 2), ("Length", 5, 3)
        ]

        for text, row, col in buttons:
            button = QPushButton(text)
            button.setFixedSize(80, 50)
            if text in ["A", "B", "C", "D", "E", "F"]:
                button.setStyleSheet("background-color: #003366; color: white; font-weight: bold;")
            elif text == "Clear":
                button.setStyleSheet("background-color: #ff6347; color: white; font-weight: bold;")
            elif text in ["VarInt", "Integer", "Length"]:
                button.setStyleSheet("background-color: #4682b4; color: white; font-weight: bold;")
            else:
                button.setStyleSheet("background-color: #d3d3d3; color: black; font-weight: bold;")
            button.clicked.connect(lambda checked, t=text: self.on_button_click(t))
            self.button_grid.addWidget(button, row, col)

        self.main_layout.addLayout(self.button_grid)

        # Status bar
        self.status_bar = QLabel("Ready")
        self.status_bar.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.main_layout.addWidget(self.status_bar)

        # Menu bar
        self.menu_bar = QMenuBar(self)
        self.setMenuBar(self.menu_bar)

        file_menu = QMenu("File", self)
        self.menu_bar.addMenu(file_menu)
        close_action = QAction("Close", self)
        close_action.triggered.connect(self.close)
        file_menu.addAction(close_action)

        options_menu = QMenu("Options", self)
        self.menu_bar.addMenu(options_menu)
        self.classic_action = QAction("Classic", self, checkable=True)
        self.classic_action.triggered.connect(self.toggle_theme)
        self.classic_action.setChecked(True)
        options_menu.addAction(self.classic_action)
        self.dark_mode_action = QAction("Dark Mode", self, checkable=True)
        self.dark_mode_action.triggered.connect(self.toggle_theme)
        options_menu.addAction(self.dark_mode_action)
        self.retro_green_action = QAction("Retro Green", self, checkable=True)
        self.retro_green_action.triggered.connect(self.toggle_theme)
        options_menu.addAction(self.retro_green_action)

        view_menu = QMenu("View", self)
        self.menu_bar.addMenu(view_menu)
        history_action = QAction("History", self)
        history_action.triggered.connect(self.toggle_history)
        view_menu.addAction(history_action)

        help_menu = QMenu("Help", self)
        self.menu_bar.addMenu(help_menu)
        about_action = QAction("About", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
        tutorial_action = QAction("VarInt Tutorial", self)
        tutorial_action.triggered.connect(self.show_varint_tutorial)
        help_menu.addAction(tutorial_action)

        # History log
        self.history = []
        self.history_window = None

        # Shortcut to clear input field
        self.entry.setFocus()
        self.entry.setShortcutEnabled(True)
        self.shortcut_escape = QAction(self)
        self.shortcut_escape.setShortcut(Qt.Key_Escape)
        self.shortcut_escape.triggered.connect(self.clear_entry)
        self.addAction(self.shortcut_escape)

    def clear_entry(self):
        self.entry.clear()
        self.status_bar.setText("Cleared input field")

    def on_button_click(self, text):
        if text == "Clear":
            self.clear_entry()
        elif text == "VarInt":
            try:
                decimal_value = int(self.entry.text())
                encoded_value = self.encode_varint(decimal_value)
                self.entry.setText(encoded_value)
                self.status_bar.setText("Converted to VarInt")
                self.add_to_history(f"Decimal to VarInt: {decimal_value} -> {encoded_value}")
            except ValueError:
                self.status_bar.setText("Error: Invalid Decimal Value")
        elif text == "Integer":
            hex_value = self.clean_hex_input(self.entry.text())
            try:
                decoded_value = self.decode_varint(hex_value)
                self.entry.setText(str(decoded_value))
                self.status_bar.setText("Converted to Integer")
                self.add_to_history(f"Hex to Integer: {hex_value} -> {decoded_value}")
            except ValueError:
                self.status_bar.setText("Error: Invalid Hex Value")
        elif text == "Length":
            hex_value = self.clean_hex_input(self.entry.text())
            try:
                decoded_value = self.decode_varint(hex_value)
                if decoded_value >= 13 and decoded_value % 2 == 1:
                    length = (decoded_value - 13) // 2
                    self.entry.setText(f"String Length: {length}")
                    self.status_bar.setText("String length calculated")
                    self.add_to_history(f"String Length from VarInt: {hex_value} -> {length}")
                elif decoded_value >= 12 and decoded_value % 2 == 0:
                    length = (decoded_value - 12) // 2
                    self.entry.setText(f"BLOB Length: {length}")
                    self.status_bar.setText("BLOB length calculated")
                    self.add_to_history(f"BLOB Length from VarInt: {hex_value} -> {length}")
                else:
                    self.entry.setText("Invalid for String/BLOB")
                    self.status_bar.setText("Invalid length value for String/BLOB")
            except ValueError:
                self.status_bar.setText("Error: Invalid Hex Value")
        else:
            current_text = self.entry.text()
            self.entry.setText(current_text + text)

    def clean_hex_input(self, hex_string):
        return hex_string.replace(" ", "")

    def decode_varint(self, hex_string):
        if len(hex_string) % 2 != 0:
            raise ValueError("Invalid Hex Value")
        bytes_array = [int(hex_string[i:i+2], 16) for i in range(0, len(hex_string), 2)]
        value = 0
        for byte in bytes_array:
            value = (value << 7) | (byte & 0x7F)
            if byte & 0x80 == 0:
                break
        return value

    def encode_varint(self, value):
        if value < 0:
            raise ValueError("Value must be non-negative")
        result = []
        while True:
            byte = value & 0x7F
            value >>= 7
            if result:
                byte |= 0x80
            result.insert(0, byte)
            if value == 0:
                break
        return ''.join(f'{byte:02X}' for byte in result)

    def toggle_theme(self):
        sender = self.sender()
        self.classic_action.setChecked(sender == self.classic_action)
        self.dark_mode_action.setChecked(sender == self.dark_mode_action)
        self.retro_green_action.setChecked(sender == self.retro_green_action)

        if sender == self.dark_mode_action and sender.isChecked():
            self.central_widget.setStyleSheet("background-color: #2e2e2e; color: white;")
            self.entry.setStyleSheet("background-color: #333333; color: white;")
            for i in range(self.button_grid.count()):
                button = self.button_grid.itemAt(i).widget()
                if button.text() == "Clear":
                    button.setStyleSheet("background-color: #ff6347; color: white; font-weight: bold;")
                elif button.text() in ["A", "B", "C", "D", "E", "F"]:
                    button.setStyleSheet("background-color: #003366; color: white; font-weight: bold;")
                elif button.text() in ["VarInt", "Integer", "Length"]:
                    button.setStyleSheet("background-color: #4682b4; color: white; font-weight: bold;")
                else:
                    button.setStyleSheet("background-color: #777777; color: black; font-weight: bold;")
        elif sender == self.retro_green_action and sender.isChecked():
            self.central_widget.setStyleSheet("background-color: #0f0f0f; color: #00ff00;")
            self.entry.setStyleSheet("background-color: #0f0f0f; color: #00ff00;")
            for i in range(self.button_grid.count()):
                button = self.button_grid.itemAt(i).widget()
                button.setStyleSheet("background-color: #001100; color: #00ff00; font-weight: bold;")
        else:
            self.central_widget.setStyleSheet("")
            self.entry.setStyleSheet("")
            for i in range(self.button_grid.count()):
                button = self.button_grid.itemAt(i).widget()
                if button.text() == "Clear":
                    button.setStyleSheet("background-color: #ff6347; color: white; font-weight: bold;")
                elif button.text() in ["A", "B", "C", "D", "E", "F"]:
                    button.setStyleSheet("background-color: #003366; color: white; font-weight: bold;")
                elif button.text() in ["VarInt", "Integer", "Length"]:
                    button.setStyleSheet("background-color: #4682b4; color: white; font-weight: bold;")
                else:
                    button.setStyleSheet("background-color: #d3d3d3; color: black; font-weight: bold;")

    def show_about(self):
        about_dialog = QDialog(self)
        about_dialog.setWindowTitle("About VarInt Calculator")
        about_dialog.setWindowIcon(QIcon("icon.ico"))
        about_dialog.setStyleSheet("background-color: #1B293B; color: white;")

        about_layout = QVBoxLayout()

        # Company Logo
        logo_label = QLabel()
        logo_pixmap = QPixmap("logo.png")
        logo_scaled_pixmap = logo_pixmap.scaled(500, 72, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        logo_label.setPixmap(logo_scaled_pixmap)
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        about_layout.addWidget(logo_label)

        about_text = QLabel("VarInt Calculator v3.0\nCreated by James Eichbaum\n© Elusive Data 2024")
        about_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        about_layout.addWidget(about_text)

        about_dialog.setLayout(about_layout)
        about_dialog.setFixedSize(550, 300)
        about_dialog.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
        about_dialog.exec_()

    def show_varint_tutorial(self):
        self.tutorial_step = 0
        self.tutorial_steps = [
            "<h2>Step 1: Convert each hex value to binary</h2><p>Example Hex: 81 20</p><ul><li>81 -> <span style='color: #00ff00;'>10000001</span></li><li>20 -> <span style='color: #00ff00;'>00100000</span></li></ul>",
            "<h2>Step 2: Drop the most significant bit (MSB) from each byte</h2><ul><li><span style='color: #ff6347;'>10000001</span> -> <span style='color: #00ff00;'>0000001</span></li><li><span style='color: #ff6347;'>00100000</span> -> <span style='color: #00ff00;'>0100000</span></li></ul>",
            "<h2>Step 3: Concatenate the remaining bits</h2><p>Result: <span style='color: #00ff00;'>0000001 0100000</span></p>",
            "<h2>Step 4: Pad with zeros on the left as needed to form the correct number</h2><p>Result: <span style='color: #00ff00;'>00000000 10100000</span></p>",
            "<h2>Step 5: Convert the binary value to hex</h2><p><span style='color: #00ff00;'>00000000 10100000</span> -> 00A0</p>",
            "<h2>Step 6: Finally, convert hex to decimal</h2><p>00A0 -> 160</p><p>The decimal representation of the varint value is: <strong>160</strong></p>"
        ]
        
        self.tutorial_dialog = QDialog(self)
        self.tutorial_dialog.setWindowTitle("VarInt Tutorial")
        self.tutorial_dialog.setWindowIcon(QIcon("icon.ico"))
        self.tutorial_dialog.setStyleSheet("background-color: #1B293B; color: white;")
        self.tutorial_layout = QVBoxLayout()

        self.tutorial_text = QTextEdit()
        self.tutorial_text.setReadOnly(True)
        self.tutorial_text.setStyleSheet("background-color: #1B293B; color: white; font-size: 14px;")
        self.tutorial_text.setHtml(self.tutorial_steps[self.tutorial_step])
        self.tutorial_layout.addWidget(self.tutorial_text)

        self.navigation_layout = QHBoxLayout()
        self.previous_button = QPushButton("Previous")
        self.previous_button.clicked.connect(self.previous_step)
        self.previous_button.setEnabled(False)
        self.navigation_layout.addWidget(self.previous_button)
        
        self.next_button = QPushButton("Next")
        self.next_button.clicked.connect(self.next_step)
        self.navigation_layout.addWidget(self.next_button)

        self.tutorial_layout.addLayout(self.navigation_layout)
        
        self.tutorial_dialog.setLayout(self.tutorial_layout)
        self.tutorial_dialog.setFixedSize(550, 450)
        self.tutorial_dialog.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
        self.tutorial_dialog.exec_()

    def next_step(self):
        self.tutorial_step += 1
        if self.tutorial_step >= len(self.tutorial_steps) - 1:
            self.next_button.setEnabled(False)
        self.previous_button.setEnabled(True)
        self.tutorial_text.setHtml(self.tutorial_steps[self.tutorial_step])

    def previous_step(self):
        self.tutorial_step -= 1
        if self.tutorial_step <= 0:
            self.previous_button.setEnabled(False)
        self.next_button.setEnabled(True)
        self.tutorial_text.setHtml(self.tutorial_steps[self.tutorial_step])

    def add_to_history(self, action):
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        self.history.append(f"[{timestamp}] {action}")
        self.status_bar.setText(f"History updated - {len(self.history)} entries")
        if self.history_window and self.history_window.isVisible():
            self.history_text.setPlainText("\n".join(self.history))

    def toggle_history(self):
        if self.history_window is None or not self.history_window.isVisible():
            self.history_window = QWidget()
            self.history_window.setWindowTitle("History")
            self.history_window.setWindowIcon(QIcon("icon.ico"))
            self.history_window.setGeometry(100, 100, 600, 400)
            history_layout = QVBoxLayout()
            self.history_text = QTextEdit()
            self.history_text.setReadOnly(True)
            self.history_text.setPlainText("\n".join(self.history))
            history_layout.addWidget(self.history_text)
            self.history_window.setLayout(history_layout)
        else:
            self.history_text.setPlainText("\n".join(self.history))
        self.history_window.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VarIntCalculator()
    window.show()
    sys.exit(app.exec())
