import tkinter as tk
from homepage import HomePage
from loginpage import LoginPage
from registerpage import RegisterPage
from forgot_password import ForgotPasswordPage
from database import initialise_database

class BasketballApp:
    #main program which is the entry point to the program
    #Handles different windows and navigating between pages
    def __init__(self):
        #Creates the main window
        self.root = tk.Tk()
        self.root.title("Hollistic Hoops")

        #setting fixed window size of the app
        self.root.geometry("720x1280")
        self.root.resizable(False, False)
        
        self.root.configure(bg = "#000000")

        initialise_database()

        #Create a container to hold all pages and stack them
        self.container = tk.Frame(self.root, bg = "#000000")
        self.container.pack(fill = "both", expand = True)

        #create dictionary to store pages
        self.pages = {}

        for PageClass in (HomePage, LoginPage, RegisterPage, ForgotPasswordPage):
            page_name = PageClass.__name__
            page = PageClass(parent = self.container, controller = self)
            self.pages[page_name] = page
            page.place(relx = 0, rely = 0, relwidth = 1, relheight = 1)

        #Start by showing the home page
        self.show_page("HomePage")

    def show_page(self, page_name):
        #Brings a page to the front and can be called on by buttons to navigate pages
        page = self.pages[page_name]
        page.tkraise()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = BasketballApp()
    app.run()