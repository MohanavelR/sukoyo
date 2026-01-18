
import os
import shutil

# Source and Destination Paths
SOURCE_DIR = "/media/mohan/Mohan_2/Sources/twemoji-master/assets/72x72"
DEST_DIR = "/media/mohan/Mohan_1/work/sukoyo/assets/icons"

# Navigation Items Mapping
NAV_ITEMS = [
    ("📊", "Dashboard", "dashboard"),
    ("📚", "Class", "class"),
    ("🏪", "Store", "store"),
    ("🏭", "Warehouse", "warehouse"),
    ("👥", "Party", "party"),
    ("📦", "Inventory", "inventory"),
    ("📈", "Stock", "stock"),
    ("💰", "Sales", "sales"),
    ("🛒", "Purchase", "purchase"),
    ("💳", "Accounts", "accounts"),
    ("🖥️", "POS Billing", "pos"),
    ("📅", "Attendance", "attendance"),
    ("⚙️", "Settings", "settings"),
]

def get_emoji_filename(emoji_char):
    # Convert emoji to hex codepoint string (lowercase)
    # Twemoji uses lowercase hex separated by dashes
    # e.g. 1f4ca
    hex_codes = []
    for char in emoji_char:
        hex_codes.append(f"{ord(char):x}")
    
    return "-".join(hex_codes)

def copy_icons():
    if not os.path.exists(DEST_DIR):
        print(f"Creating destination directory: {DEST_DIR}")
        os.makedirs(DEST_DIR, exist_ok=True)

    for emoji_char, _, filename_base in NAV_ITEMS:
        # Try base hex code
        base_hex = get_emoji_filename(emoji_char) 
        
        # Possible source filenames
        # Twemoji sometimes omits the variation selector (fe0f) or includes it.
        # We try strict mapping first, then try stripping/adding fe0f if needed.
        
        candidates = [
            f"{base_hex}.png",
            f"{base_hex.replace('-fe0f', '')}.png", # Try without variation selector
             # Sometimes emojis are complex, just in case try ensuring fe0f is there if missing? 
             # usually twemoji filenames don't have fe0f unless necessary for distinction, 
             # but often just the base code point is used.
        ]
        
        found = False
        target_name = f"{filename_base}.png"
        
        for candidate in candidates:
            src_path = os.path.join(SOURCE_DIR, candidate)
            if os.path.exists(src_path):
                dest_path = os.path.join(DEST_DIR, target_name)
                shutil.copy2(src_path, dest_path)
                print(f"✅ Copied {emoji_char} ({candidate}) -> {target_name}")
                found = True
                break
        
        if not found:
            print(f"❌ Could not find icon for {emoji_char} (Tried: {candidates})")

if __name__ == "__main__":
    copy_icons()
