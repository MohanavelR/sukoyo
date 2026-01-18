from PyQt5.QtWidgets import QComboBox
from PyQt5.QtCore import Qt

class Dropdown(QComboBox):
    """Reusable dropdown/select component"""
    def __init__(self, items=None, parent=None):
        super().__init__(parent)
        self.setObjectName("DefaultDropdown")
        self.setCursor(Qt.PointingHandCursor)
        
        if items:
            self.addItems(items)

# Alias for backwards compatibility
Select = Dropdown
