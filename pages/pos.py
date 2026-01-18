from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QPushButton, 
    QFrame, QLineEdit, QTableWidget, QTableWidgetItem, QHeaderView,
    QSpacerItem, QSizePolicy, QComboBox
)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon
from components.button import PrimaryButton, SecondaryButton, DefaultButton
import os

class POSPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("POSPage")
        self._init_ui()

    def _init_ui(self):
        # Remove default layout margins from window.py for POS page
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # 1. Header Area
        header = QFrame()
        header.setObjectName("POSHeader")
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(0, 0, 20, 0)
        header_layout.setSpacing(0)

        # Tabs
        tab1 = DefaultButton("Billing Screen 1")
        
        tab1.setProperty("active", "true")
        header_layout.addWidget(tab1)

        close_tab = DefaultButton("✕")
        
        header_layout.addWidget(close_tab)

        tab2 = DefaultButton("+ Hold Bill & Create Another")
        
        header_layout.addWidget(tab2)

        header_layout.addStretch()

        # Action Buttons
        retail_pos = PrimaryButton("Retail POS")
       
        header_layout.addWidget(retail_pos)

        header_layout.addSpacing(10)

        exit_pos = SecondaryButton("<  Exit POS")
        
        header_layout.addWidget(exit_pos)

        layout.addWidget(header)

        # 2. Main Content Area (Table + Sidebar)
        content_layout = QHBoxLayout()
        content_layout.setContentsMargins(20, 20, 20, 20)
        content_layout.setSpacing(20)

        # Left Side (Table Area)
        table_area = QVBoxLayout()
        table_area.setSpacing(15)

        # Search Bar
        search_frame = QFrame()
        search_frame.setObjectName("POSSearchFrame")
        search_layout = QHBoxLayout(search_frame)
        search_layout.setContentsMargins(10, 0, 10, 0)
        
        search_icon = QLabel("🔍") # Placeholder for actual icon
        search_layout.addWidget(search_icon)

        search_input = QLineEdit()
        search_input.setObjectName("POSSearchInput")
        search_input.setPlaceholderText("Search by item name / item code or Scan Barcode...")
        search_layout.addWidget(search_input)
        table_area.addWidget(search_frame)

        # Table
        self.table = QTableWidget()
        self.table.setObjectName("POSTable")
        self.table.setColumnCount(9)
        self.table.setHorizontalHeaderLabels([
            "#", "Item", "Unit", "Quantity", "Price/Unit", 
            "Discount", "Tax", "Amount", "Action"
        ])
        
        # Table column sizing
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Fixed)
        self.table.setColumnWidth(0, 40)   # #
        header.setSectionResizeMode(1, QHeaderView.Stretch) # Item
        self.table.setColumnWidth(2, 60)   # Unit
        self.table.setColumnWidth(3, 80)   # Quantity
        self.table.setColumnWidth(4, 90)   # Price/Unit
        self.table.setColumnWidth(5, 80)   # Discount
        self.table.setColumnWidth(6, 60)   # Tax
        self.table.setColumnWidth(7, 90)   # Amount
        self.table.setColumnWidth(8, 60)   # Action
        
        table_area.addWidget(self.table)

        # Table Footer
        table_footer = QHBoxLayout()
        self.total_items_label = QLabel("Total Items : 5")
        table_footer.addWidget(self.total_items_label)
        table_footer.addStretch()
        clear_btn = SecondaryButton("  X  Clear All Items")
       
        clear_btn.clicked.connect(self.clear_all_items)
        table_footer.addWidget(clear_btn)
        table_area.addLayout(table_footer)

        content_layout.addLayout(table_area, 3)

        # Right Side (Sidebar)
        sidebar_frame = QFrame()
        sidebar_frame.setObjectName("POSSidebar")
        sidebar_layout = QVBoxLayout(sidebar_frame)
        sidebar_layout.setContentsMargins(20, 0, 20, 0)
        sidebar_layout.setSpacing(15)

        # Shortcut Buttons Grid
        shortcuts_grid = QGridLayout()
        shortcuts_grid.setSpacing(10)
        btn_texts = ["Add Discount [F5]", "Additional Charges [F6]", "Loyalty Points [F7]", "Gift card & Vouchers"]
        for i, text in enumerate(btn_texts):
            btn = SecondaryButton(text)
           
            shortcuts_grid.addWidget(btn, i // 2, i % 2)
        sidebar_layout.addLayout(shortcuts_grid)

        # Customer Details
        cust_heading = QLabel("Customer Details")
        cust_heading.setObjectName("POSSidebarHeading")
        sidebar_layout.addWidget(cust_heading)
        
        customer_card = QFrame()
        customer_card.setObjectName("POSCustomerCard")
        cust_card_layout = QVBoxLayout(customer_card)
        add_cust_btn = DefaultButton("+ Add Customer")
        # add_cust_btn.setObjectName("POSAddCustomerBtn")
        cust_card_layout.addWidget(add_cust_btn, 0, Qt.AlignCenter)
        sidebar_layout.addWidget(customer_card)

        # Bill Details
        bill_heading = QLabel("Bill Details")
        bill_heading.setObjectName("POSSidebarHeading")
        sidebar_layout.addWidget(bill_heading)
        
        bill_details_frame = QFrame()
        bill_details_layout = QVBoxLayout(bill_details_frame)
        bill_details_layout.setSpacing(8)
        
        rows = [("Sub Total", "₹914"), ("Discount before tax", "₹10"), ("Tax", "₹11"), ("Carry Bag", "₹10")]
        for label_text, value_text in rows:
            row_frame = QFrame()
            row_layout = QHBoxLayout(row_frame)
            row_layout.setContentsMargins(0, 0, 0, 0)
            lbl = QLabel(label_text)
            lbl.setObjectName("POSBillLabel")
            val = QLabel(value_text)
            val.setObjectName("POSBillValue")
            val.setAlignment(Qt.AlignRight)
            row_layout.addWidget(lbl)
            row_layout.addWidget(val)
            bill_details_layout.addWidget(row_frame)
        sidebar_layout.addWidget(bill_details_frame)

        # Total Amount
        total_frame = QFrame()
        total_frame.setObjectName("POSTotalAmountFrame")
        total_layout = QHBoxLayout(total_frame)
        total_lbl = QLabel("Total Amount")
        total_lbl.setObjectName("POSTotalAmountLabel")
        total_val = QLabel("₹945")
        total_val.setObjectName("POSTotalAmountValue")
        total_layout.addWidget(total_lbl)
        total_layout.addStretch()
        total_layout.addWidget(total_val)
        sidebar_layout.addWidget(total_frame)

        # Received Amount
        received_label = QLabel("Received Amount")
        received_label.setObjectName("POSSidebarHeading")
        sidebar_layout.addWidget(received_label)
        
        received_frame = QFrame()
        received_frame.setObjectName("POSReceivedFrame")
        received_layout = QHBoxLayout(received_frame)
        received_input = QLineEdit("₹1500")
        received_input.setObjectName("POSReceivedInput")
        received_input.setFixedSize(150, 35)
        received_layout.addWidget(received_input)
        received_layout.addStretch()
        payment_mode = QComboBox()
        payment_mode.setObjectName("POSPaymentMode")
        payment_mode.addItem("Cash")
        payment_mode.setFixedSize(120, 35)
        received_layout.addWidget(payment_mode)
        sidebar_layout.addWidget(received_frame)

        # Change to return
        change_frame = QFrame()
        change_frame.setObjectName("POSChangeReturnFrame")
        change_layout = QHBoxLayout(change_frame)
        change_lbl = QLabel("Change To Return")
        change_lbl.setObjectName("POSChangeLabel")
        change_val = QLabel("₹400")
        change_val.setObjectName("POSChangeValue")
        change_layout.addWidget(change_lbl)
        change_layout.addStretch()
        change_layout.addWidget(change_val)
        sidebar_layout.addWidget(change_frame)

        sidebar_layout.addStretch()

        # Footer Buttons
        footer_btns_layout = QVBoxLayout()
        footer_btns_layout.setSpacing(10)
        
        h_btns = QHBoxLayout()
        h_btns.setSpacing(10)
        save_bill = PrimaryButton("Save Bill [F11]")
        save_bill.setObjectName("POSBottomActionBtn")
        save_bill.setFixedHeight(45)
        save_bill.clicked.connect(lambda: print("Saving Bill..."))
        
        save_print = PrimaryButton("Save & Print [F12]")
        # save_print.setObjectName("POSBottomActionBtn")
        save_print.setFixedHeight(45)
        save_print.clicked.connect(lambda: print("Saving and Printing..."))
        
        h_btns.addWidget(save_bill)
        h_btns.addWidget(save_print)
        footer_btns_layout.addLayout(h_btns)
        
        corp_bill = PrimaryButton("Corporate Bill")
        # corp_bill.setObjectName("POSBottomActionBtn")
        corp_bill.setFixedHeight(45)
        corp_bill.clicked.connect(lambda: print("Corporate Bill button clicked"))
        footer_btns_layout.addWidget(corp_bill)
        
        sidebar_layout.addLayout(footer_btns_layout)

        content_layout.addWidget(sidebar_frame)
        layout.addLayout(content_layout)
        self._populate_sample_data()

    def _populate_sample_data(self):
        sample_data = [
            ("01", "Camlin Geometry Box", "Pcs", "2", "₹85", "10%", "0.5%", "₹154"),
            ("02", "Classmate Sticky Notes", "Pcs", "3", "₹180", "5%", "1%", "₹518"),
            ("03", "Kangaro Punch Machine", "Pcs", "1", "₹150", "8%", "-", "₹145"),
            ("04", "Doms Sharpeners", "Box", "2", "₹50", "2%", "0.5%", "₹97"),
            ("05", "Mutton Masala", "Box", "2", "₹50", "2%", "0.5%", "₹97")
        ]
        
        self.table.setRowCount(0)
        for data in sample_data:
            self.add_item_to_table(data)

    def add_item_to_table(self, data):
        row = self.table.rowCount()
        self.table.insertRow(row)
        
        for col, value in enumerate(data):
            item = QTableWidgetItem(value)
            item.setTextAlignment(Qt.AlignCenter if col != 1 else Qt.AlignLeft | Qt.AlignVCenter)
            self.table.setItem(row, col, item)
            
        # Action Button
        delete_btn = DefaultButton("🗑️")
        # delete_btn.setObjectName("POSTableDeleteBtn")
        delete_btn.setToolTip("Delete Row")
        delete_btn.clicked.connect(self.delete_row)
        self.table.setCellWidget(row, 8, delete_btn)
        self.update_total_items_count()

    def delete_row(self):
        button = self.sender()
        if button:
            index = self.table.indexAt(button.pos())
            if index.isValid():
                self.table.removeRow(index.row())
                self.update_total_items_count()

    def clear_all_items(self):
        self.table.setRowCount(0)
        self.update_total_items_count()

    def update_total_items_count(self):
        count = self.table.rowCount()
        self.total_items_label.setText(f"Total Items : {count}")

    def paintEvent(self, event):
        # Optional: Force style refresh on paint
        self.style().unpolish(self)
        self.style().polish(self)
        super().paintEvent(event)
