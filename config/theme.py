class Theme:
    """Theme definitions for the dashboard"""
    
    THEME_DARK = {
        "bg_primary": "#0F172A",
        "bg_secondary": "#1E293B",
        "bg_accent": "#334155",
        "text_primary": "#F8FAFC",
        "text_secondary": "#CBD5E1",
        "text_accent": "#60A5FA",
        "text_disabled": "#64748B", 
        "border_primary": "#334155", 
        "border_secondary": "#475569",
        "border_accent": "#3B82F6", 
        "hover_bg_primary": "#1E293B",
        "hover_bg_secondary": "#334155",
        "hover_bg_accent": "#1D4ED8", 
        "hover_text_primary": "#FFFFFF", 
        "hover_text_secondary": "#E2E8F0",
        "hover_text_accent": "#FFFFFF",
        "active_bg_primary": "#334155", 
        "active_bg_secondary": "#3B82F6",
        "active_bg_accent": "#2563EB", 
        "active_text_primary": "#FFFFFF",
        "active_text_secondary": "#F8FAFC",
        "active_text_accent": "#FFFFFF",
    }
    
    THEME_PURPLE = {
        "bg_primary": "#F5F3FF", 
        "bg_secondary": "#FFFFFF",
        "bg_accent": "#EDE9FE",
        "text_primary": "#3B0764",
        "text_secondary": "#6B21A8",
        "text_accent": "#7C3AED",
        "text_disabled": "#A78BFA",
        "border_primary": "#DDD6FE",
        "border_secondary": "#C4B5FD",
        "border_accent": "#7C3AED", 
        "hover_bg_primary": "#EDE9FE",
        "hover_bg_secondary": "#DDD6FE",
        "hover_bg_accent": "#C4B5FD", 
        "hover_text_primary": "#3B0764",
        "hover_text_secondary": "#5B21B6",
        "hover_text_accent": "#6D28D9", 
        "active_bg_primary": "#DDD6FE", 
        "active_bg_secondary": "#C4B5FD",
        "active_bg_accent": "#7C3AED", 
        "active_text_primary": "#3B0764", 
        "active_text_secondary": "#4C1D95",
        "active_text_accent": "#FFFFFF",
    }
    
    THEME_LIGHT = {
        "bg_primary": "#F9FAFB", 
        "bg_secondary": "#FFFFFF",
        "bg_accent": "#F1F5F9",
        "text_primary": "#0F172A", 
        "text_secondary": "#475569", 
        "text_accent": "#2563EB",
        "text_disabled": "#94A3B8", 
        "border_primary": "#E2E8F0", 
        "border_secondary": "#CBD5E1",
        "border_accent": "#2563EB", 
        "hover_bg_primary": "#F1F5F9",
        "hover_bg_secondary": "#E2E8F0",
        "hover_bg_accent": "#DBEAFE", 
        "hover_text_primary": "#0F172A",
        "hover_text_secondary": "#1E293B",
        "hover_text_accent": "#1D4ED8",
        "active_bg_primary": "#E2E8F0", 
        "active_bg_secondary": "#DBEAFE",
        "active_bg_accent": "#2563EB", 
        "active_text_primary": "#0F172A",
        "active_text_secondary": "#1E293B",
        "active_text_accent": "#FFFFFF",
    }
    def get_theme(self, theme_name):
        if theme_name == "dark":
            return self.THEME_DARK
        elif theme_name == "purple":
            return self.THEME_PURPLE
        elif theme_name == "light":
            return self.THEME_LIGHT
        else:
            raise ValueError(f"Unknown theme name: {theme_name}")
        
    