import tkinter as tk
from colourscheme import ButtonStyle, StyledLabel, BG_COLOUR, ACCENT_COLOUR, TEXT_COLOUR, HOVER_COLOUR, create_frame

class TrainingMenu(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg = BG_COLOUR)
        self.controller = controller

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

        #Button to start a new training session
        shootingButton = ButtonStyle(
            main_frame,
            text = "Shooting 🎯",
            command = lambda: controller.show_page("ShootingMenu"),
            width = 20
        )
        shootingButton.pack(pady=10)

        dribblingButton = ButtonStyle(
            main_frame,
            text = "Dribbling 🏀",
            command = lambda: controller.show_page("DribblingMenu"),
            width = 20
        )
        dribblingButton.pack(pady=10)

        footworkButton = ButtonStyle(
            main_frame,
            text = "Footwork 👟",
            command = lambda: controller.show_page("FootworkMenu"),
            width = 20
        )
        footworkButton.pack(pady=10)

        finishingButton = ButtonStyle(
            main_frame,
            text = "Finishing 🏆",
            command = lambda: controller.show_page("FinishingMenu"),
            width = 20
        )
        finishingButton.pack(pady=10)
        
        backButton = ButtonStyle(
            main_frame,
            text = "Back to Main Menu",
            command = lambda: controller.show_page("MainMenu"),
            width = 20
        )
        backButton.pack(pady=30)