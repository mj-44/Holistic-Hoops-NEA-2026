import tkinter as tk
from colourscheme import ButtonStyle, StyledLabel, BG_COLOUR, ACCENT_COLOUR, TEXT_COLOUR, HOVER_COLOUR, create_frame
from thememanager import theme_manager

class ShootingMenu(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg = BG_COLOUR)
        self.controller = controller
        theme_manager.register(lambda: self.configure(bg=theme_manager.colours["bg"]))

        #Container frame to centralise content
        main_frame = create_frame(self)
        main_frame.place(relx = 0.5, rely = 0.5, anchor = "center")

        #Creating the title for the shooting menu
        title = StyledLabel(
            main_frame,
            text = "Shooting Menu",
            size = 21,
            bold = True
            
        )
        title.pack(pady=(0,50))

        #Button to Around the World Shooting Drill page
        around_the_world_button = ButtonStyle(
            main_frame,
            text = "Around the World",
            command = lambda: controller.show_page("AroundTheWorld"),
            width = 20
        )
        around_the_world_button.pack(pady=10)

        #Button to navigate to the Dribble Pull-Up Drill page
        dribble_pullup_button = ButtonStyle(
            main_frame,
            text = "Dribble Pull-Up",
            command = lambda: controller.show_page("DribblePullUpDrill"),
            width = 20
        )
        dribble_pullup_button.pack(pady=10)

        #Button to navigate to the Range Rumble Shooting Drill page
        range_rumble_button = ButtonStyle(
            main_frame,
            text = "Range Rumble",
            command = lambda: controller.show_page("RangeRumble"),
            width = 20
        )
        range_rumble_button.pack(pady=10)

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
        self.configure(bg=c["bg"])