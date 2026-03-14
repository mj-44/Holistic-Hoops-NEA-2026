#setting the colours for the application and button settings
import tkinter as tk
from tkinter import font
from thememanager import theme_manager

#the base level colour scheme for the application
BG_COLOUR = "#000000"
ACCENT_COLOUR = "#D4A017"
TEXT_COLOUR = "#FFFFFF"
HOVER_COLOUR = "#FFA500" #changes shade of orange when hovering over a button

#Creating a button style that can be reused throughout the application, with hover effects and can adapt to different themes
class ButtonStyle(tk.Button):
    def __init__(self, parent, text, command, **kwargs):
        super().__init__(
            parent,
            text=text,
            command=command,
            background=theme_manager.colours["accent"],
            foreground=theme_manager.colours["text"],
            font=("Coda", 14, "bold"),
            relief="flat",
            cursor="hand2",
            padx=20,
            pady=10,
            **kwargs
        )
        theme_manager.register(lambda: self.configure(
            background=theme_manager.colours["accent"],
            foreground=theme_manager.colours["text"]
        ))
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def on_enter(self, e):
        self["background"] = theme_manager.colours["hover"]

    def on_leave(self, e):
        self["background"] = theme_manager.colours["accent"]

#Creating a styled entry widget that can be reused, with placeholder functionality when no text is present in the entry and theme adaptability
class StyledEntry(tk.Entry):
    def __init__(self, parent, placeholder="", show="", **kwargs):
        super().__init__(
            parent,
            background=theme_manager.colours["entry_background"],
            foreground=theme_manager.colours["text"],
            font=("Coda", 12),
            insertbackground=theme_manager.colours["text"],
            relief="solid",
            borderwidth=2,
            highlightthickness=2,
            highlightcolor=theme_manager.colours["accent"],
            highlightbackground=theme_manager.colours["entry_border"],
            show=show,
            **kwargs
        )
        theme_manager.register(lambda: self.configure(
            background=theme_manager.colours["entry_background"],
            foreground=theme_manager.colours["text"],
            insertbackground=theme_manager.colours["text"],
            highlightcolor=theme_manager.colours["accent"],
            highlightbackground=theme_manager.colours["entry_border"],
        ))

        self.placeholder = placeholder
        self.placeholder_active = False

        #add placeholder if provided
        if placeholder:
            self.insert(0, placeholder)
            self.placeholder_active = True
            self.config(foreground="#666666")

            #Bind focus for placeholders
            self.bind("<FocusIn>", self.on_focus_in)
            self.bind("<FocusOut>", self.on_focus_out)
    
    def on_focus_in(self, e):
        #Remove placeholder when user clicks on entry
        if self.placeholder_active:
            self.delete(0, tk.END)
            self.config(foreground = TEXT_COLOUR)
            self.placeholder_active = False

    def on_focus_out(self, e):
        #If the entry is empty, restore the placeholder
        if not self.get():
            self.insert(0, self.placeholder)
            self.config(foreground = "#666666")
            self.placeholder_active = True

    def get_value(self):
        #Get the value or return empty string if there is a placeholder
        if self.placeholder_active:
            return ""
        return self.get()
    
#Create a label style for titles and headers that can be reused throughout the program, they are also adaptive to theme changes
class StyledLabel(tk.Label):
    def __init__(self, parent, text, size=12, bold=False, **kwargs):
        font_tuple = ("Coda", size, "bold" if bold else "normal")
        super().__init__(
            parent,
            text=text,
            background=theme_manager.colours["background"],
            foreground=theme_manager.colours["text"],
            font=font_tuple,
            **kwargs
        )
        theme_manager.register(lambda: self.configure(
            background=theme_manager.colours["background"],
            foreground=theme_manager.colours["text"]
        ))

#Function which creates a frame with background colour corresponding to the current theme and sets it to the correct colour in response to a theme change
def create_frame(parent):
    frame = tk.Frame(parent, background=theme_manager.colours["background"])
    theme_manager.register(lambda: frame.configure(background=theme_manager.colours["background"]))
    return frame

#Displays whether the user was successful or not with colours to also indicate the outcome of their actions
def show_message(parent, message, is_error = True):
    colour = "#FF4444" if is_error else "#44FF44"
    label = tk.Label(
        parent,
        text = message,
        background = BG_COLOUR,
        foreground = colour,
        font = ("Coda", 10)
    )
    return label
