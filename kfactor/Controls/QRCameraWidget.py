import cv2
from pyzbar.pyzbar import decode
from PySide6.QtCore import Slot, QTimer,Signal,QPoint
from PySide6.QtGui import QImage, QPixmap, QPainter, QColor,QPen
from PySide6.QtWidgets import QApplication, QTextEdit,QLabel, QVBoxLayout, QWidget

class QRCameraWidget(QWidget):
    codeScanned = Signal(str)

    def __init__(self):
        super().__init__()

        self.camera_label = QLabel(self)
        self.camera_label.setScaledContents(True)

        self.qr_result = QTextEdit(self)
        self.qr_result.setReadOnly(True)

        layout = QVBoxLayout(self)
        layout.addWidget(self.camera_label)
        layout.addWidget(self.qr_result)
        self.setLayout(layout)

        self.cap = cv2.VideoCapture(0)  # Open default camera (usually laptop camera)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(50)  # Update every 50 milliseconds

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
    w = CameraWidget()
    w.show()
    app.exec()