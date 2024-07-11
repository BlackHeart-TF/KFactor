from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QCheckBox, QComboBox, QSizePolicy
)
from PySide6.QtGui import QPainter, QColor
from PySide6.QtCore import Qt
import sys
import serial.tools.list_ports
from Function.SerialReader import SerialReader
from Function.Config import Config

class SettingsPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setObjectName("SettingsPage")
        
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_ShowWithoutActivating)
        self.setFixedSize(300,130)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        title_label = QLabel("Settings", self)
        palette = self.palette()
        self.window_color = palette.window().color()
        self.window_text_color = palette.windowText().color()
        self.setStyleSheet(f"""QWidget {{
                           color: {self.window_text_color.name()}
                           }}
                            #SettingsPage {{
                            background-color: {self.window_color.name()}
                            }}
                           """)
        
        title_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        layout.addWidget(title_label)

        # Serial Port Dropdown
        serial_layout = QHBoxLayout()
        serial_label = QLabel("Serial Port:", self)
        self.serial_combobox = QComboBox(self)
        self.serial_lineedit = QLineEdit(self)
        self.serial_lineedit.setText("115200")
        self.serial_lineedit.setMaximumWidth(80)
        self.populate_serial_ports()
        serial_layout.addWidget(serial_label)
        serial_layout.addWidget(self.serial_combobox)
        serial_layout.addWidget(self.serial_lineedit)
        layout.addLayout(serial_layout)

        buttons_layout = QHBoxLayout()
        save_button = QPushButton("Ok", self)
        buttons_layout.addWidget(save_button)
        layout.addSpacing(5)
        layout.addLayout(buttons_layout)

        self.setLayout(layout)
        save_button.clicked.connect(lambda: self.parent().close())
        self.serial_combobox.currentIndexChanged.connect(self.save_settings)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(self.window_color)
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(self.rect(), 10, 10)

    def populate_serial_ports(self):
        ports = ["None"]+[port.device for port in serial.tools.list_ports.comports() if 'ttyS' not in port.device]
        for port in ports:
            self.serial_combobox.addItem(port)

    def save_settings(self,event):
        selected_port = self.serial_combobox.currentText()
        selected_baud = int(self.serial_lineedit.text())
        Config.set("SerialPort",selected_port)
        Config.set("SerialBaud",selected_baud)
        


