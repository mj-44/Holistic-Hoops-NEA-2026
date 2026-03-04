import tkinter as tk
from colourscheme import ButtonStyle, StyledLabel, BG_COLOUR, ACCENT_COLOUR, TEXT_COLOUR, HOVER_COLOUR, create_frame
from thememanager import theme_manager

class DribblingMenu(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, background = BG_COLOUR)
        self.controller = controller
        theme_manager.register(lambda: self.configure(background=theme_manager.colours["background"]))

        #Container frame to centralise content
        main_frame = create_frame(self)
        main_frame.place(relx = 0.5, rely = 0.5, anchor = "center")

        #Creating the title for the dribbling menu
        title = StyledLabel(
            main_frame,
            text = "Dribbling Menu",
            size = 21,
            bold = True
            
        )
        title.pack(pady=(0,50))

        #Button to Fullcourt Weave Drill page
        alley_drill_button = ButtonStyle(
            main_frame,
            text = "Fullcourt Weave Drill",
            command = lambda: controller.show_page("FullcourtWeaveDrill"),
            width = 20
        )
        alley_drill_button.pack(pady=10)

        #Button to Spin Move Drill page
        cone_touch_finishing_button = ButtonStyle(
            main_frame,
            text = "Spin Move Drill",
            command = lambda: controller.show_page("SpinMoveDrill"),
            width = 20
        )
        cone_touch_finishing_button.pack(pady=10)

        #Button to Driving lay Drill page
        fresno_attack_button = ButtonStyle(
            main_frame,
            text = "Driving Lay Drill",
            command = lambda: controller.show_page("DrivingLayDrill"),
            width = 20
        )
        fresno_attack_button.pack(pady=10)

        #Button to return to the training menu when needed
        backButton = ButtonStyle(
            main_frame,
            text = "Back to Training Menu",
            command = lambda: controller.show_page("TrainingMenu"),
            width = 20
        )
        backButton.pack(pady=10)

        theme_manager.register(self.apply_theme)

    def apply_theme(self):
        c = theme_manager.colours
        self.configure(background=c["background"])