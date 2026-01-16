from PyQt5.QtWidgets import QWidget, QHBoxLayout, QPushButton, QLabel, QVBoxLayout
from PyQt5.QtCore import Qt
from config.theme_manager import ThemeManager


class Header(QWidget):
    def __init__(self, title="Dashboard", parent=None):
        super().__init__(parent)
        self.page_title = title
        self.setObjectName("Header")
        
        self._create_header()
        
        # Connect to theme changes
        ThemeManager().theme_changed.connect(self.update_theme)
    
    def _create_header(self):
        """Create dashboard header - styled via QSS"""
        # Main layout
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(16)
        
        # Page Title
        self.title_label = QLabel(self.page_title)
        self.title_label.setObjectName("PageTitle")
        layout.addWidget(self.title_label)
        
        # Spacer
        layout.addStretch()
        
        # User actions container
        user_widget = QWidget()
        user_widget.setObjectName("UserActionsWidget")
        user_layout = QHBoxLayout(user_widget)
        user_layout.setSpacing(12)
        user_layout.setContentsMargins(0, 0, 0, 0)
        
        # Action buttons (cart, messages, camera, notifications)
        action_icons = ["🛒", "💬", "📷", "⚫"]
        action_names = ["Cart", "Messages", "Camera", "Notifications"]
        
        for idx, (icon, name) in enumerate(zip(action_icons, action_names)):
            btn = QPushButton(icon)
            btn.setObjectName(f"ActionButton_{name}")
            btn.setProperty("class", "action-button")
            btn.setFixedSize(44, 44)
            btn.setCursor(Qt.PointingHandCursor)
            btn.setToolTip(name)  # Add tooltip for accessibility
            # No inline styles - QSS handles it!
            user_layout.addWidget(btn)
        
        # User info display
        user_info = QWidget()
        user_info.setObjectName("UserInfoWidget")
        user_info_layout = QVBoxLayout(user_info)
        user_info_layout.setSpacing(2)
        user_info_layout.setContentsMargins(12, 0, 0, 0)
        
        self.user_name = QLabel("Mohan")
        self.user_name.setObjectName("UserName")
        
        self.user_role = QLabel("Admin")
        self.user_role.setObjectName("UserRole")
        
        user_info_layout.addWidget(self.user_name)
        user_info_layout.addWidget(self.user_role)
        user_layout.addWidget(user_info)
        
        layout.addWidget(user_widget)
    
    def set_title(self, title):
        """Update the page title"""
        self.page_title = title
        self.title_label.setText(title)
    
    def set_user_info(self, name, role):
        """Update user information"""
        self.user_name.setText(name)
        self.user_role.setText(role)
    
    def update_theme(self):
        """Refresh styles when theme changes"""
        self.style().unpolish(self)
        self.style().polish(self)
        self.update()