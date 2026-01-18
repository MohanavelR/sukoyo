from PyQt5.QtWidgets import QFrame, QVBoxLayout, QGraphicsDropShadowEffect
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor

class CardWidget(QFrame):
    """
    A unified card component with consistent shadow, border radius, 
    and background styling. Replacing ad-hoc QFrame styling.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("CardWidget")
        
        # Enable shadow
        self._setup_shadow()
        
    def _setup_shadow(self):
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(20)
        shadow.setXOffset(0)
        shadow.setYOffset(4)
        shadow.setColor(QColor(0, 0, 0, 20))  # Soft shadow
        self.setGraphicsEffect(shadow)
