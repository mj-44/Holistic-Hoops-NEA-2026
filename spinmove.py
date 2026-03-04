import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from colourscheme import ButtonStyle, StyledLabel, BG_COLOUR, ACCENT_COLOUR, TEXT_COLOUR, create_frame
from thememanager import theme_manager

class SpinMoveDrill(tk.Frame):
    #Dribble Pull-Up Drill page class
    
    def __init__(self, parent, controller):
        super().__init__(parent, background = BG_COLOUR)
        self.controller = controller
        theme_manager.register(lambda: self.configure(background=theme_manager.colours["background"]))

        #Initialise variables for stat tracking
        self.makes = 0
        self.misses = 0
        self.total_shots = 50 #25 from each wing
        
        #Container frame to centralise content
        main_frame = create_frame(self)
        main_frame.place(relx = 0.5, rely = 0.5, anchor = "center")

        #Creating the title for the Full Court Weave page
        title = StyledLabel(
            main_frame,
            text = "Spin Move Drill",
            size = 21,
            bold = True
            
        )
        title.pack(pady=(20,10))

        subtitle = StyledLabel(
            main_frame,
            text = "Drill Focused on spin moves near the basket into a finish",
            size = 14,
            bold = False
        )
        subtitle.pack(pady=(0,20))

        #Load the image
        drillImage = Image.open("assets/spin_move_drill.png")

        #Resize the image to fit within the app window while maintaining aspect ratio
        drillImage = drillImage.resize((500, 300), Image.Resampling.LANCZOS)

        #Convert the image to a format Tkinter can use
        self.drillPhoto = ImageTk.PhotoImage(drillImage)
        imageLabel = tk.Label(main_frame, image = self.drillPhoto, background = BG_COLOUR)
        imageLabel.pack(pady=(20))

        #Displaying the instructions for the drill
        instructionsLabel = StyledLabel(
            main_frame,
            text = "Instructions:",
            size = 16,
            bold = True
        )
        instructionsLabel.pack(pady=(20,10))

        #Give the instructions step by step
        steps = [
            "1. Start from the 3 point line.",
            "2. Dribble towards the baseline.",
            "3. Perform a spin move near the basket.",
            "4. Finish with a layup or dunk.",
            "5. Repeat 25 times each side and record a score out of 50."
        ]

        for step in steps:
            stepLabel = StyledLabel(
                main_frame,
                text = step,
                size = 12,
                bold = False
            )
            stepLabel.pack(pady=5, padx=40, anchor="w")

        #Creating the section to actively display the score
        scoreFrame = create_frame(main_frame)
        scoreFrame.pack(pady=(30))

        #Current Score Display
        self.scoreLabel = StyledLabel(
            scoreFrame,
            text = f"Score: {self.makes}/{self.makes + self.misses}",
            size = 20,
            bold = True
        )
        self.scoreLabel.pack(pady=10)

        #Progress Display
        self.progressLabel = StyledLabel(
            scoreFrame,
            text = f"Shots Taken: {self.makes + self.misses}/{self.total_shots}",
            size = 14,
            bold = False
        )
        self.progressLabel.pack(pady=5)

        #Shooting Percentage Display
        self.percentageLabel = StyledLabel(
            scoreFrame,
            text = f"Shooting Percentage: 0.0%",
            size = 14,
            bold = False
        )
        self.percentageLabel.pack(pady=5)

        #Buttons to record makes and misses
        buttonContainer = create_frame(main_frame)
        buttonContainer.pack(pady=(20))

        #Make Button
        self.makeButton = ButtonStyle(
            buttonContainer,
            text = "MAKE ✔",
            command = self.record_make,
            width = 12
        )
        self.makeButton.pack(side = "left", padx=10)

        #Miss Button
        self.missButton = ButtonStyle(
            buttonContainer,
            text = "MISS ✘",
            command = self.record_miss,
            width = 12
        )
        self.missButton.pack(side = "left", padx=10)

        #Button to return to the shooting menu when needed
        backButton = ButtonStyle(
            main_frame,
            text = "← Back",
            command = lambda: controller.show_page("DribblingMenu"),
            width = 20
        )
        backButton.pack(pady=10)

        #Reset button to reset the drill stats
        resetButton = ButtonStyle(
            main_frame,
            text = "Reset Drill",
            command = self.reset_drill,
            width = 12
        )
        resetButton.pack(side = "left", pady=10)

        theme_manager.register(self.apply_theme)

    def apply_theme(self):
        c = theme_manager.colours
        self.configure(background=c["background"])

    def record_make(self):
        #Reording a made shot
        if self.makes + self.misses >= self.total_shots:
            messagebox.showinfo("Drill Complete", "You have completed all 50 shots!")
            return
        
        self.makes += 1
        self.update_display()

        if self.makes + self.misses >= self.total_shots:
            self.drill_complete()

    def record_miss(self):
        #Recording a missed shot
        if self.makes + self.misses >= self.total_shots:
            messagebox.showinfo("Drill Complete", "You have completed all 50 shots!")
            return
        
        self.misses += 1
        self.update_display()

        if self.makes + self.misses >= self.total_shots:
            self.drill_complete()

    def update_display(self):
        #Updating the score displays
        self.scoreLabel.config(text = f"Score: {self.makes}/{self.makes + self.misses}")
        shots_taken = self.makes + self.misses
        self.progressLabel.config(text = f"Shots Taken: {shots_taken}/{self.total_shots}") #roads the percentage to 1 decimal place

        if shots_taken > 0:
            percentage = (self.makes / shots_taken) * 100
            self.percentageLabel.config(text = f"Shooting %: {percentage: .1f}%")
        else:
            self.percentageLabel.config(text = "Shooting %: 0.0%")
        
    def drill_complete(self):
        #Notify user that the drill is complete
        percentage = (self.makes / self.total_shots) * 100
        
        message = f"Drill Complete!\n\nFinal Score: {self.makes}/{self.total_shots}\nShooting Percentage: {percentage: .1f}%"
        messagebox.showinfo("Drill Complete", message)

        from database import save_drill_score
        user = self.controller.get_current_user()
        if user:
            save_drill_score(user["id"], self.__class__.__name__, self.makes, self.total_shots)

        self.makeButton.config(state="disabled")
        self.missButton.config(state="disabled")

    def reset_drill(self):
        #Restart the drill if the user wishes to
        confirm = messagebox.askyesno("Reset Drill", "Are you sure you want to reset the drill? This will clear your current stats.")
        if confirm:
            self.makes = 0
            self.misses = 0
            self.update_display()
            self.makeButton.config(state="normal")
            self.missButton.config(state="normal")

    def tkraise(self, aboveThis=None):
        #Can be used to load saved progress
        super().tkraise(aboveThis)
        self.reset_drill()
