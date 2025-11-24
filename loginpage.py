import tkinter as tk
from colourscheme import(
    ButtonStyle, StyledLabel, StyledEntry,
    create_frame, show_message
)
from authenticator import verifyLogin

class LoginPage(tk.Frame):
    #code for the login page so the user can enter credentials
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#000000")
        self.controlerr = controller
        self.message_label = None #stores the result of the verification
        
        #container
        main_frame = create_frame(self)
        main_frame.place(relx=0.5, rely=0.5, anchor = "center")

        #Title
        title = StyledLabel(main_frame, text = "Login", size = 26, bold = True)
        title.pack(pady=(0,40))

        #Username
        usernameLabel = StyledLabel(main_frame, text = "Username", size = 12)
        usernameLabel.pack(pady=(10,5))

        self.usernameEntry = StyledEntry(main_frame, width = 30)
        self.usernameEntry.pack(pady=(0,20))

        #Password
        passwordLabel = StyledLabel(main_frame, text = "Password", size = 12)
        passwordLabel.pack(pady = (10,5))

        self.passwordEntry = StyledEntry(main_frame, show = "*", width = 30)
        self.passwordEntry.pack(pady = (0,30))

        #Bind the enter key to allow the user to login
        self.passwordEntry.bind("<Return>", lambda e: self.login())

        #Login Button
        loginButton = ButtonStyle(
            main_frame,
            text = "Login",
            command = self.login,
            width = 20
        )
        loginButton.pack(pady=10)

        #Register Button
        registerButton = ButtonStyle(
            main_frame,
            text = "Register",
            command = lambda: controller.show_page("RegisterPage"),
            width = 20
        )
        registerButton.pack(pady=10)

        #Forgot Password Button
        forgotpasswordButton = ButtonStyle(
            main_frame,
            text = "Forgot Password",
            command = lambda: controller.show_page("ForgotPasswordPage"),
            width = 20
        )
        forgotpasswordButton.pack(pady = 10)

    def login(self):
        #Handle login button click
        if self.message_label:
            self.message_label.destroy()

        #Get inputs
        username = self.usernameEntry.get().strip()
        password = self.passwordEntry.get()

        #Validate
        if not username or not password:
            self.message_label = show_message(self, "Please Enter something for all fields")
            self.message_label.place(relx = 0.5, rely = 0.85, anchor = "center")
            return
        
        #Verify
        is_valid, message, user_data = verifyLogin(username, password)

        if is_valid:
            #If the entries are valid, clear the boxes and give a success message
            self.usernameEntry.delete(0, tk.END)
            self.passwordEntry.delete(0, tk.END)

            self.message_label = show_message(
                self,
                "Login Successful! The grind continues.",
                is_error=False
            )
            self.message_label.place(relx = 0.5, rely = 0.85, anchor = "center")
            #This will redirect to the main menu once made

        else:
            self.message_label = show_message(self, message)
            self.message_label.place(relx = 0.5, rely = 0.85, anchor = "center")