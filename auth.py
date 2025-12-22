import re
import hashlib


def validate_password(password):
    """Validate password: must have uppercase, lowercase, and symbols"""
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter"
    if not re.search(r'[a-z]', password):
        return False, "Password must contain at least one lowercase letter"
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False, "Password must contain at least one special character (!@#$%^&*)"
    return True, "Password is valid"


def hash_password(password):
    """Hash password using SHA256"""
    return hashlib.sha256(password.encode()).hexdigest()


def authenticate_user(username, password):
    """
    Authenticate user - Replace this with database check
    For now: simple validation (replace with DB query)
    """
    # TODO: Replace with actual database authentication
    if username and password:
        return True
    return False


def register_user(username, password):
    """
    Register new user - Replace this with database insert
    For now: simple validation (replace with DB insert)
    """
    # TODO: Replace with actual database insert
    is_valid, msg = validate_password(password)
    if is_valid:
        return True, "Registration successful!"
    return False, msg
