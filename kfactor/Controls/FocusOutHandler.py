from PySide6.QtWidgets import QWidget
from PySide6.QtCore import QEvent, QObject
import sys

class FocusOutHandler(QObject):
    def __init__(self,callback, parent=None):
        super().__init__(parent)
        self.parent_widget = parent
        self.callback = callback

    def eventFilter(self, obj, event):
        if event.type() in (QEvent.FocusOut, QEvent.FocusIn):
            if not self.parent_widget.hasFocus() and not any(child.hasFocus() for child in self.parent_widget.findChildren(QWidget)):
                self.callback()
        return super().eventFilter(obj, event)
