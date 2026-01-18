"""
Report Page Module
Displays report categories with links to various business reports
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QPushButton, QLabel, QFrame
)
from PyQt5.QtCore import Qt
from config.theme_manager import ThemeManager


class ReportSection(QFrame):
    """Represents one report category section"""
    def __init__(self, title, icon_text, links, border_right=False, border_bottom=False):
        super().__init__()
        self.setObjectName("ReportSection")
        
        # Set border properties for grid layout
        if border_right:
            self.setProperty("border-right", "true")
        if border_bottom:
            self.setProperty("border-bottom", "true")
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Header
        header = QFrame()
        header.setProperty("class", "section-header")
        
        h_layout = QHBoxLayout(header)
        h_layout.setContentsMargins(20, 15, 20, 15)
        h_layout.setSpacing(10)
        
        icon_lbl = QLabel(icon_text)
        icon_lbl.setProperty("class", "section-icon")
        h_layout.addWidget(icon_lbl)
        
        title_lbl = QLabel(title)
        title_lbl.setProperty("class", "section-title")
        h_layout.addWidget(title_lbl)
        h_layout.addStretch()
        
        layout.addWidget(header)
        
        # Content (Links)
        content_box = QFrame()
        v_layout = QVBoxLayout(content_box)
        v_layout.setContentsMargins(20, 20, 20, 20)
        v_layout.setSpacing(10)
        
        for link_text in links:
            btn = QPushButton(link_text)
            btn.setProperty("class", "report-link")
            btn.setCursor(Qt.PointingHandCursor)
            btn.clicked.connect(lambda _, t=link_text: self.on_link_click(title, t))
            v_layout.addWidget(btn)
            
        v_layout.addStretch()
        layout.addWidget(content_box)

    def on_link_click(self, category, link):
        print(f"Opening Report: [{category}] -> {link}")


class ReportPage(QWidget):
    """Main report page with categorized report links"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("ReportPage")
        
        self._init_ui()
        
        try:
            ThemeManager().theme_changed.connect(self.update_theme)
        except Exception as e:
            print(f"Error connecting to theme manager: {e}")
    
    def _init_ui(self):
        """Initialize report page UI"""
        try:
            layout = QVBoxLayout(self)
            layout.setContentsMargins(0, 0, 0, 0)
            layout.setSpacing(20)
            
            # Main Grid Container
            container = QFrame()
            container.setObjectName("ReportContainer")
            
            grid_layout = QGridLayout(container)
            grid_layout.setContentsMargins(0, 0, 0, 0)
            grid_layout.setSpacing(0)  # Borders handled by individual frames
            
            # Define Report Categories
            # Format: Title, Icon, Links
            data = [
                ("Item", "📦", [
                    "Item Sales and Purchase Summary", 
                    "Low Stock Summary", 
                    "Stock Summary", 
                    "Item Report By Party"
                ]),
                ("Party", "👥", [
                    "Sales Summary", 
                    "Vendor Report", 
                    "Party Statement (Ledger)", 
                    "Party Wise Outstanding"
                ]),
                ("GST", "📝", [
                    "GSTR-3b", 
                    "GSTR-2 (Purchase)"
                ]),
                ("Transaction", "💳", [
                    "Profit And Loss Report", 
                    "Purchase Summary", 
                    "Bill Wise Profit", 
                    "Expense Transaction Report"
                ])
            ]
            
            # Add to Grid (2x2)
            # Top Left (Border Right, Border Bottom)
            section1 = ReportSection(data[0][0], data[0][1], data[0][2], True, True)
            grid_layout.addWidget(section1, 0, 0)
            
            # Top Right (Border Bottom only)
            section2 = ReportSection(data[1][0], data[1][1], data[1][2], False, True)
            grid_layout.addWidget(section2, 0, 1)
            
            # Bottom Left (Border Right only)
            section3 = ReportSection(data[2][0], data[2][1], data[2][2], True, False)
            grid_layout.addWidget(section3, 1, 0)
            
            # Bottom Right (No borders)
            section4 = ReportSection(data[3][0], data[3][1], data[3][2], False, False)
            grid_layout.addWidget(section4, 1, 1)

            layout.addWidget(container)
            layout.addStretch()
            
        except Exception as e:
            print(f"Error initializing report page UI: {e}")
    
    def update_theme(self):
        """Refresh styles when theme changes"""
        try:
            self.style().unpolish(self)
            self.style().polish(self)
            self.update()
        except Exception as e:
            print(f"Error updating theme: {e}")
