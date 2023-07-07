import string
import random
from tkinter import messagebox

def generate_alternative_username(username):
    suggestions = []
    username = username.lower()
    alternatives = ["@", "_", "#", "$", "&"]
    for alternative in alternatives:
        for i in range(10):
            suggestion = username + alternative + str(i)
            suggestions.append(suggestion)
    return suggestions

def generate_alternative_password(password):
    suggestions = []
    alternatives = string.ascii_uppercase + string.ascii_lowercase + string.digits + string.punctuation

    while len(suggestions) < 3:
        suggestion = ''.join(random.sample(alternatives, min(len(password), 32)))
        suggestions.append(suggestion)

    return suggestions

def submit_account(username_entry, password_entry, id_entry, dob_entry, gender_var):
    username_value = username_entry.get()
    password_value = password_entry.get()
    id_value = id_entry.get()
    dob = dob_entry.get()
    gender = gender_var.get()

    with open("user_credentials.txt", "r") as file:
        existing_usernames = [line.split(",")[0] for line in file]
        existing_passwords = [line.split(",")[1] for line in file]

    if username_value in existing_usernames:
        suggestions = generate_alternative_username(username_value)
        suggestion_text = "\n".join(f"- {suggestion}" for suggestion in suggestions)
        messagebox.showinfo(
            "Duplicate Username",
            f"The username '{username_value}' is already taken.\n\nTry one of the following suggestions:\n\n{suggestion_text}\n\nOr choose a different username.",
        )
        return "duplicate_username"
    elif password_value in existing_passwords:
        suggestions = generate_alternative_password(password_value)
        suggestion_text = "\n".join(f"- {suggestion}" for suggestion in suggestions)
        messagebox.showinfo(
            "Duplicate Password",
            f"The password you entered is already in use.\n\nTry one of the following suggestions:\n\n{suggestion_text}\n\nOr choose a different password.",
        )
        return "duplicate_password"
    else:
        with open("user_credentials.txt", "a") as file:
            file.write(f"{username_value},{password_value},{id_value},{dob},{gender}\n")

        return "created"
