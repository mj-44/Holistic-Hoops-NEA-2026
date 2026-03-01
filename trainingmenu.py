import tkinter as tk
from colourscheme import ButtonStyle, StyledLabel, BG_COLOUR, ACCENT_COLOUR, TEXT_COLOUR, HOVER_COLOUR, create_frame
from thememanager import theme_manager

class TrainingMenu(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg = BG_COLOUR)
        self.controller = controller
        theme_manager.register(lambda: self.configure(bg=theme_manager.colours["bg"]))

        #Container frame to centralise content
        main_frame = create_frame(self)
        main_frame.place(relx = 0.5, rely = 0.5, anchor = "center")

        #Creating the title for the training menu
        title = StyledLabel(
            main_frame,
            text = "Training Menu",
            size = 21,
            bold = True
            
        )
        title.pack(pady=(0,50))

        #Button to navigate to the shooting menu
        shootingButton = ButtonStyle(
            main_frame,
            text = "Shooting 🎯",
            command = lambda: controller.show_page("ShootingMenu"),
            width = 20
        )
        shootingButton.pack(pady=10)

        #Button to navigate to the dribbling menu
        dribblingButton = ButtonStyle(
            main_frame,
            text = "Dribbling 🏀",
            command = lambda: controller.show_page("DribblingMenu"),
            width = 20
        )
        dribblingButton.pack(pady=10)

        #Button to navigate to the footwork menu
        footworkButton = ButtonStyle(
            main_frame,
            text = "Footwork 👟",
            command = lambda: controller.show_page("FootworkMenu"),
            width = 20
        )
        footworkButton.pack(pady=10)

        #Button to navigate to the finishing menu
        finishingButton = ButtonStyle(
            main_frame,
            text = "Finishing 🏆",
            command = lambda: controller.show_page("FinishingMenu"),
            width = 20
        )
        finishingButton.pack(pady=10)
        
        #Button to return to the main menu when needed
        backButton = ButtonStyle(
            main_frame,
            text = "Back to Main Menu",
            command = lambda: controller.show_page("MainMenu"),
            width = 20
        )
        backButton.pack(pady=30)

        theme_manager.register(self.apply_theme)

    def apply_theme(self):
        c = theme_manager.colours
        self.configure(bg=c["bg"])