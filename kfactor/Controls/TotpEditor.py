from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QFormLayout, QLineEdit, QPushButton, QSpinBox, QSizePolicy,
    QLabel, QComboBox
)
from PySide6.QtGui import QIcon,QPainter
from PySide6.QtCore import QSize, Qt,Signal
from GAuth.TotpCode import Algorithm,TotpCode

class TOTPEditor(QWidget):
    totpSaved = Signal(TotpCode)

    def __init__(self):
        super().__init__()

        self.setWindowTitle("TOTP Manual Entry")
        self.setFixedHeight(250)
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
        self.combo_box.setCurrentIndex(0)
        self.combo_box.setEnabled(False)
        # Add form fields to layout
        form_layout.addRow("Name:", self.name_input)
        form_layout.addRow("Base32 Key:", self.secret_input)
        form_layout.addRow("Issuer:", self.issuer_input)
        form_layout.addRow("Period:", self.period_input)
        form_layout.addRow("Digits:", self.digits_input)
        form_layout.addRow("Algorithm:", self.combo_box)

        layout.addLayout(form_layout)

        # Create submit button
        submit_button = QPushButton("Submit")
        submit_button.clicked.connect(self.submit)

        layout.addWidget(submit_button, alignment=Qt.AlignHCenter)

        # Set the layout
        self.setLayout(layout)
        self.setSizePolicy(QSizePolicy.Policy.Minimum,QSizePolicy.Policy.Minimum)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(self.palette().window().color())
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(self.rect(), 10, 10)

    def load(self,totp:TotpCode):
        self.name_input.setText(totp.account)
        self.secret_input.setText(totp.secret)
        self.issuer_input.setText(totp.issuer)
        self.period_input.setValue(totp.period)
        self.digits_input.setValue(totp.digits)
        self.combo_box.setCurrentIndex(self.combo_box.findData(totp.algorithm))

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
        totp = TotpCode(name,secret,issuer,algorithm,digits,period)
        self.totpSaved.emit(totp)
        self.parent().close()


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
