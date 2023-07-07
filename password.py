import string
import random
import pyperclip
import datetime
import re
import tkinter as tk
from PIL import ImageTk, Image
from tkinter import messagebox
from tkcalendar import Calendar
from ttkthemes import ThemedStyle
#from ttkwidgets import AnimatedButton
from login_module import login
from submit import submit_account

root = tk.Tk()
password_entry_generator = tk.Entry(root)  # Global variable declaration

#######################################################
############# CREATION OF ACCOUNT ##############
####################################################
def create_account():
    global username_entry, password_entry, id_entry, dob_entry, gender_var
    ############# USERNAME, PASSWORD INPUT  ##############
    username_entry.delete(0, tk.END)
    password_entry.delete(0, tk.END)

    label_username.config(text="Username:")
    label_password.config(text="Password:")

    label_password_strength = tk.Label(root, text="Password Strength:", fg="gray")
    label_password_strength.grid(row=4, column=0, padx=5, sticky="e")
    password_strength_bar = tk.Label(root, bg="light gray", width=20)
    password_strength_bar.grid(row=4, column=1, padx=5, sticky="w")

    def update_password_strength(password):
        strength = calculate_password_strength(password)
        if strength == "weak":
            password_strength_bar.config(bg="red")
        elif strength == "medium":
            password_strength_bar.config(bg="orange")
        else:
            password_strength_bar.config(bg="green")

    def calculate_password_strength(password):
        length = len(password)
        if length < 8:
            return "weak"
        elif length < 12:
            if any(c.isupper() for c in password) and any(c.isdigit() for c in password):
                return "medium"
            else:
                return "weak"
        else:
            if any(c.isupper() for c in password) and any(c.isdigit() for c in password) and any(c in string.punctuation for c in password):
                return "strong"
            else:
                return "medium"

    def on_password_entry_change(event):
        password = password_entry.get()
        update_password_strength(password)

    password_entry.bind("<KeyRelease>", on_password_entry_change)

    # Password requirements label
    label_password_requirements = tk.Label(root, text="Password requirements: 8-32 characters, at least one uppercase, one lowercase, one digit, and one special character")
    label_password_requirements.grid(row=5, column=0, columnspan=2, pady=5)

    ############# EMPLOYEE ID INPUT  ##############
    label_id = tk.Label(root, text="Employee ID:")
    label_id.grid(row=6, column=0, padx=5, sticky="e")
    id_entry = tk.Entry(root, fg="gray")
    id_entry.insert(0, "Enter your ID")
    id_entry.grid(row=6, column=1, padx=5, sticky="w")

    def clear_form_fields():
        username_entry.delete(0, tk.END)
        password_entry.delete(0, tk.END)
        id_entry.delete(0, tk.END)
        dob_entry.delete(0, tk.END)
        gender_var.set("Male")  # Reset the gender selection

    def perform_account_submission():
        username_value = username_entry.get()
        password_value = password_entry.get()
        id_value = id_entry.get()
        dob_value = dob_entry.get()
        gender_value = gender_var.get()

        result = submit_account(username_entry, password_entry, id_entry, dob_entry, gender_var)
        if result == "created":
            messagebox.showinfo("Account Creation", "Account created successfully!")
            clear_form_fields()
        elif result == "duplicate":
            messagebox.showerror("Account Creation", "Error: Duplicate username. Please choose a different username.")
        else:
            messagebox.showerror("Account Creation", "Error occurred while creating the account.")

    def clear_id_entry(event):
        if id_entry.get() == "Enter your ID":
            id_entry.delete(0, tk.END)
            id_entry.config(fg="black")

    def restore_id_entry(event):
        if id_entry.get() == "":
            id_entry.insert(0, "Enter your ID")
            id_entry.config(fg="gray")

    id_entry.bind("<FocusIn>", clear_id_entry)
    id_entry.bind("<FocusOut>", restore_id_entry)

    ############# DATE OF BIRTH INPUT  ##############
    label_dob = tk.Label(root, text="Date of Birth:")
    label_dob.grid(row=7, column=0, padx=5, sticky="e")

    # Calendar for selecting the date of birth
    current_year = datetime.datetime.now().year
    default_dob = f"{current_year}-01-01"  # Default DOB as January 1st of the current year
    dob_entry = tk.Entry(root, fg="gray")
    dob_entry.insert(0, default_dob)
    dob_entry.grid(row=7, column=1, padx=5, sticky="w")

    def clear_dob_entry(event):
        if dob_entry.get() == "Click to select a date":
            dob_entry.delete(0, tk.END)
            dob_entry.config(fg="black")

    def select_dob():
        def get_selected_date():
            selected_date = cal.selection_get()
            dob_entry.delete(0, tk.END)
            dob_entry.insert(0, selected_date.strftime("%Y-%m-%d"))
            top.destroy()

        top = tk.Toplevel(root)
        cal = Calendar(top, date_pattern="yyyy-mm-dd", font="Arial 10", selectmode="day")
        cal.pack(pady=10)
        button_select = tk.Button(top, text="Select", command=get_selected_date)
        button_select.pack(pady=5)

    dob_entry.bind("<FocusIn>", clear_dob_entry)
    dob_entry.bind("<Button-1>", lambda event: select_dob())

    ############# GENDER SELECTION  ##############
    label_gender = tk.Label(root, text="Gender:")
    label_gender.grid(row=8, column=0, padx=5, sticky="e")
    gender_var = tk.StringVar()
    gender_var.set("Male")  # Default selection
    gender_options = ["Male", "Female", "Other"]
    gender_dropdown = tk.OptionMenu(root, gender_var, *gender_options)
    gender_dropdown.grid(row=8, column=1, padx=5, sticky="w")

    def clear_gender_dropdown(event):
        gender_var.set("")

    def restore_gender_dropdown(event):
        if gender_var.get() == "":
            gender_var.set("Male")

    gender_dropdown.bind("<Button-1>", clear_gender_dropdown)
    gender_dropdown.bind("<FocusOut>", restore_gender_dropdown)

    # Move the password requirements label to a lower row
    label_password_requirements.grid(row=5, column=0, columnspan=2, pady=5)

    # Hide the "Forgot Password" button
    login_button.grid_forget()
    new_user_label.grid_forget()
    forgot_button.grid_forget()

    # Place the submit button at the bottom
    create_account_button.grid_forget()
    submit_button = tk.Button(root, text="Submit", fg="blue", relief="flat", command=perform_account_submission)
    submit_button.grid(row=10, columnspan=2, pady=5)

    def clear_username_entry(event):
        if username_entry.get() == "Enter your username":
            username_entry.delete(0, tk.END)
            username_entry.config(fg="black")

    def restore_username_entry(event):
        if username_entry.get() == "":
            username_entry.insert(0, "Enter your username")
            username_entry.config(fg="gray")

    def clear_password_entry(event):
        if password_entry.get() == "Enter your password":
            password_entry.delete(0, tk.END)
            password_entry.config(fg="black", show="*")

    def restore_password_entry(event):
        if password_entry.get() == "":
            password_entry.insert(0, "Enter your password")
            password_entry.config(fg="gray", show="")

    #toggle_password_visibility(password_entry)

    username_entry.bind("<FocusIn>", clear_username_entry)
    username_entry.bind("<FocusOut>", restore_username_entry)
    password_entry.bind("<FocusIn>", clear_password_entry)
    password_entry.bind("<FocusOut>", restore_password_entry)

    # Set watermarks for input fields
    username_entry.insert(0, "Enter your username")
    username_entry.config(fg="gray")
    password_entry.insert(0, "Enter your password")
    password_entry.config(fg="gray", show="")

