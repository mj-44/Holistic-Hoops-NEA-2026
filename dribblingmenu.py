import tkinter as tk
from colourscheme import ButtonStyle, StyledLabel, BG_COLOUR, ACCENT_COLOUR, TEXT_COLOUR, HOVER_COLOUR, create_frame

class DribblingMenu(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg = BG_COLOUR)
        self.controller = controller

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

        #Button to return to the training menu when needed
        backButton = ButtonStyle(
            main_frame,
            text = "Back to Training Menu",
            command = lambda: controller.show_page("TrainingMenu"),
            width = 20
        )
        backButton.pack(pady=10)