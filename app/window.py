from PyQt5.QtWidgets import (
    QApplication, QHBoxLayout, QScrollArea, QMainWindow, 
    QVBoxLayout, QWidget, QStackedWidget
)
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt
import sys
# Import all pages
from pages.dashboard import DashboardPage
from pages.inventory import InventoryPage
from pages.class_page import ClassPage
from pages.store import StorePage
from pages.warehouse import WarehousePage
from pages.party import PartyPage
from pages.stock import StockPage
from pages.sales import SalesPage
from pages.purchase import PurchasePage
from pages.accounts import AccountsPage
from pages.pos import POSPage
from pages.attendance import AttendancePage
from pages.settings import SettingsPage
from pages.report import ReportPage

from config.settings import Settings
from config.theme_manager import ThemeManager
from ui.sidebar import Sidebar
from ui.header import Header
from utils.constents import NAV_ITEMS

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(Settings.TITLE)
        self.setGeometry(Settings.X, Settings.Y, Settings.WIDTH, Settings.HEIGHT)
        self.setObjectName("MainWindow")
        
        # Initialize Data Manager
        from data.data_manager import DataManager
        self.data_manager = DataManager()
        
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
        self.inventory_page = InventoryPage(self.data_manager)
        
        # Add pages to stack
        self.pages.addWidget(self.dashboard_page)
        self.pages.addWidget(self.inventory_page)
        # Initialize new pages
        self.class_page = ClassPage()
        self.store_page = StorePage()
        self.warehouse_page = WarehousePage()
        self.party_page = PartyPage()
        self.stock_page = StockPage()
        self.sales_page = SalesPage()
        self.purchase_page = PurchasePage()
        self.accounts_page = AccountsPage()
        self.pos_page = POSPage(self.data_manager)
        self.report_page = ReportPage()
        self.attendance_page = AttendancePage()
        self.settings_page = SettingsPage()
        
        # Add pages to stack
        self.pages.addWidget(self.dashboard_page)
        self.pages.addWidget(self.inventory_page)
        self.pages.addWidget(self.class_page)
        self.pages.addWidget(self.store_page)
        self.pages.addWidget(self.warehouse_page)
        self.pages.addWidget(self.party_page)
        self.pages.addWidget(self.stock_page)
        self.pages.addWidget(self.sales_page)
        self.pages.addWidget(self.purchase_page)
        self.pages.addWidget(self.accounts_page)
        self.pages.addWidget(self.pos_page)
        self.pages.addWidget(self.report_page)
        self.pages.addWidget(self.attendance_page)
        self.pages.addWidget(self.settings_page)
        # Store page mapping for easy access
        self.page_widgets = {
            "dashboard": self.dashboard_page,
            "class": self.class_page,
            "store": self.store_page,
            "warehouse": self.warehouse_page,
            "party": self.party_page,
            "inventory": self.inventory_page,
            "stock": self.stock_page,
            "sales": self.sales_page,
            "purchase": self.purchase_page,
            "accounts": self.accounts_page,
            "pos": self.pos_page,
            "report": self.report_page,
            "attendance": self.attendance_page,
            "settings": self.settings_page,
        }
        
        # Add stretch to push content to top
        self.content_layout.addStretch()
        
        # Set content widget in scroll area
        self.content_scroll.setWidget(self.content_widget)
    
    def switch_page(self, page_id):
        """Handle page navigation from sidebar"""
        print(f"Switching to page: {page_id}")
        
        # Page titles mapping
        self.page_widgets = {
            "dashboard": self.dashboard_page,
            "class": self.class_page,
            "store": self.store_page,
            "warehouse": self.warehouse_page,
            "party": self.party_page,
            "inventory": self.inventory_page,
            "stock": self.stock_page,
            "sales": self.sales_page,
            "purchase": self.purchase_page,
            "accounts": self.accounts_page,
            "pos": self.pos_page,
            "report": self.report_page,
            "attendance": self.attendance_page,
            "settings": self.settings_page,
        }
        
        
        # Update header title
        page_titles = {pid: title for _, title, pid in NAV_ITEMS}
        title = page_titles.get(page_id, "Dashboard")
        self.header.set_title(title)
        
        # Switch to the actual page if it exists
        if page_id in self.page_widgets:
            self.pages.setCurrentWidget(self.page_widgets[page_id])
            
            # Adjust scroll area policy and margins based on page
            if page_id == "pos":
                self.header.hide()
                self.content_layout.setContentsMargins(0, 0, 0, 0)
                self.content_layout.setSpacing(0)
            else:
                self.header.show()
                self.content_layout.setContentsMargins(32, 28, 32, 32)
                self.content_layout.setSpacing(24)

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

