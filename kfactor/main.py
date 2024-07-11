import sys,os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
from PySide6.QtCore import Qt,QTimer
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (QMainWindow, QListWidget, QVBoxLayout, QHBoxLayout, QPushButton, QWidget,QListWidgetItem,QLabel,QGridLayout,QFrame,
                                QProgressBar,QSizePolicy,QMessageBox)
from GAuth.TotpCode import TotpCode
from Function.KeyringHelper import KeyringHelper

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.keyring = KeyringHelper("KFactor")
        self.initUI()

    def initUI(self):
        self.setWindowTitle("KFactor - 2FA Authenticator")
        self.setGeometry(100, 100, 800, 600)

        mainWidget = QWidget()
        self.setCentralWidget(mainWidget)

        layout = QHBoxLayout(mainWidget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Create a sidebar widget
        self.sidebar = QWidget()
        self.sidebar.setObjectName("sidebar")
        self.sidebar.setStyleSheet("#sidebar{ border-radius:0px;}")
        self.sidebar.setMaximumWidth(400)
        # Create a main widget
        mainlayout = QVBoxLayout()
        self.menuButton = QPushButton("☰ KFactor")
        self.menuButton.setStyleSheet("margin: 5px 5px 0px 5px;padding: 0px 5px;font-size: 20px;border:None;")
        self.menuButton.clicked.connect(self.showMenu)
        self.listWidget = QListWidget()
        mainlayout.addWidget(self.menuButton,alignment=Qt.AlignmentFlag.AlignLeft)
        mainlayout.addWidget(self.listWidget)
        
        
        # Create a layout for the sidebar
        sidebarLayout = QVBoxLayout(self.sidebar)
        
        # Add buttons to the sidebar (for demonstration purposes)
        add_icon = QIcon.fromTheme("list-add")
        addButton = QPushButton(add_icon,"Add")
        addButton.clicked.connect(self.addCode)
        remove_icon = QIcon.fromTheme("list-remove")
        button4 = QPushButton(remove_icon,"Remove")
        import_icon = QIcon.fromTheme("document-open")
        button2 = QPushButton(import_icon,"Import")
        export_icon = QIcon.fromTheme("document-save")
        button3 = QPushButton(export_icon,"Export")
        settings_icon = QIcon.fromTheme("preferences-system")
        settingsbutton = QPushButton(settings_icon,"Settings")
        settingsbutton.clicked.connect(self.show_settings)
        sidebarLayout.addWidget(addButton)
        sidebarLayout.addWidget(button4)
        sidebarLayout.addSpacing(25)
        sidebarLayout.addWidget(button2)
        sidebarLayout.addWidget(button3)
        sidebarLayout.addStretch(1)
        sidebarLayout.addWidget(settingsbutton)

        layout.addWidget(self.sidebar)
        layout.addLayout(mainlayout)

        # Toggle sidebar visibility based on window size
        self.updateSidebarVisibility()
        self.resizeEvent = self.customResizeEvent

        # Setup QTimer to refresh every 5 seconds
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_list)
        
    def show_error(self,message:str):
        print(message)
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Critical)
        msg_box.setText(message)
        msg_box.setWindowTitle("Error")
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.exec()

    def addCode(self,event):
        from Controls.ModalOverlay import ModalOverlay
        from Controls.SerialScanBarcodePanel import SerialScanBarcodePanel
        dlg = ModalOverlay(self,SerialScanBarcodePanel())
        dlg.show()
        dlg.Wait()
        if dlg.content.code and dlg.content.code.lower().startswith("otpauth"):
            totp = TotpCode.from_otpauth(dlg.content.code)
            if totp:
                self.addItem(totp)
            else:
                self.show_error("Error Parsing Code")
        elif dlg.content.code:
            print(f"Invalid code, only otpauth accpeted: {dlg.content.code}")

    def update_list(self):
        for i in range(self.listWidget.count()):
            item = self.listWidget.item(i)
            item.update()

    def showEvent(self, event):
        entries = self.keyring.retrieve_entries()
        if entries:
            for entry in entries:
                self.addItem(TotpCode.from_dict(entry))
        self.update_list()
        self.timer.start(500)

    def hideEvent(self, event):
        self.timer.stop()

    def show_settings(self):
        from Controls.ModalOverlay import ModalOverlay
        from Controls.SettingsPage import SettingsPage
        self.settings_page = SettingsPage(self)
        overlay = ModalOverlay(self,self.settings_page)
        overlay.show()

    def addItem(self,code:TotpCode):
        item = QListWidgetItem()
        item.code = code
        frame = QFrame()
        frame.setFrameShape(QFrame.StyledPanel)
        frame.setFrameShadow(QFrame.Raised)
        frame.setLineWidth(2)
        widget_layout = QGridLayout(frame)
        widget_layout.setSpacing(0)
        # Title label
        title_label = QLabel(item.code.account)
        widget_layout.addWidget(title_label,0,0)

        # Large number area (assuming as QLabel)
        item.number_label = QLabel(str(item.code.GetCode()))
        item.number_label.setAlignment(Qt.AlignTop | Qt.AlignLeft) 
        item.number_label.setStyleSheet("font-size: 24px;")
        widget_layout.addWidget(item.number_label,1,0)

        item.progress_bar = QProgressBar()
        item.progress_bar.setOrientation(Qt.Vertical)
        item.progress_bar.setMinimum(0)
        item.progress_bar.setMaximum(100)
        item.progress_bar.setValue(item.code.GetInterval())
        item.progress_bar.setTextVisible(False)
        item.progress_bar.setSizePolicy(QSizePolicy.Fixed,QSizePolicy.Ignored)
        widget_layout.addWidget(item.progress_bar,0,1,2,1)

        def update(self=item):
            self.number_label.setText(str(self.code.GetCode()))
            self.progress_bar.setValue(self.code.GetInterval())
        item.update = update

        # Progress bar
        #progress_bar = QProgressBar()
        #progress_bar.setValue(code["progress"])
        #widget_layout.addWidget(progress_bar)

        item.setSizeHint(frame.sizeHint())  # Adjust item size
        self.listWidget.addItem(item)
        self.listWidget.setItemWidget(item, frame)

        #self.keyring.store_totp_entry(code.account,code)


    def showMenu(self):
        if self.sidebar.isVisible():
            self.sidebar.hide()
        else:
            self.sidebar.show()

    def customResizeEvent(self, event):
        # Override the resize event to handle sidebar visibility
        self.updateSidebarVisibility()
        return QMainWindow.resizeEvent(self, event)

    def updateSidebarVisibility(self):
        # Check if the window width is less than the height
        if self.width() > 500:
            self.sidebar.show()
            self.menuButton.hide()
        else:
            self.sidebar.hide()
            self.menuButton.show()

def launch():
    import sys
    from PySide6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    window.addItem(TotpCode("test","PASSWORD"))
    totp= TotpCode("test2","OBQXG43XN5ZGI===")
    window.addItem(totp)
    window.addItem(TotpCode.from_otpauth(str(totp)))
    #window.addItem({"title":"More Secrets","number":654321})
    sys.exit(app.exec())

if __name__ == "__main__":
    launch()
