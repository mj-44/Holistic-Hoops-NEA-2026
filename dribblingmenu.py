import tkinter as tk
from colourscheme import ButtonStyle, StyledLabel, BG_COLOUR, ACCENT_COLOUR, TEXT_COLOUR, HOVER_COLOUR, create_frame
from thememanager import theme_manager

#Creating the class for the dribbling menu
class DribblingMenu(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, background = BG_COLOUR)
        self.controller = controller
        theme_manager.register(lambda: self.configure(background=theme_manager.colours["background"]))

        #Container frame to centralise content on the menu for the user
        main_frame = create_frame(self)
        main_frame.place(relx = 0.5, rely = 0.5, anchor = "center")

        #Titling the page as the "Dribbling Menu"
        title = StyledLabel(
            main_frame,
            text = "Dribbling Menu",
            size = 21,
            bold = True
            
        )
        title.pack(pady=(0,50))

        #Creating button to allow the user to access the full court weave drill
        fullcourtweave_drill_button = ButtonStyle(
            main_frame,
            text = "Fullcourt Weave Drill",
            command = lambda: controller.show_page("FullcourtWeaveDrill"),
            width = 20
        )
        fullcourtweave_drill_button.pack(pady=10)

        #Another button allowing the user to access the spin move drill
        spinmove_drill_button = ButtonStyle(
            main_frame,
            text = "Spin Move Drill",
            command = lambda: controller.show_page("SpinMoveDrill"),
            width = 20
        )
        spinmove_drill_button.pack(pady=10)

        #Final button on the page (for now) allowing the user to access the driving layup drill
        drivinglay_drill_button = ButtonStyle(
            main_frame,
            text = "Driving Lay Drill",
            command = lambda: controller.show_page("DrivingLayDrill"),
            width = 20
        )
        drivinglay_drill_button.pack(pady=10)

        #Button allowing the user to return to the training menu when the user is done with this menu
        backButton = ButtonStyle(
            main_frame,
            text = "Back to Training Menu",
            command = lambda: controller.show_page("TrainingMenu"),
            width = 20
        )
        backButton.pack(pady=10)

        #Automatically applying the theme the user has chosen to this page
        theme_manager.register(self.apply_theme)

    def apply_theme(self):
        colour = theme_manager.colours
        self.configure(colour["background"])
