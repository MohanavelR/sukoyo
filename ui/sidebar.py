from PyQt5.QtWidgets import (
    QWidget, QFrame, QVBoxLayout,
    QPushButton, QLabel, QScrollArea
)
from PyQt5.QtCore import Qt, pyqtSignal, QSize
from PyQt5.QtGui import QIcon, QFont

from config.settings import Settings
from utils.constents import NAV_ITEMS
from config.theme_manager import ThemeManager


class Sidebar(QWidget):
    navigate = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.is_menu_open = True  # Start expanded
        self.current_page = "dashboard"  # Default page
        self.nav_buttons = []  # Initialize here to avoid AttributeError

        self._create_sidebar()
        
        # Connect to theme changes after UI is created
        ThemeManager().theme_changed.connect(self.update_theme)

    def _create_sidebar(self):
        """Create or recreate the sidebar UI"""
        # Clear existing layout if rebuilding
        if self.layout() is not None:
            QWidget().setLayout(self.layout())
        
        # Clear button references when rebuilding
        self.nav_buttons = []
        
        # Main sidebar frame
        self.sidebar = QFrame(self)
        self.sidebar.setObjectName("Sidebar")
        self.sidebar.setProperty("collapsed", "false" if self.is_menu_open else "true")
        
        layout = QVBoxLayout(self.sidebar)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(4)

        # Toggle button
        self.menu_btn = QPushButton()
        self.menu_btn.setObjectName("SidebarToggleButton")
        menu_icon_path = Settings.ROOT_PATH/ "sukoyo" / "assets" / "icons" / "menu.png"
        self.menu_btn.setIcon(QIcon(str(menu_icon_path)))
        self.menu_btn.setIconSize(QSize(22, 22))
        self.menu_btn.setCursor(Qt.PointingHandCursor)
        self.menu_btn.clicked.connect(self.toggle_sidebar)
        layout.addWidget(self.menu_btn)

        # Sidebar logo/title (only when expanded)
        if self.is_menu_open:
            self.sidebar_label = QLabel("SUKOVO")
            self.sidebar_label.setObjectName("SidebarLogo")
            self.sidebar_label.setAlignment(Qt.AlignCenter)
            layout.addWidget(self.sidebar_label)

        # Scroll Area for Navigation Items
        scroll_area = QScrollArea()
        scroll_area.setObjectName("SidebarScrollArea")
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.NoFrame)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        # Hide vertical scrollbar when collapsed for cleaner look
        if self.is_menu_open:
            scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        else:
            scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        # Container for buttons inside scroll area
        scroll_content = QWidget()
        scroll_content.setObjectName("SidebarScrollContent")
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setContentsMargins(0, 0, 0, 0)
        scroll_layout.setSpacing(4)

        # Navigation buttons
        for icon_filename, text, page_id in NAV_ITEMS:
            btn = QPushButton()
            btn.setObjectName(f"SidebarButton_{page_id}")
            btn.setProperty("class", "nav-button")
            btn.setCheckable(True)
            btn.setCursor(Qt.PointingHandCursor)
            
            # Set icon
            icon_path = Settings.ROOT_PATH / "sukoyo" /icon_filename
            if icon_path.exists():
                btn.setIcon(QIcon(str(icon_path)))
                btn.setIconSize(QSize(20, 20))
            else:
                print(f"Warning: Icon not found at {icon_path}")
            
            # Set text only when menu is open
            if self.is_menu_open:
                btn.setText(text)
            
            # Set active state
            is_active = (self.current_page == page_id)
            btn.setChecked(is_active)
            btn.setProperty("page", page_id)
            
            # Connect navigation
            btn.clicked.connect(lambda checked, p=page_id: self.on_navigate(p))
            
            scroll_layout.addWidget(btn)
            self.nav_buttons.append(btn)

        scroll_layout.addStretch()
        
        # Set widget for scroll area
        scroll_area.setWidget(scroll_content)
        
        # Add scroll area to main layout
        layout.addWidget(scroll_area)
        
        # Set the layout on self, not sidebar
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(self.sidebar)
        self.setLayout(main_layout)

    def toggle_sidebar(self):
        """Toggle between expanded and collapsed states"""
        self.is_menu_open = not self.is_menu_open
        
        # Rebuild sidebar with new state
        self._create_sidebar()
        
        # Force style refresh to apply collapsed property
        self.sidebar.style().unpolish(self.sidebar)
        self.sidebar.style().polish(self.sidebar)
        self.sidebar.update()

    def on_navigate(self, page):
        """Handle page navigation"""
        if self.current_page == page:
            return  # Already on this page
        
        self.current_page = page

        # Update button checked states
        for btn in self.nav_buttons:
            is_current = btn.property("page") == page
            btn.setChecked(is_current)

        # Emit navigation signal
        self.navigate.emit(page)

    def update_theme(self):
        """Refresh UI when theme changes"""
        # Force repaint of all widgets
        self.sidebar.style().unpolish(self.sidebar)
        self.sidebar.style().polish(self.sidebar)
        
        for btn in self.nav_buttons:
            btn.style().unpolish(btn)
            btn.style().polish(btn)
        
        self.update()