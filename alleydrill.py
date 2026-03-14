import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from colourscheme import ButtonStyle, StyledLabel, BG_COLOUR, ACCENT_COLOUR, TEXT_COLOUR, create_frame
from thememanager import theme_manager

#Creating the class for the alley drill
class AlleyDrill(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, background = BG_COLOUR)
        self.controller = controller
        theme_manager.register(lambda: self.configure(background=theme_manager.colours["background"]))

        #Initialise variables so that the users makes and misses can be tracked and later used for their score
        self.makes = 0
        self.misses = 0
        self.total_shots = 25
        
        #Making a container frame to centralise the content of the page
        main_frame = create_frame(self)
        main_frame.place(relx = 0.5, rely = 0.5, anchor = "center")

        #Making a title for the page to make it clear what drill they are doing
        title = StyledLabel(
            main_frame,
            text = "Alley Drill",
            size = 21,
            bold = True
        )
        title.pack(pady=(0,20))

        #Using a subtitle to give a brief description of the general task they are doing
        subtitle = StyledLabel(
            main_frame,
            text = "Drill Focused on getting by a defender in limited space!",
            size = 14,
            bold = False
        )
        subtitle.pack(pady=(0,20))

        #Loading a pre made image which gives a brief illustration of how to perform the drill.
        drillImage = Image.open("assets/alley_drill.png")

        #Resizing the image to fit within the app window while maintaining the overall aspect ratio of the app
        drillImage = drillImage.resize((500, 300), Image.Resampling.LANCZOS)

        #Convert the image into a format that can be used by Tkinter can use
        self.drillPhoto = ImageTk.PhotoImage(drillImage)

        #Displaying the image on the screen for the user to see
        imageLabel = tk.Label(main_frame, image=self.drillPhoto, background=BG_COLOUR)
        imageLabel.pack(pady=(0,20))

        #Displaying the instructions for the drill
        instructionsLabel = StyledLabel(
            main_frame,
            text = "Instructions:",
            size = 16,
            bold = True
        )
        instructionsLabel.pack(pady=(20,10))

        #Storing the steps for the drill in an array so that they can be used to be listed as instructions on the menu
        steps = [
            "1. Attacker starts from half-court with the ball with defender positioned in front.",
            "2. Red cross defends the blue player between the “alleyway” of cones",
            "3. Blue player has 10 seconds to get to the rim and try to score",
            "4. Repeat 25 times and get a score out of 25 (stops count as a miss)",
        ]

        #Iterating through the steps in the array and creating a label for each one where the text in the label
        for step in steps:
            stepLabel = StyledLabel(
                main_frame,
                text = step,
                size = 12,
                bold = False
            )
            stepLabel.pack(pady=5, padx=40, anchor="w")

        #Creating the section by using a frame to actively display the score as the user plays the drill
        scoreFrame = create_frame(main_frame)
        scoreFrame.pack(pady=(30))

        #Displaying the users current score onto the screen as a ratio of their makes against their total shots
        self.scoreLabel = StyledLabel(
            scoreFrame,
            text = f"Score: {self.makes}/{self.makes + self.misses}",
            size = 20,
            bold = True
        )
        self.scoreLabel.pack(pady=10)

        #Displaying the users amount of total shots taken
        self.progressLabel = StyledLabel(
            scoreFrame,
            text = f"Shots Taken: {self.makes + self.misses}/{self.total_shots}",
            size = 14,
            bold = False
        )
        self.progressLabel.pack(pady=5)

        #Displaying the users shooting percentage which should automatically update every shot
        self.percentageLabel = StyledLabel(
            scoreFrame,
            text = f"Shooting Percentage: 0.0%",
            size = 14,
            bold = False
        )
        self.percentageLabel.pack(pady=5)

        #Interative buttons to enable the user to inform the app of when they made a shot versus when they missed a shot
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

        #Miss or in this scenratio stop button if the defender made a stop
        self.missButton = ButtonStyle(
            buttonContainer,
            text = "MISS/STOP ✘",
            command = self.record_miss,
            width = 12
        )
        self.missButton.pack(side = "left", padx=10)

        #Button allowing the user to return to the finishing menu when they are done with the drill
        backButton = ButtonStyle(
            main_frame,
            text = "← Back",
            command = lambda: controller.show_page("FinishingMenu"),
            width = 20
        )
        backButton.pack(pady=10)
        
        #Creating a button to reset the drill
        resetButton = ButtonStyle(
            main_frame,
            text = "Reset Drill",
            command = self.reset_drill,
            width = 12
        )
        resetButton.pack(side = "left", pady=10)
        theme_manager.register(self.apply_theme)

    #Applying the theme that the user has chosen for the page automatically to this page
    def apply_theme(self):
            colour = theme_manager.colours
            self.configure(background=colour["background"])

    #Subroutine to record a made shot until they have taken the maximum amount of shots for the drill
    def record_make(self):
        if self.makes + self.misses >= self.total_shots:
            messagebox.showinfo("Drill Complete", "You have completed all 25 1v1s!")
            return
        #Increments the amount of makes from the user
        self.makes += 1
        self.update_display()
        #Increments the amount of total shots that the user has taken
        if self.makes + self.misses >= self.total_shots:
            self.drill_complete()
    #Subroutine incrementing the amount of shots the user has missed
    def record_miss(self):
        #Incrememnt the missed shots for the user
        if self.makes + self.misses >= self.total_shots:
            messagebox.showinfo("Drill Complete", "You have completed all 25 1v1s!")
            return
        #Increments the amount of total shots the user has missed
        self.misses += 1
        self.update_display()
        #Incrementing the amount of total shots the user has taken
        if self.makes + self.misses >= self.total_shots:
            self.drill_complete()

    def update_display(self):
        #Updating the score displays actively as the user plays
        self.scoreLabel.config(text = f"Score: {self.makes}/{self.makes + self.misses}")
        shots_taken = self.makes + self.misses
        self.progressLabel.config(text = f"Shots Taken: {shots_taken}/{self.total_shots}") #roads the percentage to 1 decimal place

        if shots_taken > 0:
            percentage = (self.makes / shots_taken) * 100
            self.percentageLabel.config(text = f"Shooting %: {percentage: .1f}%")
        else:
            self.percentageLabel.config(text = "Shooting %: 0.0%")

    #Notifying the user that the drill has been complete displaying their score and shooting percentage
    def drill_complete(self):
        percentage = (self.makes / self.total_shots) * 100
        
        message = f"Drill Complete!\n\nFinal Score: {self.makes}/{self.total_shots}\nShooting Percentage: {percentage: .1f}%"
        messagebox.showinfo("Drill Complete", message)
        #Saving the users score to the database
        from database import save_drill_score
        user = self.controller.get_current_user()
        if user:
            save_drill_score(user["id"], self.__class__.__name__, self.makes, self.total_shots)
        #Disabling the buttons so the user can no longer interact with them once they have completed the drill to avoid errors
        self.makeButton.config(state="disabled")
        self.missButton.config(state="disabled")

    def reset_drill(self):
        #Restart the drill if the user wishes to repeat it
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
