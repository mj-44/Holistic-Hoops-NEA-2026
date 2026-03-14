import hashlib

#Hashing the password for the password storage to be secure in the database
def hashPassword(password):
    return hashlib.sha256(password.encode()).hexdigest()

#Validating the username entry against certain conditions to ensure it is of a suitable format to be entered into the database
def validateUsername(username):
    if not username:
        return False, "Username cannot be empty"
    
    if len(username)<3:
        return False, "Username must be at least 3 characters"
    
    if len(username)>20:
        return False, "Username must be less than 20 characters"
    
    if not username.isalnum():
        return False, "Username must only contain letters and numbers"
    
    return True, ""

#Validates the users entry of password when they register to ensure its suitable
def validatePassword(password):
    if not password:
        return False, "Password cannot be empty"
    
    if len(password) < 8:
        return False, "Password must be at least 8 characters"
    
    return True, ""

#Verifies the users entry when they use the login page
def verifyLogin(username, password):
    from database import get_user
    #Checks if the username entered by the user matches a name in the database which should be fetched with the get user function
    user = get_user(username)
    if not user:
        return False, "Invalid username or password", None
    
    #chekcs if the password the user has entered matches the one stored in the database by hashing the users input
    #and checking it against the hashed stored password in the database
    hashedPassword = hashPassword(password)
    if hashedPassword != user["password"]:
        return False, "Invalid username or password", None
    
    return True, "Login successful", user

#verifies the security answer the user has entered on the forgot password page
def verifySecurityAnswer(username, securityAnswer):
    from database import get_user

    #Checks if the username they have entered is actually in the database
    user = get_user(username)
    if not user:
        return False, "Username note found", None
    
    #Hashes the answer from the user and checks it against the hashed security answer in the database to check if they match
    hashedAnswer = hashPassword(securityAnswer.lower())
    if hashedAnswer != user["security_answer"]:
        return False, "Incorrect security answer", None
    
    return True, "Security Answer Verified", user
