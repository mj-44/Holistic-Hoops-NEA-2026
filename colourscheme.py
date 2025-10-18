#setting the colours for the application and button settings
import tkinter as tk
from tkinter import font

#colour scheme
BG_COLOUR = "#000000"
ACCENT_COLOUR = "#D4A017"
TEXT_COLOUR = "#FFFFFF"
HOVER_COLOUR = "#FFA500" #changes shade of orange when hovering over a button

class ButtonStyle(tk.Button):
    #Creating app colour scheme with the hover effects
    def __init__(self, parent, text, command, **kwargs): #keyword arguments to accept any number of keyword arguments
        super().__init__(
            parent,
            text = text,
            command = command,
            bg = ACCENT_COLOUR,
            fg = TEXT_COLOUR,
            font = ("Coda", 14, "bold"),
            relief = "flat",
            cursor = "hand2",
            padx = 20,
            pady = 10,
            **kwargs 
    )
        
        #hover effects
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def on_enter(self, e):
        #Change colour when mouse hovers over the button
        self["bg"] = HOVER_COLOUR

    def on_leave(self, e):
        #Return to normal colour when mouse is no longer hovering
        self["bg"] = ACCENT_COLOUR

class StyledEntry(tk.Entry):
    #Custom text entry matching app colour scheme
    def __init__(self, parent, placeholder="", show = "", **kwargs):
        super().__init__(
            parent,
            bg="#1a1a1a",
            fg=TEXT_COLOUR,
            font=("Coda", 12),
            insertbackground=TEXT_COLOUR,
            relief="solid",
            bd=2,
            highlightthickness=2,
            highlightcolor=ACCENT_COLOUR,
            highlightbackground="#333333",
            show=show,
            **kwargs
        )
        

        self.placeholder = placeholder
        self.placeholder_active = False

        #add placeholder if provided
        if placeholder:
            self.insert(0, placeholder)
            self.placeholder_active = True
            self.config(fg="#666666")

            #Bind focus for placeholders
            self.bind("<FocusIn>", self.on_focus_in)
            self.bind("<FocusOut>", self.on_focus_out)

    def on_focus_in(self, e):
        #Remove placeholder when user clicks on entry
        if self.placeholder_active:
            self.delete(0, tk.END)
            self.config(fg = TEXT_COLOUR)
            self.placeholder_active = False

    def on_focus_out(self, e):
        #If the entry is empty, restore the placeholder
        if not self.get():
            self.insert(0, self.placeholder)
            self.config(fg = "#666666")
            self.placeholder_active = True

    def get_value(self):
        #Get the value or return empty string if there is a placeholder
        if self.placeholder_active:
            return ""
        return self.get()
    
class StyledLabel(tk.Label):
    def __init__(self, parent, text, size=12, bold=False, **kwargs):
        font_tuple = ("Coda", size, "bold" if bold else "normal")
        super().__init__(
            parent,
            text=text,
            bg=BG_COLOUR,
            fg=TEXT_COLOUR,
            font=font_tuple,
            **kwargs
        )

def create_frame(parent):
    #Create a styled frame
    return tk.Frame(parent, bg = BG_COLOUR)

def show_message(parent, message, is_error = True):
    #Displays message and returns it so it can be destroyed later
    colour = "#FF4444" if is_error else "#44FF44"
    label = tk.Label(
        parent,
        text = message,
        bg = BG_COLOUR,
        fg = colour,
        font = ("Coda", 10)
    )
    return label
