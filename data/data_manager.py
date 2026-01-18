import datetime
from .api_client import ApiClient

class DataManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DataManager, cls).__new__(cls)
            cls._instance._init_data()
            cls._instance.api = ApiClient()
        return cls._instance

    def _init_data(self):
        """Initialize with sample data"""
        self.inventory = [
            {"id": "01", "name": "Camlin Geometry Box", "stock": 200, "unit": "Pcs", 
             "price": 85, "status": "In Stock", "value": "₹17,000", "low_stock": False,
             "code": "GB-1204", "brand": "Camlin", "category": "Stationery", 
             "subcategory": "Drawing Tools", "discount": "10%", "tax": "0.5%"},
             
            {"id": "02", "name": "Classmate Sticky Notes", "stock": 100, "unit": "Pcs", 
             "price": 180, "status": "In Stock", "value": "₹18,000", "low_stock": False,
             "code": "CSN-001", "brand": "Classmate", "category": "Stationery", 
             "subcategory": "Office Supplies", "discount": "5%", "tax": "1%"},
             
            {"id": "03", "name": "Kangaro Punch Machine", "stock": 5, "unit": "Pcs", 
             "price": 150, "status": "Low Stock", "value": "₹750", "low_stock": True,
             "code": "KPM-88", "brand": "Kangaro", "category": "Stationery", 
             "subcategory": "Office Supplies", "discount": "8%", "tax": "0%"},
             
            {"id": "04", "name": "Doms Sharpeners", "stock": 50, "unit": "box", 
             "price": 50, "status": "In Stock", "value": "₹2,500", "low_stock": False,
             "code": "DS-22", "brand": "Doms", "category": "Stationery", 
             "subcategory": "Drawing Tools", "discount": "2%", "tax": "0.5%"},
             
            {"id": "05", "name": "Mutton Masala", "stock": 20, "unit": "box", 
             "price": 50, "status": "In Stock", "value": "₹1,000", "low_stock": False,
             "code": "MM-55", "brand": "Everest", "category": "Grocery", 
             "subcategory": "Spices", "discount": "2%", "tax": "0.5%"},
        ]
        
        self.transactions = []
        self.customers = []

    def get_inventory(self):
        """Return all inventory items"""
        return self.inventory

    def fetch_remote_inventory(self, endpoint="inventory"):
        """
        Example of fetching inventory from a remote API.
        This updates the local inventory if successful.
        """
        response = self.api.get(endpoint)
        if response.success:
            # Assuming the API returns a list of items
            self.inventory = response.data
            return True, "Inventory updated"
        return False, response.error

    def get_item(self, code_or_name):
        """Find item by code or name (case-insensitive)"""
        search_term = code_or_name.lower()
        for item in self.inventory:
            if search_term in item['name'].lower() or search_term in item['code'].lower():
                return item
        return None

    def update_stock(self, item_id, quantity_change):
        """Update stock for an item. Negative quantity_change reduces stock."""
        for item in self.inventory:
            if item['id'] == item_id:
                new_stock = item['stock'] + quantity_change
                if new_stock < 0:
                    raise ValueError(f"Insufficient stock for {item['name']}")
                item['stock'] = new_stock
                # Update status based on new stock
                if item['stock'] < 10:
                    item['status'] = "Low Stock"
                    item['low_stock'] = True
                else:
                    item['status'] = "In Stock"
                    item['low_stock'] = False
                return True
        return False

    def add_transaction(self, items, total_amount, customer_details=None):
        """Record a new transaction"""
        transaction = {
            "id": f"INV-{len(self.transactions) + 1000}",
            "date": datetime.datetime.now().strftime("%d/%m/%Y %H:%M"),
            "items": items,
            "total": total_amount,
            "customer": customer_details
        }
        self.transactions.append(transaction)
        return transaction['id']
