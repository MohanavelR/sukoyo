"""
Sukoyo Inventory Management System
Clean and modular structure for easy understanding
"""

from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QSize, pyqtSignal
from PyQt5.QtGui import QIcon

# ============================================================================
# CONSTANTS AND CONFIGURATION
# ============================================================================

class Config:
    """Application configuration"""
    SIDEBAR_WIDTH = 280
    LIST_ITEM_HEIGHT = 70
    WINDOW_WIDTH = 1300
    WINDOW_HEIGHT = 800


# ============================================================================
# ITEM LIST SIDEBAR - Left panel with search and items
# ============================================================================

class ItemListWidget(QWidget):
    """
    Sidebar widget showing list of inventory items
    Features: Search, Filter buttons, Item list with custom styling
    """
    item_selected = pyqtSignal(dict)  # Signal when item is clicked
    
    def __init__(self):
        super().__init__()
        self.setObjectName("ItemListPanel")
        self.setFixedWidth(Config.SIDEBAR_WIDTH)
        self._setup_ui()
        self._load_sample_data()
    
    def _setup_ui(self):
        """Create all UI elements"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 20, 16, 20)
        layout.setSpacing(16)
        
        # Title
        self._add_header(layout)
        
        # Search box
        self._add_search_bar(layout)
        
        # Filter buttons (All, Low Stock)
        self._add_filter_buttons(layout)
        
        # Items list
        self._add_items_list(layout)
        
        # Item count at bottom
        self._add_item_count(layout)
    
    def _add_header(self, layout):
        """Add 'Items' header label"""
        header = QLabel("Items")
        header.setObjectName("PanelHeader")
        layout.addWidget(header)
    
    def _add_search_bar(self, layout):
        """Add search input field"""
        self.search_bar = QLineEdit()
        self.search_bar.setObjectName("SearchInput")
        self.search_bar.setPlaceholderText("Search items...")
        self.search_bar.textChanged.connect(self._on_search)
        layout.addWidget(self.search_bar)
    
    def _add_filter_buttons(self, layout):
        """Add All and Low Stock filter buttons"""
        filter_row = QHBoxLayout()
        filter_row.setSpacing(6)
        
        # All button (default active)
        self.btn_all = QPushButton("All")
        self.btn_all.setObjectName("FilterBtn")
        self.btn_all.setProperty("active", "true")
        self.btn_all.setCheckable(True)
        self.btn_all.setChecked(True)
        
        # Low Stock button
        self.btn_low_stock = QPushButton("Low Stock")
        self.btn_low_stock.setObjectName("FilterBtn")
        self.btn_low_stock.setCheckable(True)
        
        filter_row.addWidget(self.btn_all)
        filter_row.addWidget(self.btn_low_stock)
        layout.addLayout(filter_row)
    
    def _add_items_list(self, layout):
        """Add scrollable list of items"""
        self.list_widget = QListWidget()
        self.list_widget.setObjectName("ItemList")
        self.list_widget.setCursor(Qt.PointingHandCursor)
        self.list_widget.itemClicked.connect(self._on_item_clicked)
        layout.addWidget(self.list_widget)
    
    def _add_item_count(self, layout):
        """Add item count label at bottom"""
        self.count_label = QLabel("0 items")
        self.count_label.setObjectName("ItemCount")
        layout.addWidget(self.count_label)
    
    def _load_sample_data(self):
        """Load sample inventory items"""
        items = [
            {"name": "Camlin Geometry Box", "stock": "10 Pcs", 
             "status": "In Stock", "value": "₹500", "low_stock": False},
            {"name": "Classmate Sticky Notes", "stock": "100 pcs", 
             "status": "In Stock", "value": "₹1,200", "low_stock": False},
            {"name": "Kangaro Punch Machine", "stock": "5 Pcs", 
             "status": "Low Stock", "value": "₹2,500", "low_stock": True},
            {"name": "Doms Sharpeners", "stock": "10 bag", 
             "status": "In Stock", "value": "₹800", "low_stock": False},
        ]
        
        for item_data in items:
            self._add_item_to_list(item_data)
        
        self.count_label.setText(f"{len(items)} items")
        self.list_widget.setCurrentRow(0)
    
    def _add_item_to_list(self, item_data):
        """Add a single item to the list with custom widget"""
        # Create list item
        item = QListWidgetItem()
        item.setSizeHint(QSize(240, Config.LIST_ITEM_HEIGHT))
        item.setData(Qt.UserRole, item_data)
        self.list_widget.addItem(item)
        
        # Create custom widget for this item
        item_widget = self._create_item_widget(item_data)
        self.list_widget.setItemWidget(item, item_widget)
    
    def _create_item_widget(self, data):
        """Create the visual widget for one list item"""
        widget = QWidget()
        widget.setObjectName("ItemListItem")
        
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(10, 8, 10, 8)
        layout.setSpacing(5)
        
        # Top row: Name and Value
        top_row = QHBoxLayout()
        top_row.setSpacing(6)
        
        name_label = QLabel(data["name"])
        name_label.setObjectName("ItemTitle")
        name_label.setWordWrap(True)
        
        value_label = QLabel(data["value"])
        value_label.setObjectName("ItemValue")
        
        top_row.addWidget(name_label)
        top_row.addStretch()
        top_row.addWidget(value_label)
        
        # Bottom row: Status and Stock
        bottom_row = QHBoxLayout()
        bottom_row.setSpacing(6)
        
        status_label = QLabel(data["status"])
        status_label.setObjectName("ItemStatus")
        if data["low_stock"]:
            status_label.setProperty("lowstock", "true")
        
        stock_label = QLabel(data["stock"])
        stock_label.setObjectName("ItemSubtitle")
        
        bottom_row.addWidget(status_label)
        bottom_row.addStretch()
        bottom_row.addWidget(stock_label)
        
        layout.addLayout(top_row)
        layout.addLayout(bottom_row)
        
        return widget
    
    def _on_search(self, search_text):
        """Filter items based on search text"""
        for i in range(self.list_widget.count()):
            item = self.list_widget.item(i)
            item_data = item.data(Qt.UserRole)
            
            # Show/hide based on search match
            matches = search_text.lower() in item_data["name"].lower()
            item.setHidden(not matches)
    
    def _on_item_clicked(self, item):
        """Handle when user clicks an item"""
        item_data = item.data(Qt.UserRole)
        self.item_selected.emit(item_data)


# ============================================================================
# DETAIL VIEW - Right panel with tabs and content
# ============================================================================

class DetailPanel(QWidget):
    """
    Main detail panel showing item information
    Features: Header with actions, Stock info bar, Tabs, Content pages
    """
    
    def __init__(self):
        super().__init__()
        self.setObjectName("DetailViewContainer")
        self._setup_ui()
    
    def _setup_ui(self):
        """Create the main layout"""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Content container (the white rounded box)
        content = QWidget()
        content.setObjectName("MainContent")
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(24, 24, 24, 24)
        content_layout.setSpacing(16)
        
        # Add all sections
        self._add_header_section(content_layout)
        self._add_stock_info_bar(content_layout)
        self._add_tabs_section(content_layout)
        self._add_content_pages(content_layout)
        
        main_layout.addWidget(content)
    
    def _add_header_section(self, layout):
        """Add top header with back button and action buttons"""
        header_row = QHBoxLayout()
        header_row.setSpacing(12)
        
        # Back button
        back_btn = QPushButton("← Camlin Geometry Box")
        back_btn.setObjectName("BackBtn")
        back_btn.setCursor(Qt.PointingHandCursor)
        back_btn.clicked.connect(lambda: print("Back clicked"))
        header_row.addWidget(back_btn)
        
        header_row.addStretch()
        
        # Action buttons on the right
        actions = self._create_action_buttons()
        header_row.addWidget(actions)
        
        layout.addLayout(header_row)
    
    def _create_action_buttons(self):
        """Create the action buttons container"""
        container = QWidget()
        container.setObjectName("ActionsContainer")
        actions_layout = QHBoxLayout(container)
        actions_layout.setContentsMargins(0, 0, 0, 0)
        actions_layout.setSpacing(8)
        
        # Standard buttons
        btn_barcode = self._create_action_btn("🖨 Barcode", "Barcode Print")
        btn_adjust = self._create_action_btn("📊 Adjust", "Adjust Stock")
        btn_edit = self._create_action_btn("✏ Edit", "Edit Item")
        
        actions_layout.addWidget(btn_barcode)
        actions_layout.addWidget(btn_adjust)
        actions_layout.addWidget(btn_edit)
        
        # Dynamic buttons (shown based on active tab)
        self.btn_add_uom = self._create_action_btn("+ UOM", "Add UOM")
        self.btn_add_batch = self._create_action_btn("+ Batch", "Add Batch")
        self.btn_add_uom.hide()
        self.btn_add_batch.hide()
        
        actions_layout.addWidget(self.btn_add_uom)
        actions_layout.addWidget(self.btn_add_batch)
        
        return container
    
    def _create_action_btn(self, text, action_name):
        """Helper to create an action button"""
        btn = QPushButton(text)
        btn.setObjectName("ActionBtn")
        btn.setCursor(Qt.PointingHandCursor)
        btn.clicked.connect(lambda: print(f"Action: {action_name}"))
        return btn
    
    def _add_stock_info_bar(self, layout):
        """Add stock information bar"""
        stock_bar = QWidget()
        stock_bar.setObjectName("StockInfoBar")
        stock_layout = QHBoxLayout(stock_bar)
        stock_layout.setContentsMargins(16, 10, 16, 10)
        stock_layout.setSpacing(32)
        
        # Add three stat boxes
        stock_layout.addLayout(self._create_stat_box("Current Stock", "637 Units"))
        stock_layout.addLayout(self._create_stat_box("Stock Value", "₹10,689"))
        stock_layout.addLayout(self._create_stat_box("Min Stock Level", "100 Units"))
        stock_layout.addStretch()
        
        layout.addWidget(stock_bar)
    
    def _create_stat_box(self, label_text, value_text):
        """Create a stat box (label + value)"""
        container = QVBoxLayout()
        container.setSpacing(4)
        
        label = QLabel(label_text)
        label.setObjectName("StockLabel")
        
        value = QLabel(value_text)
        value.setObjectName("StockValue")
        
        container.addWidget(label)
        container.addWidget(value)
        
        return container
    
    def _add_tabs_section(self, layout):
        """Add tab buttons"""
        tabs_container = QWidget()
        tabs_container.setObjectName("TabsContainer")
        tabs_layout = QHBoxLayout(tabs_container)
        tabs_layout.setContentsMargins(0, 0, 0, 0)
        tabs_layout.setSpacing(0)
        
        # Create tab buttons
        self.tab_buttons = {}
        tab_names = ["Item Details", "Stock Details", "UOM", "Batch"]
        
        for name in tab_names:
            btn = QPushButton(name)
            btn.setObjectName("TabBtn")
            btn.setCursor(Qt.PointingHandCursor)
            btn.clicked.connect(lambda checked, n=name: self._switch_tab(n))
            tabs_layout.addWidget(btn)
            self.tab_buttons[name] = btn
        
        tabs_layout.addStretch()
        layout.addWidget(tabs_container)
    
    def _add_content_pages(self, layout):
        """Add stacked pages for different tabs"""
        self.stack = QStackedWidget()
        self.stack.setObjectName("ContentStack")
        
        # Create all pages
        self.pages = {
            "Item Details": ItemDetailsPage(),
            "Stock Details": StockDetailsPage(),
            "UOM": UOMPage(),
            "Batch": BatchPage()
        }
        
        for page in self.pages.values():
            self.stack.addWidget(page)
        
        layout.addWidget(self.stack)
        
        # Set default tab
        self._switch_tab("Item Details")
    
    def _switch_tab(self, tab_name):
        """Switch to a different tab"""
        # Update button styles
        for name, btn in self.tab_buttons.items():
            is_active = (name == tab_name)
            btn.setProperty("active", "true" if is_active else "false")
            btn.style().unpolish(btn)
            btn.style().polish(btn)
        
        # Switch page
        self.stack.setCurrentWidget(self.pages[tab_name])
        
        # Show/hide dynamic buttons
        self.btn_add_uom.setVisible(tab_name == "UOM")
        self.btn_add_batch.setVisible(tab_name == "Batch")


# ============================================================================
# PAGE WIDGETS - Different content for each tab
# ============================================================================

class ItemDetailsPage(QWidget):
    """Page showing item details (General Details + Price Details)"""
    
    def __init__(self):
        super().__init__()
        self.setObjectName("DetailsPage")
        self._setup_ui()
    
    def _setup_ui(self):
        """Create scrollable page with sections"""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setObjectName("DetailsScroll")
        
        content = QWidget()
        content.setObjectName("ScrollContent")
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(0, 12, 0, 0)
        content_layout.setSpacing(24)
        
        # Add sections
        content_layout.addWidget(self._create_general_section())
        content_layout.addWidget(self._create_price_section())
        content_layout.addStretch()
        
        scroll.setWidget(content)
        main_layout.addWidget(scroll)
    
    def _create_general_section(self):
        """Create General Details section"""
        section = QWidget()
        section.setObjectName("SectionWidget")
        layout = QVBoxLayout(section)
        layout.setContentsMargins(20, 18, 20, 18)
        layout.setSpacing(14)
        
        # Title
        title = QLabel("General Details")
        title.setObjectName("SectionTitle")
        layout.addWidget(title)
        
        # Grid of details
        details = [
            ("Item Type", "Product"), ("Item Name", "Camlin Geometry Box"),
            ("Item Code", "GB-1204"), ("Brand", "Camlin"),
            ("Category", "Stationery"), ("Subcategory", "Drawing Tools"),
            ("Discount", "5%"), ("Measuring Unit", "Piece"),
            ("Opening Stock", "500 Pcs"), ("Low Stock Warning", "Active"),
            ("Minimum Stock", "100 Pcs"), ("Maximum Stock", "1000 Pcs")
        ]
        layout.addLayout(self._create_details_grid(details))
        
        return section
    
    def _create_price_section(self):
        """Create Price Details section"""
        section = QWidget()
        section.setObjectName("SectionWidget")
        layout = QVBoxLayout(section)
        layout.setContentsMargins(20, 18, 20, 18)
        layout.setSpacing(14)
        
        # Title
        title = QLabel("Price Details")
        title.setObjectName("SectionTitle")
        layout.addWidget(title)
        
        # Grid of details
        details = [
            ("Sales Price", "₹100 (with GST)"),
            ("Wholesale Price", "₹80 (with GST)"),
            ("Purchase Price", "₹60 (with Tax)"),
            ("HSN Code", "9017"),
            ("GST Tax Rate", "18%"),
            ("Profit Margin", "40%")
        ]
        layout.addLayout(self._create_details_grid(details))
        
        return section
    
    def _create_details_grid(self, details):
        """Create grid layout for label-value pairs"""
        grid = QGridLayout()
        grid.setHorizontalSpacing(24)
        grid.setVerticalSpacing(16)
        grid.setContentsMargins(0, 0, 0, 0)
        
        row, col = 0, 0
        for label_text, value_text in details:
            # Create container for label + value
            container = QWidget()
            container.setObjectName("DetailContainer")
            v_layout = QVBoxLayout(container)
            v_layout.setContentsMargins(0, 0, 0, 0)
            v_layout.setSpacing(5)
            
            label = QLabel(label_text)
            label.setObjectName("DetailLabel")
            
            value = QLabel(value_text)
            value.setObjectName("DetailValue")
            
            v_layout.addWidget(label)
            v_layout.addWidget(value)
            
            grid.addWidget(container, row, col)
            
            col += 1
            if col > 2:  # 3 columns
                col = 0
                row += 1
        
        return grid


class StockDetailsPage(QWidget):
    """Page showing stock transaction history"""
    
    def __init__(self):
        super().__init__()
        self.setObjectName("StockPage")
        self._setup_ui()
    
    def _setup_ui(self):
        """Create table with stock history"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 12, 0, 12)
        
        table = self._create_table()
        layout.addWidget(table)
    
    def _create_table(self):
        """Create stock details table"""
        scroll = QScrollArea()
        scroll.setObjectName("TableScrollArea")
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        
        table = QTableWidget(5, 6)
        table.setObjectName("DataTable")
        table.setHorizontalHeaderLabels(
            ["#", "Date", "Type", "Invoice", "Quantity", "Balance"]
        )
        
        # Configure table
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        table.setColumnWidth(0, 50)
        table.verticalHeader().setVisible(False)
        table.verticalHeader().setDefaultSectionSize(48)
        table.setShowGrid(True)
        table.setAlternatingRowColors(True)
        
        # Add data
        data = [
            ("01", "30/04/2025", "Stock In", "PO-400", "+200", "637"),
            ("02", "28/04/2025", "Sale", "INV-523", "-50", "437"),
            ("03", "25/04/2025", "Stock In", "PO-389", "+150", "487"),
            ("04", "20/04/2025", "Adjustment", "ADJ-012", "+37", "337"),
            ("05", "15/04/2025", "Opening Stock", "-", "300", "300"),
        ]
        
        for r, row_data in enumerate(data):
            for c, text in enumerate(row_data):
                item = QTableWidgetItem(text)
                align = Qt.AlignCenter if c == 0 else Qt.AlignLeft
                item.setTextAlignment(align | Qt.AlignVCenter)
                table.setItem(r, c, item)
        
        scroll.setWidget(table)
        return scroll


