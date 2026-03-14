#Created a page to centralise the management of the theme the user has chosen for the application and updates the page
#with theme almost simulataneously

#Constant for the colours used when in dark mode (original scheme)
DARK_THEME = {
    "background": "#000000",
    "accent": "#D4A017",
    "text": "#FFFFFF",
    "hover": "#FFA500",
    "entry_background": "#1a1a1a",
    "entry_border": "#333333",
    "subtext": "#666666",
    "error": "#FF4444",
    "success": "#44FF44",
}

#Colours used when the application is in light mode
LIGHT_THEME = {
    "background": "#FFFFFF",
    "accent": "#82C8E5",
    "text": "#272757",
    "hover": "#5757a7",
    "entry_background": "#FFFFFF",
    "entry_border": "#CCCCCC",
    "subtext": "#888888",
    "error": "#CC0000",
    "success": "#007700",
}

#Creating the class for the theme manager
class ThemeManager:
    def __init__(self):
        self._dark_mode = True
        self._listeners = []  #Creating a list to the callbacks to call when theme changes

    #Sets the theme to the mode the user has chosen to use on the application
    @property
    def colours(self):
        if self._dark_mode:
            return DARK_THEME
        else:
            return LIGHT_THEME
        
    #A getter which finds out if the page is in dark mode or not
    @property
    def is_dark(self):
        return self._dark_mode

    #A toggle which enables the user to switch between light and dark mode
    def toggle(self):
        self._dark_mode = not self._dark_mode
        self._notify_listeners()

    #Other parts of the app can respond to this theme change in accordance with what the theme they have chosen is
    def register(self, callback):
        #Register a function to be called when the theme changes
        self._listeners.append(callback)

    #Calls all callbacks during a theme change
    def _notify_listeners(self):
        for callback in self._listeners:
            try:
                callback()
            except Exception:
                pass  #Page may have been destroyed, skip silently

#Global singleton - import this everywhere
theme_manager = ThemeManager()
