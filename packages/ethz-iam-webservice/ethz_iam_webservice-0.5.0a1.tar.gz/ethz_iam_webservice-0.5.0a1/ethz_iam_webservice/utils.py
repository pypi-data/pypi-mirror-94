import secrets
import string
import re
allowed_special_chars = ', ; . : - ( ) { } / \ '.split()


def check_password(password):
    if len(password) < 12:
        raise ValueError("Password is too short, it should contain at least 12 characters")

    match = re.search(r'\s+', password)
    if match:
        raise ValueError("Password must not contain any whitespace")

    match = re.search(r'([^a-zA-Z0-9\,\;\.\:\-\(\)\{\}\/\\]+)', password)
    if match:
        raise ValueError("Password contains illegal character: {}".format(', '.join(match.groups()) ) )

    has_uppercase = 0
    if any(char.lower() != char for char in password):
        has_uppercase = 1

    has_lowercase = 0
    if any(char.upper() != char for char in password):
        has_lowercase = 1

    has_number = 0
    if any(char.isdigit() for char in password):
        has_number = 1

    has_special_char = 0
    if any(char in allowed_special_chars for char in password):
        has_special_char = 1

    score =  has_uppercase+has_lowercase+has_number+has_special_char
    if score > 2:
        return True
    else:
        return False


def gen_password():
    alphabet = string.ascii_letters + string.digits + ''.join(allowed_special_chars)
    password = ''
    while True:
        password = ''.join(secrets.choice(alphabet) for i in range(15))
        if check_password(password):
            break
    return password