class UOMPage(QWidget):
    """Page showing Unit of Measure configurations"""
    
    def __init__(self):
        super().__init__()
        self.setObjectName("UOMPage")
        self._setup_ui()
    
    def _setup_ui(self):
        """Create UOM table"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 12, 0, 12)
        
        table = self._create_table()
        layout.addWidget(table)
    
    def _create_table(self):
        """Create UOM table"""
        scroll = QScrollArea()
        scroll.setObjectName("TableScrollArea")
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        
        table = QTableWidget(2, 5)
        table.setObjectName("DataTable")
        table.setHorizontalHeaderLabels(
            ["#", "UOM Type", "Quantity", "Rate", "Stock"]
        )
        
        # Configure
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        table.setColumnWidth(0, 50)
        table.verticalHeader().setVisible(False)
        table.verticalHeader().setDefaultSectionSize(48)
        table.setShowGrid(True)
        
        # Add data
        data = [
            ("01", "Box", "10 Pcs/Box", "₹500", "63 Boxes"),
            ("02", "Piece", "1 Pc", "₹50", "637 Pcs")
        ]
        
        for r, row_data in enumerate(data):
            for c, text in enumerate(row_data):
                item = QTableWidgetItem(text)
                align = Qt.AlignCenter if c == 0 else Qt.AlignLeft
                item.setTextAlignment(align | Qt.AlignVCenter)
                table.setItem(r, c, item)
        
        scroll.setWidget(table)
        return scroll


class BatchPage(QWidget):
    """Page showing batch information"""
    
    def __init__(self):
        super().__init__()
        self.setObjectName("BatchPage")
        self._setup_ui()
    
    def _setup_ui(self):
        """Create batch table with action buttons"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 12, 0, 12)
        
        table = self._create_table()
        layout.addWidget(table)
    
    def _create_table(self):
        """Create batch table with action column"""
        scroll = QScrollArea()
        scroll.setObjectName("TableScrollArea")
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        
        table = QTableWidget(3, 6)
        table.setObjectName("DataTable")
        table.setHorizontalHeaderLabels(
            ["#", "Batch No", "Quantity", "MFG Date", "EXP Date", "Action"]
        )
        
        # Configure
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        table.setColumnWidth(0, 50)
        table.verticalHeader().setVisible(False)
        table.verticalHeader().setDefaultSectionSize(48)
        table.setShowGrid(True)
        
        # Add data
        data = [
            ("01", "B001-2025", "250", "01/01/25", "01/01/27"),
            ("02", "B002-2025", "200", "15/01/25", "15/01/27"),
            ("03", "B003-2025", "187", "28/01/25", "28/01/27")
        ]
        
        for r, row_data in enumerate(data):
            for c, text in enumerate(row_data):
                item = QTableWidgetItem(text)
                align = Qt.AlignCenter if c == 0 else Qt.AlignLeft
                item.setTextAlignment(align | Qt.AlignVCenter)
                table.setItem(r, c, item)
            
            # Add action button
            btn_widget = QWidget()
            btn_widget.setObjectName("TableActionWidget")
            btn_layout = QHBoxLayout(btn_widget)
            btn_layout.setContentsMargins(8, 4, 8, 4)
            
            btn = QPushButton("🖨 Print")
            btn.setObjectName("TableActionBtn")
            btn.setMinimumHeight(32)
            btn.clicked.connect(lambda: print("Print clicked"))
            btn_layout.addWidget(btn)
            btn_layout.addStretch()
            
            table.setCellWidget(r, 5, btn_widget)
        
        scroll.setWidget(table)
        return scroll


# ============================================================================
# MAIN INVENTORY PAGE - Combines sidebar and detail panel
# ============================================================================

class InventoryPage(QWidget):
    """
    Main Inventory Management Page
    Layout: [ItemList Sidebar] [Detail Panel]
    """
    
    def __init__(self):
        super().__init__()
        self.setObjectName("InventoryPage")
        self._setup_ui()
    
    def _setup_ui(self):
        """Create main layout with sidebar and detail panel"""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Left: Item list sidebar
        self.item_list = ItemListWidget()
        layout.addWidget(self.item_list)
        
        # Right: Detail panel
        self.detail_panel = DetailPanel()
        layout.addWidget(self.detail_panel)
        
        # Connect signals
        self.item_list.item_selected.connect(self._on_item_selected)
        
        # Set stretch factors (sidebar fixed, detail expands)
        layout.setStretch(0, 0)
        layout.setStretch(1, 1)
    
    def _on_item_selected(self, item_data):
        """Handle item selection from sidebar"""
        print(f"Selected: {item_data['name']}")
        # TODO: Update detail panel with selected item data


