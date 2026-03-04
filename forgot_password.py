import tkinter as tk
from colourscheme import(ButtonStyle, StyledLabel, StyledEntry, create_frame, show_message)
from authenticator import(verifySecurityAnswer, validatePassword, hashPassword)
from database import get_user, updatePassword
from thememanager import theme_manager

class ForgotPasswordPage(tk.Frame):
    #Page where the user can recover their account by resetting their password
    def __init__(self, parent, controller):
        super().__init__(parent, background = "#000000")
        self.controller = controller
        self.message_label = None
        self.securityQuestionText = None
        theme_manager.register(lambda: self.configure(background=theme_manager.colours["background"]))

        #Container
        main_frame = create_frame(self)
        main_frame.place(relx = 0.5, rely = 0.5, anchor = "center")

        #Title
        title = StyledLabel(
            main_frame,
            text = "Reset Password",
            size = 26,
            bold = True
        )
        title.pack(pady = (0,30))

        #Username
        usernameLabel = StyledLabel(main_frame, text = "Username", size = 12)
        usernameLabel.pack(pady = (10,5))

        self.usernameEntry = StyledEntry(main_frame, width = 30)
        self.usernameEntry.pack(pady = (0, 15))

        #Button loading security question
        loadButton = ButtonStyle(
            main_frame,
            text = "Load Security Question",
            command = self.loadSecurityQuestion,
            width = 20
        )
        loadButton.pack(pady = 10)

        #Displaying security question
        self.securityQuestionDisplay = StyledLabel(
            main_frame,
            text = "",
            size = 11
        )
        self.securityQuestionDisplay.pack(pady = (20, 5))

        #Security Answer Field
        securityAnswerLabel = StyledLabel(
            main_frame,
            text = "Your Answer",
            size = 12
        )
        securityAnswerLabel.pack(pady = (10, 5))

        self.securityAnswerEntry = StyledEntry(main_frame, width = 30)
        self.securityAnswerEntry.pack(pady = (0, 15))

        #Create a field for the user to enter their new password
        newPasswordLabel = StyledLabel(main_frame, text = "New Password", size = 12)
        newPasswordLabel.pack(pady = (10, 5))

        self.newPasswordEntry = StyledEntry(main_frame, show = "*", width = 30)
        self.newPasswordEntry.pack(pady = (0, 15))

        #Confirm New Password
        confirmPasswordLabel = StyledLabel(
            main_frame,
            text = "Confirm New Password",
            size = 12
        )
        confirmPasswordLabel.pack(pady = (10, 5))

        self.confirmPasswordEntry = StyledEntry(main_frame, show = "*", width = 30)
        self.confirmPasswordEntry.pack(pady = (0, 25))

        #Reset Password Button
        resetButton = ButtonStyle(
            main_frame,
            text = "Reset Password",
            command = self.resetPassword,
            width = 20
        )
        resetButton.pack(pady = 10)

        #Button to return to the login page
        backButton = ButtonStyle(
            main_frame,
            text = "Back to Login",
            command = lambda: controller.show_page("LoginPage"),
            width = 20
        )
        backButton.pack(pady = 10)

        theme_manager.register(self.apply_theme)

    def apply_theme(self):
        c = theme_manager.colours
        self.configure(background=c["background"])

    def loadSecurityQuestion(self):
        #Load display and user's security question
        if self.message_label:
            self.message_label.destroy()

        username = self.usernameEntry.get().strip()

        if not username:
            self.message_label = show_message(self, "Please enter your username")
            self.message_label.place(relx = 0.5, rely = 0.92, anchor = "center")
            return
        
        #Get user from database
        user = get_user(username)

        if not user:
            self.message_label = show_message(self, "Username not found")
            self.message_label.place(relx = 0.5, rely = 0.92, anchor = "center")
            return
        
        #Display security question
        self.securityQuestionText = user["security_question"]
        self.securityQuestionDisplay.config(
            text = f"Security Question: {self.securityQuestionText}"
        )

        self.message_label = show_message(
            self,
            "Security question loaded!",
            is_error = False
        )
        self.message_label.place(relx = 0.5, rely = 0.92, anchor = "center")

    def resetPassword(self):
        #Clears any previous messages
        if self.message_label:
            self.message_label.destroy()

        #Get all input values
        username = self.usernameEntry.get().strip()
        securityAnswer = self.securityAnswerEntry.get().strip()
        newPassword = self.newPasswordEntry.get()
        confirmPassword = self.confirmPasswordEntry.get()

        #validate fields
        if not all([username, securityAnswer, newPassword, confirmPassword]):
            self.message_label = show_message(self, "Please fill in all fields")
            self.message_label.place(relx = 0.5, rely = 0.92, anchor = "center")
            return
        
        #Verify answer to the security question
        is_valid, message, user_data = verifySecurityAnswer(
            username,
            securityAnswer
        )

        if not is_valid:
            self.message_label = show_message(self, message)
            self.message_label.place(relx = 0.5, rely = 0.92, anchor = "center")
            return
        
        #Validate new password
        is_valid, error_msg = validatePassword(newPassword)
        if not is_valid:
            self.message_label = show_message(self, error_msg)
            self.message_label.place(relx = 0.5, rely = 0.92, anchor = "center")
            return
        
        #Check that the new password is the same as the confirmed password
        if newPassword != confirmPassword:
            self.message_label = show_message(self, "Passwords do not match")
            self.message_label.place(relx = 0.5, rely = 0.92, anchor = "center")
            return
        
        #Hash new password
        hashedPassword = hashPassword(newPassword)

        #Update the password to the database
        success = updatePassword(username, hashedPassword)

        if success:
            #Clear fields
            self.usernameEntry.delete(0, tk.END)
            self.securityAnswerEntry.delete(0, tk.END)
            self.newPasswordEntry.delete(0, tk.END)
            self.confirmPasswordEntry.delete(0, tk.END)
            self.securityQuestionDisplay.config(text = "")

            #Show success message
            self.message_label = show_message(
                self,
                "Successfully Reset Password",
                is_error = False
            )
            self.message_label.place(relx = 0.5, rely = 0.92, anchor = "center")

            #Redirect to login page after a couple of seconds
            self.after(2000, lambda: self.controller.show_page("LoginPage"))

        else:
            self.message_label = show_message(
                self,
                "Failed to reset password, please try again."
            )
            self.message_label.place(relx = 0.5, rely = 0.92, anchor = "center")