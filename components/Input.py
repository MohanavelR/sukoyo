from PyQt5.QtWidgets import QLineEdit
class Input(QLineEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("primaryInput")       