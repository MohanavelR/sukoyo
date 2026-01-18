import sys
import os

# Add the parent directory to sys.path to allow imports from sukoyo
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data.api_client import ApiClient

def test_api():
    # Initialize ApiClient
    api = ApiClient()
    
    # Configure with a mock API (JSONPlaceholder)
    api.configure(base_url="https://jsonplaceholder.typicode.com")
    
    print("Fetching posts from JSONPlaceholder...")
    response = api.get("posts/1")
    
    if response.success:
        print("\nSuccess!")
        print(f"Message: {response.message}")
        print(f"Data: {response.data}")
    else:
        print("\nError!")
        print(f"Error Message: {response.error}")
        if response.data:
            print(f"Details: {response.data}")

def test_data_manager_integration():
    from data.data_manager import DataManager
    dm = DataManager()
    
    print("\nTesting DataManager integration...")
    # Configure DataManager's internal api client
    dm.api.configure(base_url="https://jsonplaceholder.typicode.com")
    
    # Fetch from a mock endpoint
    success, message = dm.fetch_remote_inventory(endpoint="todos/1")
    
    if success:
        print(f"Integration Success: {message}")
        print(f"Current Inventory (Mock Item): {dm.inventory}")
    else:
        print(f"Integration Error: {message}")

if __name__ == "__main__":
    test_api()
    test_data_manager_integration()
