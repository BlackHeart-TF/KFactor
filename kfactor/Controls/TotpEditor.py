from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QFormLayout, QLineEdit, QPushButton, QSpinBox,
    QLabel, QComboBox
)
from PySide6.QtGui import QIcon,QPainter
from PySide6.QtCore import QSize, Qt
from GAuth.TotpCode import Algorithm

class TOTPEditor(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("TOTP Manual Entry")

        # Create layout
        layout = QVBoxLayout()

        # Create form layout
        form_layout = QFormLayout()

        # Create form fields
        self.name_input = QLineEdit()
        self.secret_input = QLineEdit()
        self.issuer_input = QLineEdit()
        self.period_input = QSpinBox()
        self.period_input.setRange(1, 60)
        self.period_input.setValue(30)
        self.digits_input = QSpinBox()
        self.digits_input.setRange(1, 10)
        self.digits_input.setValue(6)
        self.combo_box = QComboBox()
        self.combo_box.addItem("SHA1", Algorithm.SHA1)
        self.combo_box.addItem("SHA256", Algorithm.SHA256)
        self.combo_box.addItem("SHA512", Algorithm.SHA512)
        self.combo_box.addItem("MD5", Algorithm.MD5)
        # Add form fields to layout
        form_layout.addRow("Name:", self.name_input)
        form_layout.addRow("Secret Key:", self.secret_input)
        form_layout.addRow("Issuer:", self.issuer_input)
        form_layout.addRow("Period:", self.period_input)
        form_layout.addRow("Digits:", self.digits_input)
        form_layout.addRow("Algorithm:", self.combo_box)

        layout.addLayout(form_layout)

        # Create submit button
        submit_button = QPushButton("Submit")
        submit_button.clicked.connect(self.submit)

        layout.addWidget(submit_button, alignment=Qt.AlignCenter)

        # Set the layout
        self.setLayout(layout)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(self.palette().window().color())
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(self.rect(), 10, 10)

    def submit(self):
        # Collect data from inputs
        name = self.name_input.text()
        secret = self.secret_input.text()
        issuer = self.issuer_input.text()
        period = self.period_input.value()
        digits = self.digits_input.value()
        algorithm = self.combo_box.itemData(self.combo_box.currentIndex())

        # Print collected data (for now, can be replaced with further processing)
        print(f"Name: {name}")
        print(f"Secret Key: {secret}")
        print(f"Issuer: {issuer}")
        print(f"Period: {period}")
        print(f"Digits: {digits}")
        print(f"Algorithm: {algorithm} ({Algorithm.toAlgoString(algorithm)})")

        # Clear inputs after submission
        self.name_input.clear()
        self.secret_input.clear()
        self.issuer_input.clear()
        self.period_input.setValue(1)
        self.digits_input.setValue(1)
        self.combo_box.setCurrentIndex(0)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("TOTP Entry Form Example")

        # Set the central widget
        self.setCentralWidget(TOTPEditor())


if __name__ == "__main__":
    app = QApplication([])

    window = MainWindow()
    window.show()

    app.exec()
