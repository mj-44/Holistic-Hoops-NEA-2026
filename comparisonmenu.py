import tkinter as tk
from colourscheme import ButtonStyle, StyledLabel, StyledEntry, BG_COLOUR, TEXT_COLOUR, ACCENT_COLOUR, create_frame, show_message
from database import get_high_scores_by_username, get_user
from thememanager import theme_manager

#Listing all the drill names and storing them in a constant so that they can be used throughout the page
ALL_DRILLS = [
    "AlleyDrill",
    "AroundTheWorld",
    "BackPedalFinishing",
    "BackPedalFinishingPF",
    "ConeTouchFinishing",
    "DribblePullUpDrill",
    "DrivingLayDrill",
    "FresnoAttack",
    "FullcourtWeaveDrill",
    "OffBalancePullUps",
    "RangeRumble",
    "SpinMoveDrill",
]

#Friendly display names matching the drill class names that were listed prior above
DRILL_DISPLAY_NAMES = {
    "AlleyDrill": "Alley Drill",
    "AroundTheWorld": "Around The World",
    "BackPedalFinishing": "Back Pedal Finishing",
    "BackPedalFinishingPF": "Back Pedal Finishing (PF)",
    "ConeTouchFinishing": "Cone Touch Finishing",
    "DribblePullUpDrill": "Dribble Pull-Up",
    "DrivingLayDrill": "Driving Lay Drill",
    "FresnoAttack": "Fresno Attack",
    "FullcourtWeaveDrill": "Fullcourt Weave",
    "OffBalancePullUps": "Off-Balance Pull-Ups",
    "RangeRumble": "Range Rumble",
    "SpinMoveDrill": "Spin Move Drill",
}