def generate_password():
    global password_entry_generator  # Access the global variable

    password_length = random.randint(8, 32)  # Random length between 8 and 32

    lowercase_letters = string.ascii_lowercase
    uppercase_letters = string.ascii_uppercase
    digits = string.digits
    special_characters = string.punctuation

    # Ensure at least one character from each category
    password = [
        random.choice(lowercase_letters),
        random.choice(uppercase_letters),
        random.choice(digits),
        random.choice(special_characters)
    ]

    # Generate remaining characters
    remaining_length = password_length - 4
    password.extend(random.choices(lowercase_letters + uppercase_letters + digits + special_characters, k=remaining_length))

    # Shuffle the password characters
    random.shuffle(password)

    # Convert the list to a string
    random_password = ''.join(password)

    password_entry_generator.delete(0, tk.END)  # Clear the existing content
    password_entry_generator.insert(0, random_password)
    pyperclip.copy(random_password)

def toggle_password_visibility(password_entry):
    if password_visible.get():
        password_visible.set(False)
        eye_button.config(image=eye_closed_image)
        password_entry.config(show="*")
    else:
        password_visible.set(True)
        eye_button.config(image=eye_open_image)
        password_entry.config(show="")

def perform_login():
    username, password = login_entry.get(), password_entry.get()

    if not login(username, password):
        messagebox.showinfo("Login", "Logged in successfully!")
    else:
        messagebox.showerror("Login", "Invalid username or password!")

