class Theme:
    """Theme definitions for the dashboard"""
    
    # Dark Theme (Neutral/Zinc) - Kept as distinct 3rd option
    THEME_DARK = {
        "bg_primary": "#09090b",      # Zinc 950
        "bg_secondary": "#18181b",    # Zinc 900
        "bg_accent": "#27272a",       # Zinc 800
        "text_primary": "#f4f4f5",    # Zinc 100
        "text_secondary": "#a1a1aa",  # Zinc 400
        "text_accent": "#38bdf8",     # Sky 400
        "text_disabled": "#52525b",   # Zinc 600
        "border_primary": "#27272a",  # Zinc 800
        "border_secondary": "#3f3f46",# Zinc 700
        "border_accent": "#38bdf8",   # Sky 400
        "hover_bg_primary": "#18181b",
        "hover_bg_secondary": "#27272a",
        "hover_bg_accent": "#3f3f46",
        "hover_text_primary": "#ffffff",
        "hover_text_secondary": "#d4d4d8",
        "hover_text_accent": "#7dd3fc",
        "active_bg_primary": "#27272a",
        "active_bg_secondary": "#3f3f46",
        "active_bg_accent": "#0ea5e9",
        "active_text_primary": "#ffffff",
        "active_text_secondary": "#e4e4e7",
        "active_text_accent": "#ffffff",
    }
    
    # Purple Theme (User Specified)
    THEME_PURPLE = {
        "bg_primary": "#1a1625",
        "bg_secondary": "#1f1a2d",
        "bg_accent": "#231b2e",
        "text_primary": "#ffffff",
        "text_secondary": "#e5e7eb",
        "text_accent": "#9ca3af",
        "text_disabled": "#6b7280",   # Added for completeness
        "border_primary": "#2d2936",
        "border_secondary": "#353142",
        "border_accent": "#3e3a4c",
        "hover_bg_primary": "#241e33",
        "hover_bg_secondary": "#29223b",
        "hover_bg_accent": "#2d2440",
        "hover_text_primary": "#ffffff",
        "hover_text_secondary": "#e4e7ee",
        "hover_text_accent": "#f1f5f9",
        "active_bg_primary": "#161221",
        "active_bg_secondary": "#1a1627",
        "active_bg_accent": "#1e1828",
        "active_text_primary": "#dbeafe",
        "active_text_secondary": "#cbd5e1",
        "active_text_accent": "#f8fafc",
    }
    
    # Light Theme (User Specified)
    THEME_LIGHT = {
        "bg_primary": "#ffffff",
        "bg_secondary": "#f3f4f6",
        "bg_accent": "#e5e7eb",
        "text_primary": "#111827",
        "text_secondary": "#090a0b",
        "text_accent": "#4b4d51",
        "text_disabled": "#9ca3af",   # Added for completeness
        "border_primary": "#e5e7eb",
        "border_secondary": "#d1d5db",
        "border_accent": "#c2ccd7",
        "hover_bg_primary": "#f5f5f5",
        "hover_bg_secondary": "#eef0f2",
        "hover_bg_accent": "#ededed",
        "hover_text_primary": "#0a0f1f",
        "hover_text_secondary": "#334155",
        "hover_text_accent": "#0f172a",
        "active_bg_primary": "#ececec",
        "active_bg_secondary": "#e2e4e7",
        "active_bg_accent": "#e5e5e5",
        "active_text_primary": "#000000",
        "active_text_secondary": "#1e293b",
        "active_text_accent": "#0a0f1f",
    }

    def get_theme(self, theme_name):
        if theme_name == "dark":
            return self.THEME_DARK
        elif theme_name == "purple":
            return self.THEME_PURPLE
        elif theme_name == "light":
            return self.THEME_LIGHT
        else:
            # Default to dark if unknown
            return self.THEME_DARK