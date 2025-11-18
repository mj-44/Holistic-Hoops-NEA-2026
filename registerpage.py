import tkinter as tk
from colourscheme import(
    ButtonStyle, StyledLabel, StyledEntry,
    create_frame, show_message
)

from authenticator import(
    validateUsername, validatePassword, hashPassword
)
from database import add_user

class RegisterPage(tk.Frame):
    #Page for users to create their account
    def __init__(self, parent, controller):
        super().__init__(parent, bg = "#000000")
        self.controller = controller
        self.message_label = None

        #Container
        main_frame = create_frame(self)
        main_frame.place(relx = 0.5, rely = 0.5, anchor = "center")

        #Title
        title = StyledLabel(main_frame, text = "Create Account", size = 26, bold = True)
        title.pack(pady = (0,30))

        #Username
        usernameLabel = StyledLabel(main_frame, text = "Username", size = 12)
        usernameLabel.pack(pady = (10,5))

        self.usernameEntry = StyledEntry(main_frame, width = 30)
        self.usernameEntry.pack(pady = (0, 15))

        #Password
        passwordLabel = StyledLabel(main_frame, text = "Password", size = 12)
        passwordLabel.pack(pady = (10, 5))

        self.passwordEntry = StyledEntry(main_frame, show = "*", width = 30) #censors password upon entry
        self.passwordEntry.pack(pady = (0, 15))

        #Confirm Password
        confirmLabel = StyledLabel(main_frame, text = "Confirm Password", size = 12)
        confirmLabel.pack(pady = (10, 5))

        self.confirmEntry = StyledEntry(main_frame, show = "*", width = 30)
        self.confirmEntry.pack(pady = (0, 15))

        #Security Question
        securityQuestionLabel = StyledLabel(
            main_frame,
            text = "Security Question",
            size = 12
        )
        securityQuestionLabel.pack(pady = (10, 5))

        self.securityQuestionEntry = StyledEntry(main_frame, width = 30)
        self.securityQuestionEntry.pack(pady = (0, 15))

        #Security Answer
        securityAnswerLabel = StyledLabel(
            main_frame,
            text = "Security Answer",
            size = 12
        )
        securityAnswerLabel.pack(pady=(10, 5))

        self.securityAnswerEntry = StyledEntry(main_frame, width = 30)
        self.securityAnswerEntry.pack(pady = (0,25))

        #Register Button
        registerButton = ButtonStyle(
            main_frame,
            text = "Register",
            command = self.register,
            width = 20
        )
        registerButton.pack(pady=10)

        #Login Button
        loginButton = ButtonStyle(
            main_frame,
            text = "Back to Login",
            command = lambda: controller.show_page("LoginPage"),
            width = 20
        )
        loginButton.pack(pady = 10)
 
    def register(self):
        #Handling the clicking of the registration button
        if self.message_label:
            self.message_label.destroy()

        username = self.usernameEntry.get().strip()
        password = self.passwordEntry.get()
        confirmPassword = self.confirmEntry.get()
        securityQuestion = self.securityQuestionEntry.get().strip()
        securityAnswer = self.securityAnswerEntry.get().strip()

        #Validate all the user inputs are filled
        if not all([username, password, confirmPassword, securityQuestion, securityAnswer]):
            self.message_label = show_message(self, "Please fill in all fields")
            self.message_label.place(relx = 0.5, rely = 0.92, anchor = "center")
            return
        
        #Validate username
        isValid, errorMessage = validateUsername(username)
        if not isValid:
            self.message_label = show_message(self, errorMessage)
            self.message_label.place(relx = 0.5, rely = 0.92, anchor = "center")
            return
        
        #Validate Password
        isValid, errorMessage = validatePassword(password)
        if not isValid:
            self.message_label = show_message(self, errorMessage)
            self.message_label.place(relx = 0.5, rely = 0.92, anchor = "center")
            return
        
        #Hash Password and Security Answer
        hashedPassword = hashedPassword(password)
        hashedAnswer = hashedAnswer(securityAnswer)

        #Add the user to the database
        success = add_user(
            username,
            hashedPassword,
            securityQuestion,
            hashedAnswer
        )

        if success:
            self.usernameEntry.delete(0, tk.END)
            self.passwordEntry.delete(0, tk.END)
            self.confirmEntry.delete(0, tk.END)
            self.securityQuestionEntry.delete(0, tk.END)
            self.securityAnswerEntry.delete(0, tk.END)

            #Show success message
            self.message_label = show_message(
                self,
                "Successfully Created Account! The grind begins today.",
                is_error=False
            )
            self.message_label.place(relx = 0.5, rely = 0.92, anchor = "center")
            #here, the page should be redirected to the main menu after registering

        else:
            self.message_label = show_message(
                self,
                "Username already exists"
            )
            self.message_label.place(relx = 0.5, rely = 0.92, anchor = "center")
