import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QLineEdit, QPushButton, QHBoxLayout, QTableView, QWidget, QFrame, QGridLayout,QSizePolicy
from PySide6.QtCore import Qt,QPropertyAnimation,Property,QSequentialAnimationGroup,QPauseAnimation,QEvent,QEasingCurve
from PySide6.QtGui import QColor, QPalette,QPainter
from time import sleep

class ModalOverlay(QWidget):
    def __init__(self, parent,content=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setStyleSheet("ModelOverlay {background-color: rgba(0, 0, 0, 0.5);}")
        self.setSizePolicy(QSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding))
        #self.setGeometry(0,0,parent.size().width(),parent.size().height())

        self._opacity = 0

        # Set up the animation for the custom opacity property
        self.fadeInAnimation = QPropertyAnimation(self, b"opacity")
        self.fadeInAnimation.setDuration(450)  # The fade duration is quicker
        self.fadeInAnimation.setStartValue(0)
        self.fadeInAnimation.setEndValue(100)  # Target alpha value (0-255)
        self.fadeInAnimation.setEasingCurve(QEasingCurve.InOutQuad)
        # Prepare a sequential animation group with a pause and then the fade-in
        self.animationSequence = QSequentialAnimationGroup(self)
        #self.animationSequence.addAnimation(QPauseAnimation(150))  # Pause for 0.2 seconds
        self.animationSequence.addAnimation(self.fadeInAnimation)

        self.contentContainer = QWidget(self)
        self.contentContainer.setObjectName("contentContainer")
        self.contentContainer.setStyleSheet("#contentContainer {border-radius: 10px; padding: 10px;}")

        # Layout for the content container
        contentLayout = QGridLayout(self.contentContainer)
        self.content = content if content else self.createSampleWidget()
        contentLayout.addWidget(self.content, 1, 1)
        self.setLayout(contentLayout)
        # Add the content container to the main widget's layout, in the middle cell
        self.layout().addWidget(self.contentContainer, 1, 1)

        # Set stretch factors to center the content container
        self.layout().setColumnStretch(0, 1)
        self.layout().setColumnStretch(1, 3)
        self.layout().setColumnStretch(2, 1)
        self.layout().setRowStretch(0, 1)
        self.layout().setRowStretch(1, 3)
        self.layout().setRowStretch(2, 1)

        # Clicking outside the content widget closes the overlay
        self.mousePressEvent = lambda event: self.close()

        if parent:
            self.setParent(parent)
            self.resize(parent.size())
            parent.installEventFilter(self)

    def eventFilter(self, obj, event):
        if obj == self.parent() and event.type() == QEvent.Resize:
            self.resize(obj.size())  # Resize the overlay to match the parent's size
        return super().eventFilter(obj, event)

    @Property(float)
    def opacity(self):
        return self._opacity

    @opacity.setter
    def opacity(self, value):
        self._opacity = value
        self.update() 

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setBrush(QColor(0, 0, 0, self._opacity))  # Semi-transparent black
        painter.setPen(Qt.NoPen)  # No border
        painter.drawRect(self.rect())  # Cover the entire widget area
    
    def showEvent(self, event: QEvent):
        super().showEvent(event)
        self._alpha = 0  # Reset alpha to 0 every time the widget is shown
        self.animationSequence.start() 

    def createSampleWidget(self):
        # Create the central content widget with arbitrary contents
        widget = QWidget(self)

        widgetLayout = QVBoxLayout(widget)

        textbox = QLineEdit(widget)
        widgetLayout.addWidget(textbox)

        buttonsLayout = QHBoxLayout()
        for i in range(1, 4):
            button = QPushButton(f'Button {i}', widget)
            buttonsLayout.addWidget(button)
        widgetLayout.addLayout(buttonsLayout)

        tableView = QTableView(widget)
        widgetLayout.addWidget(tableView)

        widget.setFixedSize(400, 300)
        return widget
    
    def Wait(self):
        while self.isVisible():
            QApplication.processEvents()

if __name__ == "__main__":
    class CentralWidget(QWidget):
        def __init__(self, parent=None):
            super().__init__(parent)
            self.mlayout = QVBoxLayout(self)

            # Placeholder content in main window
            self.placeholderButton = QPushButton("Open Modal Overlay", self)
            self.placeholderButton.clicked.connect(self.showModalOverlay)
            self.mlayout.addWidget(self.placeholderButton)

        def showModalOverlay(self):
            self.overlay = ModalOverlay(self.parent())
            self.overlay.show()


