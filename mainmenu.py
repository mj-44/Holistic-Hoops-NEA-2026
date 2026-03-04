import tkinter as tk
from colourscheme import ButtonStyle, StyledLabel, BG_COLOUR, ACCENT_COLOUR, TEXT_COLOUR, HOVER_COLOUR, create_frame
from thememanager import theme_manager

class MainMenu(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, background = BG_COLOUR)
        self.controller = controller
        theme_manager.register(lambda: self.configure(background=theme_manager.colours["background"]))

        #Contrainer frame to centralise content
        main_frame = create_frame(self)
        main_frame.place(relx = 0.5, rely = 0.5, anchor = "center")

        #Creating the title for the main menu
        title = StyledLabel(
            main_frame,
            text = "Hollistic Hoops",
            size = 21,
            bold = True
            
        )
        title.pack(pady=(0,50))

        #Button to training menu
        trainingButton = ButtonStyle(
            main_frame,
            text = "Training 🏀",
            command = lambda: controller.show_page("TrainingMenu"),
            width = 15
        )
        trainingButton.pack(pady=10)

        #Button to settings menu
        settingsButton = ButtonStyle(
            main_frame,
            text = "Settings ⚙️",
            command = lambda: controller.show_page("SettingsMenu"),
            width = 15
        )
        settingsButton.pack(pady=10)

        #Button to tracker menu
        trackerButton = ButtonStyle(
            main_frame,
            text = "Tracker 📊",
            command = lambda: controller.show_page("TrackerMenu"),
            width = 15
        )
        trackerButton.pack(pady=10)

        #Button to comparison menu
        comparisonButton = ButtonStyle(
            main_frame,
            text = "Comparison 𝐕𝐒",
            command = lambda: controller.show_page("ComparisonMenu"),
            width = 15
        )
        comparisonButton.pack(pady=10)

        theme_manager.register(self.apply_theme)

    def apply_theme(self):
        c = theme_manager.colours
        self.configure(background=c["background"])
