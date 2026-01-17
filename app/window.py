from PyQt5.QtWidgets import (
    QApplication, QHBoxLayout, QScrollArea, QMainWindow, 
    QVBoxLayout, QWidget, QStackedWidget
)
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt
import sys
from pages.dashboard import DashboardPage
from pages.inventory import InventoryPage

from config.settings import Settings
from config.theme_manager import ThemeManager
from ui.sidebar import Sidebar
from ui.header import Header


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(Settings.TITLE)
        self.setGeometry(Settings.X, Settings.Y, Settings.WIDTH, Settings.HEIGHT)
        self.setObjectName("MainWindow")
        
        self._init_ui()
        
        # Connect sidebar navigation
        self.sidebar.navigate.connect(self.switch_page)
        
        # Connect to theme changes
        ThemeManager().theme_changed.connect(self.update_theme)
    
    def _init_ui(self):
        """Initialize the main UI layout"""
        # Central widget
        central_widget = QWidget()
        central_widget.setObjectName("CentralWidget")
        self.setCentralWidget(central_widget)
        
        # Main horizontal layout (sidebar + content)
        self.main_layout = QHBoxLayout(central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        
        # Sidebar
        self.sidebar = Sidebar()
        self.main_layout.addWidget(self.sidebar)
        
        # Content area
        self._create_content_area()
        
        # Add scroll area to main layout
        self.main_layout.addWidget(self.content_scroll, 1)
    
    def _create_content_area(self):
        """Create the scrollable content area"""
        # Scroll area
        self.content_scroll = QScrollArea()
        self.content_scroll.setObjectName("ContentScrollArea")
        self.content_scroll.setWidgetResizable(True)
        self.content_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        # Content widget inside scroll area
        self.content_widget = QWidget()
        self.content_widget.setObjectName("ContentWidget")
        
        # Content layout
        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_layout.setContentsMargins(32, 28, 32, 32)
        self.content_layout.setSpacing(24)
        
        # Header
        self.header = Header(title="Dashboard")
        self.content_layout.addWidget(self.header)
        
        # Stacked widget for pages
        self.pages = QStackedWidget()
        self.pages.setObjectName("PagesStack")
        self.content_layout.addWidget(self.pages)
        
        # Initialize pages
        self.dashboard_page = DashboardPage()
        self.inventory_page = InventoryPage()
        
        # Add pages to stack
        self.pages.addWidget(self.dashboard_page)
        self.pages.addWidget(self.inventory_page)
        
        # Store page mapping for easy access
        self.page_widgets = {
            "dashboard": self.dashboard_page,
            "inventory": self.inventory_page,
        }
        
        # Add stretch to push content to top
        self.content_layout.addStretch()
        
        # Set content widget in scroll area
        self.content_scroll.setWidget(self.content_widget)
    
    def switch_page(self, page_id):
        """Handle page navigation from sidebar"""
        print(f"Switching to page: {page_id}")
        
        # Page titles mapping
        page_titles = {
            "dashboard": "Dashboard",
            "analytics": "Analytics",
            "products": "Products",
            "orders": "Orders",
            "inventory": "Inventory",
            "settings": "Settings",
        }
        
        # Update header title
        title = page_titles.get(page_id, "Dashboard")
        self.header.set_title(title)
        
        # Switch to the actual page if it exists
        if page_id in self.page_widgets:
            self.pages.setCurrentWidget(self.page_widgets[page_id])
            
            # Adjust scroll area policy based on page
            if page_id == "inventory":
                # Inventory page has its own internal scrolling
                self.content_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            else:
                # Other pages use the content area scroll
                self.content_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        else:
            # Page not implemented yet - stay on current page or show dashboard
            print(f"Page '{page_id}' not implemented yet")
    
    def update_theme(self):
        """Refresh UI when theme changes"""
        # Force style refresh on main components
        self.style().unpolish(self)
        self.style().polish(self)
        self.update()

