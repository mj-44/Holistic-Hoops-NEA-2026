import tkinter as tk
from colourscheme import ButtonStyle, StyledLabel, BG_COLOUR, ACCENT_COLOUR, TEXT_COLOUR, create_frame
from database import get_high_scores_by_username
from thememanager import theme_manager

#Storing the drill names in a constant, grouped by category so that they can be grouped like this when
#their scores are being displayed to the user
DRILL_CATEGORIES = {
    "🎯 Shooting": [
        ("AroundTheWorld",      "Around The World",         50),
        ("DribblePullUpDrill",  "Dribble Pull-Up",          50),
        ("RangeRumble",         "Range Rumble",             50),
    ],
    "🏆 Finishing": [
        ("AlleyDrill",          "Alley Drill",              25),
        ("ConeTouchFinishing",  "Cone Touch Finishing",     25),
        ("FresnoAttack",        "Fresno Attack",            50),
    ],
    "👟 Footwork": [
        ("BackPedalFinishing",  "Back Pedal Finishing",     50),
        ("BackPedalFinishingPF","Back Pedal Finishing (PF)",50),
        ("OffBalancePullUps",   "Off-Balance Pull-Ups",     50),
    ],
    "🏀 Dribbling": [
        ("FullcourtWeaveDrill", "Fullcourt Weave",          25),
        ("SpinMoveDrill",       "Spin Move Drill",          50),
        ("DrivingLayDrill",     "Driving Lay Drill",        50),
    ],
}

#Storing the badges and the threshold percentage needed on each task to achieve each badge. The scores were chosen at random
#but the the badge names were taken from my design
BADGES = [
    ("🏆 Hall of Fame", "#8C44FF", 90),  #hall of fame badge (highest tier)
    ("🥇 Gold",         "#FFD900", 75),  #gold badge
    ("🥈 Silver",       "#9C9C9C", 50),  #silver badge
    ("🥉 Bronze",       "#CD7F32", 25),  #bronze badge
    ("❌ None",         "#FF0000",  0),  #red badge for scores unworthy of one (lowest tier)
]

#Creating a subroutine to get the badge that the user has in a certain task. It returns the badge they got and the colour
#So it can appear differently on the screen for the user.
def get_badge(percentage):
    for label, colour, threshold in BADGES:
        if percentage >= threshold:
            return label, colour
    return BADGES[-1][0], BADGES[-1][1]

