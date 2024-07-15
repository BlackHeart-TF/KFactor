from PySide6.QtWidgets import QWidget,QVBoxLayout,QLabel
from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter, QColor
from Function.SerialReader import SerialReader
from Function.Config import Config

class SerialScanBarcodePanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.code:str = None

        self.serial = SerialReader()
        self.serial.barcode_read.connect(self.barcodeRead)

        palette = self.palette()
        self.window_color = palette.window().color()
        self.window_text_color = palette.windowText().color()
        self.setObjectName("ContentPanel")
        self.setStyleSheet(f"""QWidget {{
                           color: {self.window_text_color.name()}
                           }}
                            #ContentPanel {{
                            border-radius: 10px; 
                            padding: 10px; 
                            background-color: {self.window_color.name()};
                            }} 
                            QLabel {{
                                font-size:24pt
                            }}
                           """)
        
        color = self.palette().window()
        self.setFixedSize(300,100)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_ShowWithoutActivating)
        layout = QVBoxLayout(self)
        self.label = QLabel("Scan Barcode")
        layout.addWidget(self.label,alignment=Qt.AlignCenter)
        self.setLayout(layout)

    def barcodeRead(self,code):
        #print(code)
        self.code = code
        self.parent().hide()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(self.window_color)
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(self.rect(), 10, 10)

    def showEvent(self,event):
        port = Config.get("SerialPort")
        baud = Config.get("SerialBaud")
        if port and baud:
            self.serial.start(port,baud)
        else:
            self.label.setText("Port not set")

    def hideEvent(self,event):
        self.serial.stop()