from PySide6.QtWidgets import QWidget, QLabel,QPushButton, QGridLayout


class ModalMessageBox(QWidget):
    def __init__(self, parent,message:str):
        super().__init__(parent)
        
        grid = QGridLayout(self)

        self.message_label = QLabel(message,parent)

        self.ok_button = QPushButton("OK",parent)
        self.ok_button.clicked.connect(self.parent().close)
