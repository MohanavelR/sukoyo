from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QPushButton, 
    QFrame, QLineEdit, QTableWidget, QTableWidgetItem, QHeaderView,
    QSpacerItem, QSizePolicy, QComboBox, QMessageBox
)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon
from components.button import PrimaryButton, SecondaryButton, DefaultButton
import os

class POSPage(QWidget):
    def __init__(self, data_manager):
        super().__init__()
        self.setObjectName("POSPage")
        self.data_manager = data_manager
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
        search_input.returnPressed.connect(self._on_search_return)
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
        save_bill.clicked.connect(self.save_bill)
        
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
        # self._populate_sample_data() # Removed sample data population

    def _on_search_return(self):
        """Handle search input (barcode scan simulation)"""
        search_input = self.findChild(QLineEdit, "POSSearchInput")
        query = search_input.text().strip()
        if not query:
            return
            
        item = self.data_manager.get_item(query)
        if item:
            self.add_item_to_table(item)
            search_input.clear()
        else:
            # Simple feedback (could be improved with a toast/message box)
            print(f"Item not found: {query}")

    def add_item_to_table(self, item_data):
        """Add item to table, or increment quantity if exists"""
        # Logic to check if item already exists in table
        for row in range(self.table.rowCount()):
            item_widget = self.table.item(row, 1) # Item name column
            if item_widget and item_widget.text() == item_data['name']:
                # Item exists, update quantity
                qty_item = self.table.item(row, 3)
                current_qty = int(qty_item.text())
                new_qty = current_qty + 1
                qty_item.setText(str(new_qty))
                
                # Update Amount
                price = float(item_data['price'])
                amount_item = self.table.item(row, 7)
                amount_item.setText(f"₹{price * new_qty}")
                
                self.update_bill_details()
                return

        # Add new row
        row = self.table.rowCount()
        self.table.insertRow(row)
        
        # Mapping data to columns: 
        # #, Item, Unit, Quantity, Price/Unit, Discount, Tax, Amount, Action
        
        # #
        self.table.setItem(row, 0, QTableWidgetItem(str(row + 1)))
        
        # Item
        self.table.setItem(row, 1, QTableWidgetItem(item_data['name']))
        
        # Unit
        self.table.setItem(row, 2, QTableWidgetItem(item_data['unit']))
        
        # Quantity
        qty_item = QTableWidgetItem("1")
        qty_item.setTextAlignment(Qt.AlignCenter)
        self.table.setItem(row, 3, qty_item)
        
        # Price
        self.table.setItem(row, 4, QTableWidgetItem(f"₹{item_data['price']}"))
        
        # Discount
        self.table.setItem(row, 5, QTableWidgetItem(item_data.get('discount', '-')))
        
        # Tax
        self.table.setItem(row, 6, QTableWidgetItem(item_data.get('tax', '-')))
        
        # Amount
        amount = item_data['price'] # 1 qty
        self.table.setItem(row, 7, QTableWidgetItem(f"₹{amount}"))
            
        # Action Button
        delete_btn = DefaultButton("🗑️")
        delete_btn.setToolTip("Delete Row")
        delete_btn.clicked.connect(self.delete_row)
        self.table.setCellWidget(row, 8, delete_btn)
        
        self.update_total_items_count()
        self.update_bill_details()

    def update_bill_details(self):
        """Calculate and update sidebar totals"""
        total = 0
        for row in range(self.table.rowCount()):
            amount_str = self.table.item(row, 7).text().replace('₹', '')
            total += float(amount_str)
            
        # Update Total Amount Label
        total_val_lbl = self.findChild(QLabel, "POSTotalAmountValue")
        if total_val_lbl:
            total_val_lbl.setText(f"₹{total}")
            
    def save_bill(self):
        """Save transaction to DataManager"""
        if self.table.rowCount() == 0:
            return

        items = []
        total_amount = 0
        
        try:
            for row in range(self.table.rowCount()):
                item_name = self.table.item(row, 1).text()
                qty = int(self.table.item(row, 3).text())
                price_str = self.table.item(row, 7).text().replace('₹', '')
                amount = float(price_str)
                total_amount += amount
                
                # Update Stock
                # We need item ID, but we only have name here. 
                # Ideally we should store ID in user data of the item.
                # For this refactor, we'll look up by name/code via DataManager internally 
                # or assume we can find it.
                item = self.data_manager.get_item(item_name)
                if item:
                    self.data_manager.update_stock(item['id'], -qty)
                
                items.append({
                    "name": item_name,
                    "qty": qty,
                    "amount": amount
                })
            
            # Record Transaction
            invoice_id = self.data_manager.add_transaction(items, total_amount)
            print(f"Bill Saved! Invoice: {invoice_id}")
            
            # Clear UI
            self.clear_all_items()
            self.update_bill_details()
            
            # Show success
            QMessageBox.information(self, "Success", f"Bill saved successfully! Invoice: {invoice_id}")

        except Exception as e:
            print(f"Error saving bill: {e}")
            QMessageBox.critical(self, "Error", f"Failed to save bill: {str(e)}")

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
