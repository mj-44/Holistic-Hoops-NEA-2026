import tkinter as tk
from colourscheme import ButtonStyle, StyledLabel, BG_COLOUR, ACCENT_COLOUR, TEXT_COLOUR, create_frame
from database import get_high_scores_by_username
from thememanager import theme_manager

#Drill display names in a consistent order, grouped by category
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

# Badge definitions: (display text, colour, minimum percentage threshold)
BADGES = [
    ("🏆 Hall of Fame", "#8C44FF", 90),  # purple
    ("🥇 Gold",         "#FFD900", 75),  # gold
    ("🥈 Silver",       "#9C9C9C", 50),  # silver
    ("🥉 Bronze",       "#CD7F32", 25),  # bronze
    ("❌ None",         "#FF0000",  0),  # red
]

def get_badge(percentage):
    #Returns (badge_text, colour) for a given percentage
    for label, colour, threshold in BADGES:
        if percentage >= threshold:
            return label, colour
    return BADGES[-1][0], BADGES[-1][1]


class TrackerMenu(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG_COLOUR)
        self.controller = controller
        self.current_user = None
        theme_manager.register(lambda: self.configure(bg=theme_manager.colours["bg"]))

        #Scrollable canvas so all drills fit
        canvas = tk.Canvas(self, bg=BG_COLOUR, highlightthickness=0)
        scrollbar = tk.Scrollbar(self, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        self.inner = tk.Frame(canvas, bg=BG_COLOUR)
        self.inner_window = canvas.create_window((360, 0), window=self.inner, anchor="n")

        self.inner.bind("<Configure>", lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        ))
        canvas.bind("<Configure>", lambda e: canvas.itemconfig(
            self.inner_window, width=e.width
        ))
        canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(-1*(e.delta//120), "units"))

        #Page title
        StyledLabel(self.inner, text="My High Scores", size=21, bold=True).pack(pady=(30, 5))

        self.subtitleLabel = StyledLabel(self.inner, text="Log in to see your scores", size=12, bold=False)
        self.subtitleLabel.pack(pady=(0, 10))

        #Badge Key
        key_outer = tk.Frame(self.inner, bg="#111111")
        key_outer.pack(fill="x", padx=30, pady=(0, 15))

        tk.Label(key_outer, text="Badge Key", bg="#111111", fg="#888888",
                 font=("Coda", 10, "bold")).pack(pady=(8, 4))

        key_row = tk.Frame(key_outer, bg="#111111")
        key_row.pack(pady=(0, 8))

        for badge_label, colour, threshold in BADGES:
            badge_frame = tk.Frame(key_row, bg="#111111")
            badge_frame.pack(side="left", padx=8)

            #Coloured dot indicator
            dot = tk.Canvas(badge_frame, width=14, height=14, bg="#111111", highlightthickness=0)
            dot.pack(side="left", padx=(0, 4))
            dot.create_oval(2, 2, 12, 12, fill=colour, outline=colour)

            threshold_text = f"{threshold}%+" if threshold > 0 else "<25%"
            tk.Label(badge_frame,
                     text=f"{badge_label} ({threshold_text})",
                     bg="#111111", fg=colour,
                     font=("Coda", 9)).pack(side="left")

        #Summary bar
        summary_frame = tk.Frame(self.inner, bg="#111111", bd=0)
        summary_frame.pack(fill="x", padx=30, pady=(0, 20))

        summary_inner = tk.Frame(summary_frame, bg="#111111")
        summary_inner.pack(pady=15)

        StyledLabel(summary_inner, text="Drills Completed", size=11, bold=False).grid(row=0, column=0, padx=30)
        StyledLabel(summary_inner, text="Best Avg %", size=11, bold=False).grid(row=0, column=1, padx=30)
        StyledLabel(summary_inner, text="Total Drills", size=11, bold=False).grid(row=0, column=2, padx=30)

        self.completedLabel = tk.Label(summary_inner, text="0", bg="#111111", fg=ACCENT_COLOUR,
                                       font=("Coda", 22, "bold"))
        self.completedLabel.grid(row=1, column=0, padx=30)

        self.avgLabel = tk.Label(summary_inner, text="0.0%", bg="#111111", fg=ACCENT_COLOUR,
                                 font=("Coda", 22, "bold"))
        self.avgLabel.grid(row=1, column=1, padx=30)

        self.totalLabel = tk.Label(summary_inner, text=str(sum(len(v) for v in DRILL_CATEGORIES.values())),
                                   bg="#111111", fg=TEXT_COLOUR, font=("Coda", 22, "bold"))
        self.totalLabel.grid(row=1, column=2, padx=30)

        #Drill rows - one section per category
        self.row_labels = {}  # drill_key -> (score_label, pct_label, badge_lbl, bar_fill, total, row_bg)

        for category, drills in DRILL_CATEGORIES.items():
            #Category header
            cat_frame = tk.Frame(self.inner, bg=BG_COLOUR)
            cat_frame.pack(fill="x", padx=20, pady=(15, 5))

            tk.Label(cat_frame, text=category, bg=BG_COLOUR, fg=ACCENT_COLOUR,
                     font=("Coda", 14, "bold")).pack(side="left")

            #Divider
            tk.Frame(self.inner, bg=ACCENT_COLOUR, height=1).pack(fill="x", padx=20, pady=(0, 8))

            #Column headers
            col_frame = tk.Frame(self.inner, bg=BG_COLOUR)
            col_frame.pack(fill="x", padx=25)
            col_frame.columnconfigure(0, weight=3)
            col_frame.columnconfigure(1, weight=2)
            col_frame.columnconfigure(2, weight=2)
            col_frame.columnconfigure(3, weight=2)
            col_frame.columnconfigure(4, weight=3)

            for col, heading in enumerate(["Drill", "Score", "Percentage", "Badge", "Progress"]):
                tk.Label(col_frame, text=heading, bg=BG_COLOUR, fg="#888888",
                         font=("Coda", 10, "bold")).grid(row=0, column=col, sticky="w", padx=5)

            #One row per drill
            for i, (drill_key, display_name, total) in enumerate(drills):
                row_bg = BG_COLOUR if i % 2 == 0 else "#0d0d0d"
                row = tk.Frame(self.inner, bg=row_bg)
                row.pack(fill="x", padx=20, pady=1)
                row.columnconfigure(0, weight=3)
                row.columnconfigure(1, weight=2)
                row.columnconfigure(2, weight=2)
                row.columnconfigure(3, weight=2)
                row.columnconfigure(4, weight=3)

                #Drill name
                tk.Label(row, text=display_name, bg=row_bg, fg=TEXT_COLOUR,
                         font=("Coda", 11), anchor="w").grid(row=0, column=0, sticky="w", padx=8, pady=8)

                #Score (e.g. 42/50)
                score_label = tk.Label(row, text="–", bg=row_bg, fg="#888888",
                                       font=("Coda", 11))
                score_label.grid(row=0, column=1, padx=5, pady=8)

                #Percentage
                pct_label = tk.Label(row, text="–", bg=row_bg, fg="#888888",
                                     font=("Coda", 11))
                pct_label.grid(row=0, column=2, padx=5, pady=8)

                #Badge label
                badge_lbl = tk.Label(row, text="–", bg=row_bg, fg="#888888",
                                     font=("Coda", 10, "bold"))
                badge_lbl.grid(row=0, column=3, padx=5, pady=8)

                #Progress bar
                bar_frame = tk.Frame(row, bg=row_bg)
                bar_frame.grid(row=0, column=4, padx=8, pady=8, sticky="ew")

                bar_bg = tk.Frame(bar_frame, bg="#333333", height=12, width=140)
                bar_bg.pack_propagate(False)
                bar_bg.pack(anchor="w")

                bar_fill = tk.Frame(bar_bg, bg="#333333", height=12, width=0)
                bar_fill.place(x=0, y=0, height=12)

                self.row_labels[drill_key] = (score_label, pct_label, badge_lbl, bar_fill, total, row_bg)

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
        self.configure(bg=c["bg"])

    def set_current_user(self, username):
        self.current_user = username
        self.subtitleLabel.config(text=f"Showing high scores for: {username}")
        self.refresh_scores()

    def refresh_scores(self):
        if not self.current_user:
            return

        scores = get_high_scores_by_username(self.current_user) or {}

        completed = 0
        percentages = []

        for drill_key, (score_label, pct_label, badge_lbl, bar_fill, total, row_bg) in self.row_labels.items():
            data = scores.get(drill_key)

            if data:
                completed += 1
                pct = data["percentage"]
                percentages.append(pct)

                badge_text, badge_colour = get_badge(pct)

                score_label.config(
                    text=f"{data['makes']}/{data['total_shots']}",
                    fg=badge_colour
                )
                pct_label.config(
                    text=f"{pct}%",
                    fg=badge_colour
                )
                badge_lbl.config(
                    text=badge_text,
                    fg=badge_colour
                )

                #Progress bar fill width proportional to percentage (max 140px)
                fill_width = int((pct / 100) * 140)
                bar_fill.config(bg=badge_colour, width=fill_width)
                bar_fill.place(x=0, y=0, height=12, width=fill_width)
            else:
                score_label.config(text="–", fg="#888888")
                pct_label.config(text="–", fg="#888888")
                badge_lbl.config(text="–", fg="#888888")
                bar_fill.place(x=0, y=0, height=12, width=0)

        #Update summary bar
        self.completedLabel.config(text=str(completed))
        avg = round(sum(percentages) / len(percentages), 1) if percentages else 0.0
        self.avgLabel.config(text=f"{avg}%")

    def _score_colour(self, percentage):
        #Now delegates to get_badge() for consistency
        _, colour = get_badge(percentage)
        return colour

    def tkraise(self, aboveThis=None):
        super().tkraise(aboveThis)
        self.refresh_scores()