import tkinter as tk
from colourscheme import ButtonStyle, StyledLabel, BG_COLOUR, ACCENT_COLOUR, TEXT_COLOUR, HOVER_COLOUR, create_frame
from thememanager import theme_manager

class FootworkMenu(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, background = BG_COLOUR)
        self.controller = controller
        theme_manager.register(lambda: self.configure(background=theme_manager.colours["background"]))

        #Container frame to centralise content
        main_frame = create_frame(self)
        main_frame.place(relx = 0.5, rely = 0.5, anchor = "center")

        #Creating the title for the footwork menu
        title = StyledLabel(
            main_frame,
            text = "Footwork Menu",
            size = 21,
            bold = True
            
        )
        title.pack(pady=(0,50))

        #Button to Back Pedal Finishing Drill page
        back_pedal_finishing_button = ButtonStyle(
            main_frame,
            text = "Back Pedal Finishing",
            command = lambda: controller.show_page("BackPedalFinishing"),
            width = 20
        )
        back_pedal_finishing_button.pack(pady=10)

        #Button to Back Pedal Finishing Drill with pumpfake page
        back_pedal_finishing_pf_button = ButtonStyle(
            main_frame,
            text = "BPF w/ Pumpfake",
            command = lambda: controller.show_page("BackPedalFinishingPF"),
            width = 20
        )
        back_pedal_finishing_pf_button.pack(pady=10)

        #Button to Off-Balance Pull-Ups Drill page
        off_balance_pullups_button = ButtonStyle(
            main_frame,
            text = "Off-Balance Pull-Ups",
            command = lambda: controller.show_page("OffBalancePullUps"),
            width = 20
        )
        off_balance_pullups_button.pack(pady=10)                                                                

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
        colour = theme_manager.colours
        self.configure(background=colour["background"])                                    
