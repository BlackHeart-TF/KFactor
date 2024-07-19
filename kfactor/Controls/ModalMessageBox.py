from PySide6.QtWidgets import QWidget, QLabel,QPushButton, QGridLayout
from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QPainter

class ModalMessageBox(QWidget):
    def __init__(self, parent,message:str,x:int,y:int):
        super().__init__(parent)
        self.setFixedSize(x,y)
        grid = QGridLayout(self)

        self.message_label = QLabel(message,parent)

        self.ok_button = QPushButton("OK",parent)
        self.ok_button.clicked.connect(self.parent().close)

        grid.addWidget(self.message_label,0,0,1,3)
        grid.addWidget(self.ok_button,1,2)
        self.setLayout(grid)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(self.palette().window().color())
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(self.rect(), 10, 10)

class ModalConfirmationBox(QWidget):
    responded = Signal(bool)

    def __init__(self, parent,message:str,x:int,y:int):
        super().__init__(parent)
        self.setFixedSize(x,y)
        grid = QGridLayout(self)

        self.message_label = QLabel(message,parent)

        self.yes_button = QPushButton("Yes",parent)
        self.yes_button.clicked.connect(self.Yes)

        self.no_button = QPushButton("No",parent)
        self.no_button.clicked.connect(self.No)

        grid.addWidget(self.message_label,0,0,1,3)
        grid.addWidget(self.yes_button,1,2)
        grid.addWidget(self.no_button,1,1)
        self.setLayout(grid)

    def Yes(self):
        self.responded.emit(True)
        self.parent().close
    
    def No(self):
        self.responded.emit(False)
        self.parent().close

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(self.palette().window().color())
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(self.rect(), 10, 10)