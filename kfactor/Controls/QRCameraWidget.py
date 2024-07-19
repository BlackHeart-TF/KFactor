
from PySide6.QtCore import Qt, Slot, QTimer,Signal,QPoint,QEvent
from PySide6.QtGui import QImage, QPixmap, QPainter, QColor,QPen
from PySide6.QtWidgets import QApplication, QPushButton,QLabel, QGridLayout, QWidget,QSizePolicy
from Function.Config import Config

class QRCameraWidget(QWidget):
    import cv2
    from pyzbar.pyzbar import decode

    codeScanned = Signal(str)

    def __init__(self,parent=None):
        super().__init__(parent)

        self.setSizePolicy(QSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding))

        self.camera_label = QLabel(self)
        self.camera_label.setScaledContents(True)

        self.back_button = QPushButton("Back")
        self.back_button.clicked.connect(self.close)

        self.layout = QGridLayout(self)
        self.layout.addWidget(self.camera_label,0,0)
        self.layout.addWidget(self.back_button,0,0,alignment=Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignTop)
        self.setLayout(self.layout)

        
        if parent:
            self.setParent(parent)
            self.resize(parent.size())
            parent.installEventFilter(self)

    def showEvent(self,event):
        index = Config.get("CameraIDX")
        if index is not None:
            self.cap = QRCameraWidget.cv2.VideoCapture(index)
        if not index or not self.cap.isOpened():
            oops = QLabel()
            oops.setText("No Camera detected")
            oops.setStyleSheet("font-size: 24px; font-weight: bold;")
            self.layout.addWidget(oops,0,0,alignment=Qt.AlignmentFlag.AlignCenter|Qt.AlignmentFlag.AlignHCenter)
        else:
            self.timer = QTimer(self)
            self.timer.timeout.connect(self.update_frame)
            self.timer.start(50)  # Update every 50 milliseconds
            

    def eventFilter(self, obj, event):
        if obj == self.parent() and event.type() == QEvent.Resize:
            self.resize(obj.size())  # Resize the overlay to match the parent's size
        return super().eventFilter(obj, event)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(self.palette().window().color())
        painter.setPen(Qt.NoPen)
        painter.drawRect(self.rect())

    @Slot()
    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert OpenCV image (BGR) to QImage (RGB)
            h, w, ch = frame.shape
            img = QImage(frame.data, w, h, ch * w, QImage.Format_RGB888)
            decoded_objects = decode(frame)
            if decoded_objects:
                self.timer.stop()
                obj = decoded_objects[0]
                self.highlight_qr_code(img,obj)
                self.codeScanned.emit(obj.data.decode('utf-8'))
                self.cap.release()
                QTimer.singleShot(2000, self.close)
            
            pixmap = QPixmap.fromImage(img)
            self.camera_label.setPixmap(pixmap)

            
    def highlight_qr_code(self, frame, obj):
        # Extract the bounding box coordinates of the QR code
        bbox_points = obj.polygon

        # Convert bbox_points to tuple of QPoint for use with QPainter
        bbox_qpoints = [QPoint(p[0], p[1]) for p in bbox_points]

        # Draw a red rectangle around the QR code
        painter = QPainter(frame)
        pen = QPen(QColor(0, 255, 0))  # Green color
        pen.setWidth(5)  # Set the line thickness (5 pixels in this case)
        painter.setPen(pen)
        painter.drawPolygon(bbox_qpoints)
        painter.end()


if __name__ == "__main__":
    app = QApplication()
    w = QRCameraWidget()
    w.show()
    app.exec()