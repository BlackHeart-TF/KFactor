from PySide6.QtWidgets import QPushButton, QMenu
from PySide6.QtCore import QPoint, Slot
class SplitButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.menu = QMenu(self)
        self.setMenu(self.menu)
        self.clicked.connect(self.perform_default_action)
        self.default_action = None

    def perform_default_action(self):
        if self.default_action:
            self.default_action.trigger()

    def add_action(self, text, func):
        action = self.menu.addAction(text)
        action.triggered.connect(func)
        action.triggered.connect(lambda x,action=action:self.setDefault(action))
        # if not self.default_action:
        #     self.default_action = action

    def setDefault(self,action):
        self.default_action = action

    def hitButton(self, pos: QPoint) -> bool:
        if self.default_action and self.width()-18 > pos.x():
            self.perform_default_action()
            return False
        else:
            return super().hitButton(pos)