#Creating the class for the comparison menu
class ComparisonMenu(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, background=BG_COLOUR)
        self.controller = controller
        self.current_user = None      #set by controller after login
        self.message_label = None
        theme_manager.register(lambda: self.configure(background=theme_manager.colours["background"]))

        #Scrollable canvas setup so the comparison table fits on screen and the resolution of the page can remain fixed
        canvas = tk.Canvas(self, background=BG_COLOUR, highlightthickness=0)
        scrollbar = tk.Scrollbar(self, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        #Creating an inner frame inside the canvas
        self.inner = tk.Frame(canvas, background=BG_COLOUR)
        self.inner_window = canvas.create_window((360, 0), window=self.inner, anchor="n")

        self.inner.bind("<Configure>", lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        ))
        canvas.bind("<Configure>", lambda e: canvas.itemconfig(
            self.inner_window, width=e.width
        ))

        #Setting the mousewheel as a valid input allowing the user to scroll and go up and down the page
        canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(-1*(e.delta//120), "units"))

        #Creating a clear title page for this menu of the application "Player Comparison"
        StyledLabel(self.inner, text="Player Comparison", size=21, bold=True).pack(pady=(30, 10))

        #Creating a section where the user can search for another user to compare themselves to
        search_frame = create_frame(self.inner)
        search_frame.pack(pady=10)

        #Creating a label to make it clear that this is where they should be searching for the username of the person
        #they wish to compare themselves to
        StyledLabel(search_frame, text="Search opponent username:", size=12).pack(side="left", padx=(0, 10))

        self.searchEntry = StyledEntry(search_frame, width=20)
        self.searchEntry.pack(side="left", padx=(0, 10))

        #Creating a button which upon being clicked searches for the user and if found, returns their scores and compares
        #them against each other
        ButtonStyle(
            search_frame,
            text="Compare",
            command=self.run_comparison,
            width=10
        ).pack(side="left")

        #Creating column headers for the menu to make the data on the page make more sense and identify whos scores are whose
        header_frame = create_frame(self.inner)
        header_frame.pack(fill="x", padx=20, pady=(20, 5))
        header_frame.columnconfigure(0, weight=2)
        header_frame.columnconfigure(1, weight=1)
        header_frame.columnconfigure(2, weight=1)
        
        #Created labels to make clear what each column is for
        #One displays the drill name, another the score the user got on that drill, the other the score that the opponent got
        StyledLabel(header_frame, text="Drill", size=12, bold=True).grid(row=0, column=0, sticky="w")
        self.you_header = StyledLabel(header_frame, text="You", size=12, bold=True)
        self.you_header.grid(row=0, column=1)
        self.them_header = StyledLabel(header_frame, text="Opponent", size=12, bold=True)
        self.them_header.grid(row=0, column=2)

        #Creating a divider for a neater format on the page
        tk.Frame(self.inner, background=ACCENT_COLOUR, height=2).pack(fill="x", padx=20, pady=5)

        #Creating a container for each row representing each drill
        self.rows_frame = create_frame(self.inner)
        self.rows_frame.pack(fill="x", padx=20)

        #Making the rows for the drills
        self.row_widgets = {}
        for i, drill in enumerate(ALL_DRILLS):
            row_background = BG_COLOUR if i % 2 == 0 else "#0d0d0d"
            row = tk.Frame(self.rows_frame, background=row_background)
            row.pack(fill="x", pady=1)
            row.columnconfigure(0, weight=2)
            row.columnconfigure(1, weight=1)
            row.columnconfigure(2, weight=1)

            #Creating a label for the name of the drill when being stored in the row
            name_label = tk.Label(
                row, text=DRILL_DISPLAY_NAMES[drill],
                background=row_background, foreground=TEXT_COLOUR,
                font=("Coda", 11), anchor="w"
            )
            name_label.grid(row=0, column=0, sticky="w", padx=5, pady=6)

            #The score that the user got on that particular drill
            yourscore_label = tk.Label(
                row, text="-",
                background=row_background, foreground=TEXT_COLOUR,
                font=("Coda", 11)
            )
            yourscore_label.grid(row=0, column=1, pady=6)

            #The score that the opponent got on that same drill
            oppscore_label = tk.Label(
                row, text="-",
                background=row_background, foreground=TEXT_COLOUR,
                font=("Coda", 11)
            )
            oppscore_label.grid(row=0, column=2, pady=6)

            self.row_widgets[drill] = (yourscore_label, oppscore_label, row_background)

        #Button that allows the user to return to the homepage when they are done using this menu
        ButtonStyle(
            self.inner,
            text="← Back to Main Menu",
            command=lambda: controller.show_page("MainMenu"),
            width=20
        ).pack(pady=30)

        theme_manager.register(self.apply_theme)
    
    #Automatically applies the theme that the user has chosen to use on the application to this particular page
    def apply_theme(self):
        colour = theme_manager.colours
        self.configure(background=colour["background"])

    def set_current_user(self, username):
        #Identifies the user who is logged in and sets them as the current user
        self.current_user = username
        self.you_header.config(text=username)
        self.refresh_my_scores()

    def refresh_my_scores(self):
        #Refetch the users scores from the database and redisplay them in the case that the page hasn't got updated scores
        if not self.current_user:
            return
        self.my_scores = get_high_scores_by_username(self.current_user) or {}
        self._redraw_rows(self.my_scores, getattr(self, "opponent_scores", {}))

    #Subroutine for comparing the two scores together
    def run_comparison(self):
        #Clears any old messages in case there were any
        if self.message_label:
            self.message_label.destroy()

        #fetches the opponents username from the database
        opponent_username = self.searchEntry.get_value().strip()

        #Returns an error message if the opponent username field is left blank
        if not opponent_username:
            self.message_label = show_message(self.inner, "Please enter a username to search")
            self.message_label.pack()
            return

        #Stops the user from their comparing their own scores to themself
        if opponent_username == self.current_user:
            self.message_label = show_message(self.inner, "You can't compare yourself to yourself!")
            self.message_label.pack()
            return

        #Searches up the opponent in the database
        opponent_scores = get_high_scores_by_username(opponent_username)

        #Returns an error message if the user being searched for isn't in the database
        if opponent_scores is None:
            self.message_label = show_message(self.inner, f"User '{opponent_username}' not found")
            self.message_label.pack()
            return

        #If the scores are found, it then extracts their scores
        self.opponent_scores = opponent_scores
        self.them_header.config(text=opponent_username)

        #fetches the users scores from the database
        self.my_scores = get_high_scores_by_username(self.current_user) or {}
        self._redraw_rows(self.my_scores, self.opponent_scores)

    #Subroutine which once the scores have been obtained, comparisons can be made and thus the rows can be updated
    def _redraw_rows(self, my_scores, opponent_scores):
        for drill in ALL_DRILLS:
            you_label, them_label, row_background = self.row_widgets[drill]

            my_data = my_scores.get(drill)
            opp_data = opponent_scores.get(drill)

            my_text = f"{my_data['makes']}/{my_data['total_shots']} ({my_data['percentage']}%)" if my_data else "No score"
            opp_text = f"{opp_data['makes']}/{opp_data['total_shots']} ({opp_data['percentage']}%)" if opp_data else "No score"

            #Attributing colours to each of the user score for each drill to show who is better at each drill
            if my_data and opp_data:
                if my_data["makes"] > opp_data["makes"]:
                    my_colour = "#44FF44"   #green - I'm winning
                    opp_colour = "#FF4444"  #red - opponent losing
                elif opp_data["makes"] > my_data["makes"]:
                    my_colour = "#FF4444"
                    opp_colour = "#44FF44"
                else:
                    my_colour = TEXT_COLOUR   #white - tied
                    opp_colour = TEXT_COLOUR
            else:
                #If one or both scores are empty, or they have the same score then appear white to give a neutral colour
                my_colour = TEXT_COLOUR
                opp_colour = TEXT_COLOUR

            you_label.config(text=my_text, foreground=my_colour)
            them_label.config(text=opp_text, foreground=opp_colour)

    def tkraise(self, aboveThis=None):
        super().tkraise(aboveThis)
        #Refresh my scores every time we land on this page (in case new drills completed)
        self.refresh_my_scores()