def resize_image(event):
    new_width = event.width
    new_height = event.height
    resized_image = original_image.resize((new_width, new_height))
    background_label.configure(image=resized_image)
    background_label.image = resized_image


#######################################################
############# CREATE THE MAIN WINDOW  ##############
####################################################
root.title("Login Panel")
#root.geometry("900x600")

# Set the theme style to a funky theme
style = ThemedStyle(root)
style.set_theme("plastik")

# Load and resize the background image
original_image = Image.open("pexels-anni-roenkae-2457278.jpg")
width, height = root.winfo_screenwidth(), root.winfo_screenheight()
resized_image = original_image.resize((width, height))
background_image = ImageTk.PhotoImage(resized_image)

background_label = tk.Label(root, image=background_image)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

# Bind the resize event to the function
root.bind("<Configure>", resize_image)

# Load eye icon images
eye_open_image = ImageTk.PhotoImage(Image.open("eye_open.png").resize((20, 20)))
eye_closed_image = ImageTk.PhotoImage(Image.open("eye_closed.png").resize((20, 20)))
# Create a variable to track password visibility
password_visible = tk.BooleanVar(value=False)

middle_column = int(root.grid_size()[0] / 2)
# Create and pack the widgets
label_title = tk.Label(root, text="Login", font=("Arial", 24, "bold"))
label_title.grid(row=0, column=middle_column, columnspan=2, pady=10)

label_username = tk.Label(root, text="Username:")
label_username.grid(row=1, column=0, padx=5, sticky="e")

username_entry = tk.Entry(root)
username_entry.grid(row=1, column=1, padx=5, sticky="w")

label_password = tk.Label(root, text="Password:")
label_password.grid(row=2, column=0, padx=5, sticky="e")

password_entry = tk.Entry(root, show="*", font=("Arial", 12), width=30)
password_entry.grid(row=2, column=1, padx=5, sticky="w")

#password_requirements = tk.Label(root, text="Password Requirements:\n- At least 8 characters\n- Uppercase and lowercase letters\n- At least one digit\n- At least one special character", font=("Arial", 10), justify="left")
#password_requirements.grid(row=3, columnspan=2, pady=5)

eye_button = tk.Button(root, image=eye_closed_image, relief="flat", command=toggle_password_visibility)
eye_button.grid(row=2, column=2, padx=5)
eye_button.config(command=toggle_password_visibility)

login_button = tk.Button(root, text="Login", command=perform_login)
login_button.grid(row=4, columnspan=2, pady=10)
login_entry = tk.Entry(root, font=("Calibri", 11, "normal"), width=20)

forgot_button = tk.Button(root, text="Forgot Password", command=generate_password)
forgot_button.grid(row=5, columnspan=2, pady=5)

new_user_label = tk.Label(root, text="New user? ", font=("Arial", 10), justify="left")
new_user_label.grid(row=6, columnspan=2, pady=5)

create_account_button = tk.Button(root, text="Create Account", fg="blue", relief="flat", command=create_account)
create_account_button.grid(row=7, columnspan=2, pady=5)

# Load back and home icons
back_icon = ImageTk.PhotoImage(Image.open("back_icon.png").resize((20, 20)))
home_icon = ImageTk.PhotoImage(Image.open("home_icon.png").resize((20, 20)))

# Create labels for back and home icons
'''back_label = tk.Label(root, image=back_icon)
home_label = tk.Label(root, image=home_icon)

# Place the labels on the top-left corner
back_label.grid(row=0, column=0, padx=5, pady=5, sticky="nw")
home_label.grid(row=0, column=1, padx=5, pady=5, sticky="nw")'''

# Create the back and home buttons
button_home = tk.Button(root, image=back_icon, command=create_account)
button_home.grid(row=0, column=0, padx=10, pady=10, sticky="w")

button_back = tk.Button(root, image=home_icon, command=perform_login)
button_back.grid(row=0, column=1, padx=2, pady=10, sticky="w")

# Start the main event loop
root.mainloop()
