from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt
from components.card import CardWidget

class AccountsPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("AccountsPage")
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setAlignment(Qt.AlignTop)
        
        card = CardWidget()
        card.setMaximumHeight(300)
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(40, 40, 40, 40)
        
        label = QLabel("Accounts & Finance")
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("font-size: 24px; color: #6b7280; font-weight: 500;")
        
        sub_label = QLabel("This page is under construction")
        sub_label.setAlignment(Qt.AlignCenter)
        sub_label.setStyleSheet("font-size: 14px; color: #9ca3af; margin-top: 10px;")
        
        card_layout.addStretch()
        card_layout.addWidget(label)
        card_layout.addWidget(sub_label)
        card_layout.addStretch()
        
        layout.addWidget(card)
