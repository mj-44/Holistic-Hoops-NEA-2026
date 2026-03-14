import tkinter as tk
from colourscheme import ButtonStyle, StyledLabel, BG_COLOUR, ACCENT_COLOUR, TEXT_COLOUR, HOVER_COLOUR, create_frame
from thememanager import theme_manager

#Creating the class for the training menu so that it can be used in the application
class TrainingMenu(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, background = BG_COLOUR)
        self.controller = controller
        theme_manager.register(lambda: self.configure(background=theme_manager.colours["background"]))

        #Creating a frame so that the content of the page can be centralised
        main_frame = create_frame(self)
        main_frame.place(relx = 0.5, rely = 0.5, anchor = "center")

        #Creating a title for the training menu
        title = StyledLabel(
            main_frame,
            text = "Training Menu",
            size = 21,
            bold = True
            
        )
        title.pack(pady=(0,50))

        #Buttons allowing the user to access the respective menu they wish to access to find
        #drills for the aspect of their game they want to work on
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
        
        #Button to return to the main menu if the user were to be done with training for the time being
        backButton = ButtonStyle(
            main_frame,
            text = "Back to Main Menu",
            command = lambda: controller.show_page("MainMenu"),
            width = 20
        )
        backButton.pack(pady=30)

        #Automatically applies the theme that the user has chosen (light or dark mode) onto the page
        theme_manager.register(self.apply_theme)

    def apply_theme(self):
        colour = theme_manager.colours
        self.configure(background=colour["background"])
