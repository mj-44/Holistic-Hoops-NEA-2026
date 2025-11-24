import hashlib

def hashPassword(password):
    #use SHA-256 for secure storage
    return hashlib.sha256(password.encode()).hexdigest()

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

def validatePassword(password):
    if not password:
        return False, "Password cannot be empty"
    if len(password) < 8:
        return False, "Password must be at least 8 characters"
    return True, ""

def verifyLogin(username, password):
    from database import get_user

    user = get_user(username)
    if not user:
        return False, "Invalid username or password", None
    
    hashedPassword = hashPassword(password)
    if hashedPassword != user["password"]:
        return False, "Invalid username or password"
    
    return True, "Login successful", user

def verifySecurityAnswer(username, securityAnswer):
    from database import get_user

    user = get_user(username)
    if not user:
        return False, "Username note found", None
    
    hashedAnswer = hashPassword(securityAnswer.lower())
    if hashedAnswer != user["security_answer"]:
        return False, "Incorrect security answer", None
    
    return True, "Security Answer Verified", user