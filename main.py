from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMainWindow, QListWidget, QVBoxLayout, QHBoxLayout, QPushButton, QWidget,QListWidgetItem,QLabel,QGridLayout,QFrame


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle("Resizable Sidebar Example")
        self.setGeometry(100, 100, 800, 600)

        mainWidget = QWidget()
        self.setCentralWidget(mainWidget)

        layout = QHBoxLayout(mainWidget)

        # Create a sidebar widget
        self.sidebar = QWidget()
        self.sidebar.setObjectName("sidebar")
        self.sidebar.setStyleSheet("#sidebar{background-color: #22ffffff; border-radius:0px;}")
        self.sidebar.setMaximumWidth(400)
        # Create a main widget
        self.listWidget = QListWidget()
        
        # Create a layout for the sidebar
        sidebarLayout = QVBoxLayout(self.sidebar)
        layout.setContentsMargins(0, 0, 0, 0)

        # Add buttons to the sidebar (for demonstration purposes)
        button1 = QPushButton("Add")
        button4 = QPushButton("Remove")
        button2 = QPushButton("Import")
        button3 = QPushButton("Export")
        sidebarLayout.addWidget(button1)
        sidebarLayout.addWidget(button4)
        sidebarLayout.addSpacing(25)
        sidebarLayout.addWidget(button2)
        sidebarLayout.addWidget(button3)
        sidebarLayout.addStretch(1)

        layout.addWidget(self.sidebar)
        layout.addWidget(self.listWidget)

        # Toggle sidebar visibility based on window size
        self.updateSidebarVisibility()
        self.resizeEvent = self.customResizeEvent

    def addItem(self,code):
        item = QListWidgetItem()

        frame = QFrame()
        frame.setFrameShape(QFrame.StyledPanel)
        frame.setFrameShadow(QFrame.Raised)
        frame.setLineWidth(2)
        widget_layout = QGridLayout(frame)
        widget_layout.setSpacing(0)
        widget_layout.setContentsMargins(0,0,0,0)
        # Title label
        title_label = QLabel(code["title"])
        widget_layout.addWidget(title_label,0,0)

        # Large number area (assuming as QLabel)
        number_label = QLabel(str(code["number"]))
        number_label.setAlignment(Qt.AlignTop | Qt.AlignLeft) 
        number_label.setStyleSheet("font-size: 24px;")
        widget_layout.addWidget(number_label,1,0)

        # Progress bar
        #progress_bar = QProgressBar()
        #progress_bar.setValue(code["progress"])
        #widget_layout.addWidget(progress_bar)

        item.setSizeHint(frame.sizeHint())  # Adjust item size
        self.listWidget.addItem(item)
        self.listWidget.setItemWidget(item, frame)

    def customResizeEvent(self, event):
        # Override the resize event to handle sidebar visibility
        self.updateSidebarVisibility()
        return QMainWindow.resizeEvent(self, event)

    def updateSidebarVisibility(self):
        # Check if the window width is less than the height
        if self.width() > 600:
            self.sidebar.show()
        else:
            self.sidebar.hide()


if __name__ == "__main__":
    import sys
    from PySide6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    window.addItem({"title":"Secrets","number":123456})
    window.addItem({"title":"More Secrets","number":654321})
    sys.exit(app.exec())
