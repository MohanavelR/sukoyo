from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QPushButton
from PyQt5.QtCore import Qt
from components.card import CardWidget
from components.button import PrimaryButton
from config.theme_manager import ThemeManager
from config.theme import Theme

class SettingsPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("SettingsPage")
        self._init_ui()
        
        ThemeManager().theme_changed.connect(self.update_theme)

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Theme Settings Card
        card = CardWidget()
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(30, 30, 30, 30)
        card_layout.setSpacing(20)
        
        title = QLabel("Appearance")
        title.setStyleSheet("font-size: 20px; font-weight: 600; color: {{text_primary}};")
        title.setObjectName("SectionTitle")
        card_layout.addWidget(title)
        
        subtitle = QLabel("Customize the visual style of the application")
        subtitle.setStyleSheet("font-size: 14px; color: {{text_secondary}};")
        subtitle.setObjectName("SectionSubtitle")
        card_layout.addWidget(subtitle)
        
        # Theme Options
        themes_layout = QHBoxLayout()
        themes_layout.setSpacing(15)
        
        self.theme_buttons = []
        
        themes = [
            ("Dark Trend", "dark"),
            ("Elegant Purple", "purple"),
            ("Clean Light", "light")
        ]
        
        for name, theme_id in themes:
            btn = PrimaryButton(name)
            btn.setCheckable(True)
            btn.clicked.connect(lambda checked, t=theme_id: self.change_theme(t))
            themes_layout.addWidget(btn)
            self.theme_buttons.append((theme_id, btn))
            
        card_layout.addLayout(themes_layout)
        card_layout.addStretch()
        
        layout.addWidget(card)
        layout.addStretch()
        
        # Set initial active state
        self.update_active_button()

    def change_theme(self, theme_id):
        manager = ThemeManager()
        manager.set_theme(theme_id)
        self.update_active_button()
        
    def update_active_button(self):
        pass
    def update_theme(self):
        self.style().unpolish(self)
        self.style().polish(self)
        pass
