#thememanager.py
#Central theme manager - holds current colour scheme and notifies registered pages on change

#Default dark mode colours (original scheme)
DARK_THEME = {
    "bg": "#000000",
    "accent": "#D4A017",
    "text": "#FFFFFF",
    "hover": "#FFA500",
    "entry_bg": "#1a1a1a",
    "entry_border": "#333333",
    "subtext": "#666666",
    "error": "#FF4444",
    "success": "#44FF44",
}

#Light mode colours
LIGHT_THEME = {
    "bg": "#FFFFFF",
    "accent": "#82C8E5",
    "text": "#272757",
    "hover": "#5757a7",
    "entry_bg": "#FFFFFF",
    "entry_border": "#CCCCCC",
    "subtext": "#888888",
    "error": "#CC0000",
    "success": "#007700",
}

class ThemeManager:
    def __init__(self):
        self._dark_mode = True
        self._listeners = []  #list of callbacks to call when theme changes

    @property
    def colours(self):
        return DARK_THEME if self._dark_mode else LIGHT_THEME

    @property
    def is_dark(self):
        return self._dark_mode

    def toggle(self):
        self._dark_mode = not self._dark_mode
        self._notify_listeners()

    def register(self, callback):
        #Register a function to be called when the theme changes
        self._listeners.append(callback)

    def _notify_listeners(self):
        for callback in self._listeners:
            try:
                callback()
            except Exception:
                pass  #Page may have been destroyed, skip silently

#Global singleton - import this everywhere
theme_manager = ThemeManager()