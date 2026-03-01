import tkinter as tk
from colourscheme import ButtonStyle, StyledLabel, BG_COLOUR, ACCENT_COLOUR, TEXT_COLOUR, HOVER_COLOUR, create_frame
from thememanager import theme_manager

class SettingsMenu(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG_COLOUR)
        self.controller = controller
        theme_manager.register(lambda: self.configure(bg=theme_manager.colours["bg"]))

        #Container frame to centralise content
        self.main_frame = create_frame(self)
        self.main_frame.place(relx=0.5, rely=0.5, anchor="center")

        #Title
        self.title = StyledLabel(
            self.main_frame,
            text="Settings Menu",
            size=21,
            bold=True
        )
        self.title.pack(pady=(0, 50))

        #Light/Dark mode toggle button
        self.themeButton = ButtonStyle(
            self.main_frame,
            text=self._theme_button_text(),
            command=self.toggle_theme,
            width=20
        )
        self.themeButton.pack(pady=15)

        #Back button
        backButton = ButtonStyle(
            self.main_frame,
            text="Back to Main Menu",
            command=lambda: controller.show_page("MainMenu"),
            width=20
        )
        backButton.pack(pady=15)

        #Logout button
        logoutButton = ButtonStyle(
            self.main_frame,
            text="Logout",
            command=self.logout,
            width=20
        )
        logoutButton.pack(pady=15)



        #Register with the theme manager so we update when theme changes
        theme_manager.register(self.apply_theme)

    def logout(self):
    # Force back to dark mode on logout
        if not theme_manager.is_dark:
            theme_manager.toggle()
        
        self.controller.current_user = None
        self.controller.show_page("LoginPage")
    
    def _theme_button_text(self):
        return "Switch to Light Mode" if theme_manager.is_dark else "Switch to Dark Mode"

    def toggle_theme(self):
        #Toggle the theme globally - all registered pages will update
        theme_manager.toggle()

    def apply_theme(self):
        #Called by ThemeManager when theme changes - update all widget colours
        c = theme_manager.colours
        self.configure(bg=c["bg"])
        self.main_frame.configure(bg=c["bg"])
        self.title.configure(bg=c["bg"], fg=c["text"])
        self.themeButton.configure(
            text=self._theme_button_text(),
            bg=c["accent"],
            fg=c["text"]
        )
