"""
Theme definitions for Chatterbox
"""

# Dark Theme (Default)
DARK_THEME = {
    "name": "dark",
    "bg": "#1e1e1e",
    "fg": "#d4d4d4",
    "bg_secondary": "#252526",
    "bg_tertiary": "#2d2d30",
    "border": "#3e3e42",
    "input_bg": "#3c3c3c",
    "input_fg": "#cccccc",
    "button_bg": "#0e639c",
    "button_fg": "#ffffff",
    "button_hover": "#1177bb",
    "button_active": "#094771",
    "slider_bg": "#3c3c3c",
    "slider_fg": "#0e639c",
    "scrollbar_bg": "#3e3e42",
    "scrollbar_fg": "#686868",
    "label_fg": "#cccccc",
    "placeholder_fg": "#858585",
    "highlight_bg": "#094771",
    "highlight_fg": "#ffffff",
}

# Light Theme
LIGHT_THEME = {
    "name": "light",
    "bg": "#ffffff",
    "fg": "#000000",
    "bg_secondary": "#f3f3f3",
    "bg_tertiary": "#e8e8e8",
    "border": "#cccccc",
    "input_bg": "#ffffff",
    "input_fg": "#000000",
    "button_bg": "#007acc",
    "button_fg": "#ffffff",
    "button_hover": "#005a9e",
    "button_active": "#004578",
    "slider_bg": "#e0e0e0",
    "slider_fg": "#007acc",
    "scrollbar_bg": "#f0f0f0",
    "scrollbar_fg": "#c0c0c0",
    "label_fg": "#000000",
    "placeholder_fg": "#999999",
    "highlight_bg": "#cce8ff",
    "highlight_fg": "#000000",
}

# Available themes
THEMES = {
    "dark": DARK_THEME,
    "light": LIGHT_THEME
}

def get_theme(theme_name: str = "dark"):
    """Get theme by name, defaults to dark"""
    return THEMES.get(theme_name, DARK_THEME)
