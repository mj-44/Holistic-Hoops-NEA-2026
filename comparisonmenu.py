import tkinter as tk
from colourscheme import ButtonStyle, StyledLabel, StyledEntry, BG_COLOUR, TEXT_COLOUR, ACCENT_COLOUR, create_frame, show_message
from database import get_high_scores_by_username, get_user
from thememanager import theme_manager

#All drill names in a consistent display order
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

#Friendly display names matching the drill class names above
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

class ComparisonMenu(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, background=BG_COLOUR)
        self.controller = controller
        self.current_user = None      #set by controller after login
        self.message_label = None
        theme_manager.register(lambda: self.configure(background=theme_manager.colours["background"]))

        #Scrollable canvas setup so the comparison table fits on screen
        canvas = tk.Canvas(self, background=BG_COLOUR, highlightthickness=0)
        scrollbar = tk.Scrollbar(self, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        #Inner frame inside the canvas
        self.inner = tk.Frame(canvas, background=BG_COLOUR)
        self.inner_window = canvas.create_window((360, 0), window=self.inner, anchor="n")

        self.inner.bind("<Configure>", lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        ))
        canvas.bind("<Configure>", lambda e: canvas.itemconfig(
            self.inner_window, width=e.width
        ))

        #Mousewheel scroll
        canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(-1*(e.delta//120), "units"))

        #Page title
        StyledLabel(self.inner, text="Player Comparison", size=21, bold=True).pack(pady=(30, 10))

        #Search section
        search_frame = create_frame(self.inner)
        search_frame.pack(pady=10)

        StyledLabel(search_frame, text="Search opponent username:", size=12).pack(side="left", padx=(0, 10))

        self.searchEntry = StyledEntry(search_frame, width=20)
        self.searchEntry.pack(side="left", padx=(0, 10))

        ButtonStyle(
            search_frame,
            text="Compare",
            command=self.run_comparison,
            width=10
        ).pack(side="left")

        #Column headers
        header_frame = create_frame(self.inner)
        header_frame.pack(fill="x", padx=20, pady=(20, 5))
        header_frame.columnconfigure(0, weight=2)
        header_frame.columnconfigure(1, weight=1)
        header_frame.columnconfigure(2, weight=1)

        StyledLabel(header_frame, text="Drill", size=12, bold=True).grid(row=0, column=0, sticky="w")
        self.you_header = StyledLabel(header_frame, text="You", size=12, bold=True)
        self.you_header.grid(row=0, column=1)
        self.them_header = StyledLabel(header_frame, text="Opponent", size=12, bold=True)
        self.them_header.grid(row=0, column=2)

        #Divider
        tk.Frame(self.inner, background=ACCENT_COLOUR, height=2).pack(fill="x", padx=20, pady=5)

        #Drill rows container
        self.rows_frame = create_frame(self.inner)
        self.rows_frame.pack(fill="x", padx=20)

        #Build one row per drill (initially blank)
        self.row_widgets = {}
        for i, drill in enumerate(ALL_DRILLS):
            row_background = BG_COLOUR if i % 2 == 0 else "#0d0d0d"
            row = tk.Frame(self.rows_frame, background=row_background)
            row.pack(fill="x", pady=1)
            row.columnconfigure(0, weight=2)
            row.columnconfigure(1, weight=1)
            row.columnconfigure(2, weight=1)

            name_label = tk.Label(
                row, text=DRILL_DISPLAY_NAMES[drill],
                background=row_background, foreground=TEXT_COLOUR,
                font=("Coda", 11), anchor="w"
            )
            name_label.grid(row=0, column=0, sticky="w", padx=5, pady=6)

            you_label = tk.Label(
                row, text="-",
                background=row_background, foreground=TEXT_COLOUR,
                font=("Coda", 11)
            )
            you_label.grid(row=0, column=1, pady=6)

            them_label = tk.Label(
                row, text="-",
                background=row_background, foreground=TEXT_COLOUR,
                font=("Coda", 11)
            )
            them_label.grid(row=0, column=2, pady=6)

            self.row_widgets[drill] = (you_label, them_label, row_background)

        #Back button
        ButtonStyle(
            self.inner,
            text="← Back to Main Menu",
            command=lambda: controller.show_page("MainMenu"),
            width=20
        ).pack(pady=30)

        theme_manager.register(self.apply_theme)

    def apply_theme(self):
        c = theme_manager.colours
        self.configure(background=c["background"])

    def set_current_user(self, username):
        #Called by the controller after login so the page knows who is logged in
        self.current_user = username
        self.you_header.config(text=username)
        self.refresh_my_scores()

    def refresh_my_scores(self):
        #Re-fetch my scores from the DB and redisplay (opponent column stays as-is)
        if not self.current_user:
            return
        self.my_scores = get_high_scores_by_username(self.current_user) or {}
        self._redraw_rows(self.my_scores, getattr(self, "opponent_scores", {}))

    def run_comparison(self):
        #Clear any old messages
        if self.message_label:
            self.message_label.destroy()

        opponent_username = self.searchEntry.get_value().strip()

        if not opponent_username:
            self.message_label = show_message(self.inner, "Please enter a username to search")
            self.message_label.pack()
            return

        if opponent_username == self.current_user:
            self.message_label = show_message(self.inner, "You can't compare yourself to yourself!")
            self.message_label.pack()
            return

        #Look up the opponent
        opponent_scores = get_high_scores_by_username(opponent_username)

        if opponent_scores is None:
            self.message_label = show_message(self.inner, f"User '{opponent_username}' not found")
            self.message_label.pack()
            return

        self.opponent_scores = opponent_scores
        self.them_header.config(text=opponent_username)

        self.my_scores = get_high_scores_by_username(self.current_user) or {}
        self._redraw_rows(self.my_scores, self.opponent_scores)

    def _redraw_rows(self, my_scores, opponent_scores):
        #Update every drill row with scores and apply colour coding
        for drill in ALL_DRILLS:
            you_label, them_label, row_background = self.row_widgets[drill]

            my_data = my_scores.get(drill)
            opp_data = opponent_scores.get(drill)

            my_text = f"{my_data['makes']}/{my_data['total_shots']} ({my_data['percentage']}%)" if my_data else "No score"
            opp_text = f"{opp_data['makes']}/{opp_data['total_shots']} ({opp_data['percentage']}%)" if opp_data else "No score"

            #Determine colours
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
                #One or both have no score - neutral white
                my_colour = TEXT_COLOUR
                opp_colour = TEXT_COLOUR

            you_label.config(text=my_text, foreground=my_colour)
            them_label.config(text=opp_text, foreground=opp_colour)

    def tkraise(self, aboveThis=None):
        super().tkraise(aboveThis)
        #Refresh my scores every time we land on this page (in case new drills completed)
        self.refresh_my_scores()