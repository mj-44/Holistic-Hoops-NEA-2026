import tkinter as tk
from colourscheme import ButtonStyle, StyledLabel, create_frame
from thememanager import theme_manager

class HomePage(tk.Frame):
    #Home page to welcome the user to the application with buttons redirecting to login and registration page
    def __init__(self, parent, controller):
        super().__init__(parent, background = "#000000")
        self.controller = controller
        theme_manager.register(lambda: self.configure(background=theme_manager.colours["background"]))

        #Container frame to centre content
        main_frame = create_frame(self)
        main_frame.place(relx = 0.5, rely = 0.5, anchor = "center")

        #App Title and motto
        title = StyledLabel(
            main_frame,
            text = "Hollistic Hoops",
            size = 28,
            bold = True
        )
        title.pack(pady=(0,50))

        subtitle = StyledLabel(
            main_frame,
            text = "Train, Compete, Repeat",
            size = 14
        )
        subtitle.pack(pady=(0,80))

        #Login button
        loginButton = ButtonStyle(
            main_frame,
            text = "Login",
            command = lambda: controller.show_page("LoginPage"),
            width = 20
        )
        loginButton.pack(pady = 15)

        #Register button
        registerButton = ButtonStyle(
            main_frame,
            text = "Register",
            command = lambda: controller.show_page("RegisterPage"),
            width = 20
        )
        registerButton.pack(pady=15)

        theme_manager.register(self.apply_theme)

    def apply_theme(self):
        colour = theme_manager.colours
        self.configure(background=colour["background"])
