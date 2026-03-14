import tkinter as tk
from homepage import HomePage
from loginpage import LoginPage
from registerpage import RegisterPage
from forgot_password import ForgotPasswordPage
from mainmenu import MainMenu
from trainingmenu import TrainingMenu
from shootingmenu import ShootingMenu
from dribblingmenu import DribblingMenu
from footworkmenu import FootworkMenu
from finishingmenu import FinishingMenu
from dribblepullupdrill import DribblePullUpDrill
from alleydrill import AlleyDrill
from aroundtheworld import AroundTheWorld
from backpedalfinishing import BackPedalFinishing
from backpedalfinishingpf import BackPedalFinishingPF
from conetouchfinishing import ConeTouchFinishing
from fresnoattack import FresnoAttack
from offbalancepullups import OffBalancePullUps
from rangerumble import RangeRumble
from fullcourtweave import FullcourtWeaveDrill
from spinmove import SpinMoveDrill
from settingsmenu import SettingsMenu
from drivinglay import DrivingLayDrill
from comparisonmenu import ComparisonMenu
from trackermenu import TrackerMenu
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
        
        self.root.configure(background = "#000000")

        initialise_database()

        #Create a container to hold all pages and stack them
        self.container = tk.Frame(self.root, background = "#000000")
        self.container.pack(fill = "both", expand = True)

        #create dictionary to store pages
        self.pages = {}

        for PageClass in (HomePage, LoginPage, RegisterPage, ForgotPasswordPage, MainMenu, TrainingMenu, ShootingMenu, DribblingMenu, FootworkMenu, FinishingMenu, DribblePullUpDrill, AlleyDrill, AroundTheWorld, BackPedalFinishing, BackPedalFinishingPF, ConeTouchFinishing, FresnoAttack, OffBalancePullUps, RangeRumble, FullcourtWeaveDrill, SpinMoveDrill, DrivingLayDrill, SettingsMenu, ComparisonMenu, TrackerMenu):
            page_name = PageClass.__name__
            page = PageClass(parent = self.container, controller = self)
            self.pages[page_name] = page
            page.place(relx = 0, rely = 0, relwidth = 1, relheight = 1)

        #Start by showing the home page
        self.show_page("HomePage")

    def get_current_user(self):
        return self.current_user

    def set_current_user(self, user_data):
        self.current_user = user_data
        self.pages["ComparisonMenu"].set_current_user(user_data["username"])
        self.pages["TrackerMenu"].set_current_user(user_data["username"])

    def show_page(self, page_name):
        page = self.pages[page_name]
        page.tkraise()

    def run(self):
        self.root.mainloop()

    def show_page(self, page_name):
        #Brings a page to the front and can be called on by buttons to navigate pages
        page = self.pages[page_name]
        page.tkraise()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = BasketballApp()
    app.run()
