from PyQt5.QtWidgets import QPushButton

class PrimaryButton(QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("primaryButton") 
class SecondaryButton(QPushButton): 
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("secondaryButton")
class DefaultButton(QPushButton): 
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("defaultButton")        