#Creating the class for the tracker menu itself to be used in the application
class TrackerMenu(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, background=BG_COLOUR)
        self.controller = controller
        self.current_user = None
        theme_manager.register(lambda: self.configure(background=theme_manager.colours["background"]))

        #As the page is likely to be long, I have added the ability for a scrollable canvas so that the user can access all the
        #data on the page while keeping the resolution of the application fixed
        canvas = tk.Canvas(self, background = BG_COLOUR, highlightthickness = 0)
        scrollbar = tk.Scrollbar(self, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand = scrollbar.set)
        scrollbar.pack(side = "right", fill = "y")
        canvas.pack(side = "left", fill = "both", expand = True)

        self.inner = tk.Frame(canvas, background =BG_COLOUR)
        self.inner_window = canvas.create_window((360, 0), window=self.inner, anchor="n")

        #defining the scroll region and enable the user to scroll up and down the page through their scroll wheel
        self.inner.bind("<Configure>", lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        ))
        canvas.bind("<Configure>", lambda e: canvas.itemconfig(
            self.inner_window, width=e.width
        ))
        canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(-1*(e.delta//120), "units"))

        #The title for the menu
        StyledLabel(self.inner, text="My High Scores", size=21, bold=True).pack(pady=(30, 5))

        #Subtitle for the page giving a brief description of what the page can be used for
        self.subtitleLabel = StyledLabel(self.inner, text="Log in to see your scores", size=12, bold=False)
        self.subtitleLabel.pack(pady=(0, 10))

        #Creating a clear key for the badges so the user knows what they need in order to jump to the next badge level
        key_outer = tk.Frame(self.inner, background="#111111")
        key_outer.pack(fill="x", padx=30, pady=(0, 15))

        tk.Label(key_outer, text="Badge Key", background="#111111", foreground="#888888",
                 font=("Coda", 10, "bold")).pack(pady=(8, 4))

        key_row = tk.Frame(key_outer, background="#111111")
        key_row.pack(pady=(0, 8))

        for badge_label, colour, threshold in BADGES:
            badge_frame = tk.Frame(key_row, background="#111111")
            badge_frame.pack(side="left", padx=8)

            #Using a coloured dot to indicate the badge colour to the user
            dot = tk.Canvas(badge_frame, width=14, height=14, background="#111111", highlightthickness=0)
            dot.pack(side="left", padx=(0, 4))
            dot.create_oval(2, 2, 12, 12, fill=colour, outline=colour)

            threshold_text = f"{threshold}%+" if threshold > 0 else "<25%"
            tk.Label(badge_frame,
                     text=f"{badge_label} ({threshold_text})",
                     background="#111111", foreground=colour,
                     font=("Coda", 9)).pack(side="left")

        #Creating a bar giving the user a summary
        summary_frame = tk.Frame(self.inner, background="#111111", bd=0)
        summary_frame.pack(fill="x", padx=30, pady=(0, 20))

        summary_inner = tk.Frame(summary_frame, background="#111111")
        summary_inner.pack(pady=15)

        StyledLabel(summary_inner, text="Drills Completed", size=11, bold=False).grid(row=0, column=0, padx=30)
        
        StyledLabel(summary_inner, text="Best Avg %", size=11, bold=False).grid(row=0, column=1, padx=30)
        
        StyledLabel(summary_inner, text="Total Drills", size=11, bold=False).grid(row=0, column=2, padx=30)

        #Label here to show the completition of a task
        self.completedLabel = tk.Label(summary_inner, text="0", background="#111111", foreground=ACCENT_COLOUR,
                                       font=("Coda", 22, "bold"))
        self.completedLabel.grid(row=1, column=0, padx=30)

        #Label to show the users percentage (best average) in a drill
        self.avgLabel = tk.Label(summary_inner, text="0.0%", background="#111111", foreground=ACCENT_COLOUR,
                                 font=("Coda", 22, "bold"))
        self.avgLabel.grid(row=1, column=1, padx=30)

        #Label to show the users best total score on that
        self.totalLabel = tk.Label(summary_inner, text=str(sum(len(v) for v in DRILL_CATEGORIES.values())),
                                   background="#111111", foreground=TEXT_COLOUR, font=("Coda", 22, "bold"))
        self.totalLabel.grid(row=1, column=2, padx=30)

        #Creating the drill rows. For formatting purposes it will be best to do one drill per row
        self.row_labels = {}  #creating the labels for each row (score, percentage, badge, progress bar, and total)

        for category, drills in DRILL_CATEGORIES.items():
            #Creating the header for each category
            category_frame = tk.Frame(self.inner, background=BG_COLOUR)
            category_frame.pack(fill="x", padx=20, pady=(15, 5))

            tk.Label(category_frame, text=category, background=BG_COLOUR, foreground=ACCENT_COLOUR,
                     font=("Coda", 14, "bold")).pack(side="left")

            #Adding a divider to make the format more appealing
            tk.Frame(self.inner, background=ACCENT_COLOUR, height=1).pack(fill="x", padx=20, pady=(0, 8))

            #Creating the column headers for the menu for each different category to be displayed
            column_frame = tk.Frame(self.inner, background=BG_COLOUR)
            column_frame.pack(fill="x", padx=25)
            column_frame.columnconfigure(0, weight=3)
            column_frame.columnconfigure(1, weight=2)
            column_frame.columnconfigure(2, weight=2)
            column_frame.columnconfigure(3, weight=2)
            column_frame.columnconfigure(4, weight=3)

            for column, heading in enumerate(["Drill", "Score", "Percentage", "Badge", "Progress"]):
                tk.Label(column_frame, text=heading, background=BG_COLOUR, foreground="#888888",
                         font=("Coda", 10, "bold")).grid(row=0, column=column, sticky="w", padx=5)

            #Displaying each drill on the menu row by row to maintain an appealing interface
            for i, (drill_key, display_name, total) in enumerate(drills):
                row_background = BG_COLOUR if i % 2 == 0 else "#0d0d0d"
                row = tk.Frame(self.inner, background=row_background)
                row.pack(fill="x", padx=20, pady=1)
                row.columnconfigure(0, weight=3)
                row.columnconfigure(1, weight=2)
                row.columnconfigure(2, weight=2)
                row.columnconfigure(3, weight=2)
                row.columnconfigure(4, weight=3)

                #Displaying the name of the drill
                tk.Label(row, text=display_name, background=row_background, foreground=TEXT_COLOUR,
                         font=("Coda", 11), anchor="w").grid(row=0, column=0, sticky="w", padx=8, pady=8)

                #Showing the best score that the user got on that specific drill
                score_label = tk.Label(row, text="–", background=row_background, foreground="#888888",
                                       font=("Coda", 11))
                score_label.grid(row=0, column=1, padx=5, pady=8)

                #Displaying their percentage of their best score attempt on the drill
                percentage_label = tk.Label(row, text="–", background=row_background, foreground="#888888",
                                     font=("Coda", 11))
                percentage_label.grid(row=0, column=2, padx=5, pady=8)

                #Showing the badge that user currently has on the drill
                badge_label = tk.Label(row, text="–", background=row_background, foreground="#888888",
                                     font=("Coda", 10, "bold"))
                badge_label.grid(row=0, column=3, padx=5, pady=8)

                #Showing a progress bar for the user's score on that drill (thought it would be an appealing feature)
                bar_frame = tk.Frame(row, background=row_background)
                bar_frame.grid(row=0, column=4, padx=8, pady=8, sticky="ew")

                bar_background = tk.Frame(bar_frame, background="#333333", height=12, width=140)
                bar_background.pack_propagate(False)
                bar_background.pack(anchor="w")

                bar_fill = tk.Frame(bar_background, background="#333333", height=12, width=0)
                bar_fill.place(x=0, y=0, height=12)

                self.row_labels[drill_key] = (score_label, percentage_label, badge_label, bar_fill, total, row_background)

        #Button allowing the user to return to the main menu
        ButtonStyle(
            self.inner,
            text="← Back to Main Menu",
            command=lambda: controller.show_page("MainMenu"),
            width=20
        ).pack(pady=30)

        theme_manager.register(self.apply_theme)

    #Automatically applying the theme that the user has enabled (light or dark mode) onto the page
    def apply_theme(self):
        colour = theme_manager.colours
        self.configure(background=colour["background"])

    #Identifying the user they are showing the high scores of which should be the person who is logged into the account
    def set_current_user(self, username):
        self.current_user = username
        self.subtitleLabel.config(text=f"Showing high scores for: {username}")
        self.refresh_scores()

    #gets the scores of the user and puts them in the format that they are to be displayed in on the page
    def refresh_scores(self):
        if not self.current_user:
            return

        scores = get_high_scores_by_username(self.current_user) or {}

        completed = 0
        percentages = []

        for drill_key, (score_label, percentage_label, badge_label, bar_fill, total, row_background) in self.row_labels.items():
            data = scores.get(drill_key)

            if data:
                completed += 1
                percentage = data["percentage"]
                percentages.append(percentage)

                badge_text, badge_colour = get_badge(percentage)

                #Displaying the score percentage and badge in the colour of the badge that they obtained on that drill
                score_label.config(
                    text=f"{data['makes']}/{data['total_shots']}",
                    foreground=badge_colour
                )
                percentage_label.config(
                    text=f"{percentage}%",
                    foreground=badge_colour
                )
                badge_label.config(
                    text=badge_text,
                    foreground=badge_colour
                )

                #Progress bar calculated to fit in proportion to the size of the bar
                fill_width = int((percentage / 100) * 140)
                bar_fill.config(background=badge_colour, width=fill_width)
                bar_fill.place(x=0, y=0, height=12, width=fill_width)
            else:
                score_label.config(text="–", foreground="#888888")
                percentage_label.config(text="–", foreground="#888888")
                badge_label.config(text="–", foreground="#888888")
                bar_fill.place(x=0, y=0, height=12, width=0)

        #Updates summary bar
        self.completedLabel.config(text=str(completed))
        avg = round(sum(percentages) / len(percentages), 1) if percentages else 0.0
        self.avgLabel.config(text=f"{avg}%")

    #Getting the colour of the badge for the percentage the user got on a task
    def _score_colour(self, percentage):
        _, colour = get_badge(percentage)
        return colour
    
    #Refreshes the screen upon the user entering the page so the contents of the page is up to date
    def tkraise(self, aboveThis=None):
        super().tkraise(aboveThis)
        self.refresh_scores()
