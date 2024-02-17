import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox
from tkinter.filedialog import askopenfilename
import csv
import re
import os.path
from PIL import Image, ImageTk

# create the desktop window
app = ctk.CTk()

# set the dimension to the window
app.geometry("700x600")

# set the dimension of the window to be permanent
app.resizable(False, False)

# set the title of window
app.title("User Account Registration System")

# Set the background color
app.configure(bg="lightgray")

# Validation Check Functions

# Function to check the presence of data for each entry
def is_present(value):
    # Check if the value is not an empty string and not None
    return value is not None and value != ""


# Function to check the format of Date of Birth Entry
def is_valid_date_of_birth(date_of_birth):
    # Define the regular expression pattern for DD/MM/YYYY
    date_pattern = re.compile(r'^\d{2}/\d{2}/\d{4}$')

    # Check if the date_of_birth matches the pattern
    return bool(date_pattern.match(date_of_birth))


# Function to check the length of (11 digits) and starts with '09'
def is_valid_phone_number(phone_number):
    # Check if the phone number has a length of 11 digits including 09
    return len(str(phone_number)) == 11 and phone_number.startswith('09') and phone_number.isdigit()


# Function to check valid email
def is_valid_email(email):
    regex = r'^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
    return re.match(regex, email)


# Function to check valid password
def is_valid_password(password):
    # Check if the password meets the criteria
    return (
            len(password) >= 8 and  # Check the length of password
            any(char.isdigit() for char in password) and  # Check the digits
            any(char.isalpha() for char in password) and  # Check the characters
            re.search(r'[!@#$%^&*(),.?":{}|<>]', password)  # Check the special character
    )


def Login_page_function():
    # Function to direct to Registration Page
    def forward_to_registration_page():
        Login_page.destroy()
        app.update()
        registration_page_functioin()


    # Function to direct to System User's Dashboard
    def forward_to_system_user_dashboard():
        Login_page.destroy()
        app.update()
        system_user_account_function()


    # Function to direct to End User's Dashboard
    def forward_to_end_user_dashboard():
        Login_page.destroy()
        app.update()
        end_user_account_function()


    # Function to hide and show password
    def show_hide_password():
        if Password_entry.cget("show") == "*":
            Password_entry.configure(show="")
        else:
            Password_entry.configure(show="*")


    # Login Button Function
    def login_button_function():
        email = Email_entry.get()
        password = Password_entry.get()

        # Open csv file to read
        with open("user_accounts.csv", "r", newline="") as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # Skip the header row
            for row in reader:
                stored_email, stored_password, user_type = row[5], row[6], row[7]

                if email == stored_email and password == stored_password:
                    if user_type == "End User":
                        messagebox.showinfo("Success", "End User Login successful")
                        # Display End User's Dashboard
                        forward_to_end_user_dashboard()
                    elif user_type == "System User":
                        messagebox.showinfo("Success", "System User Login successful")
                        # Display System User's Dashboard
                        forward_to_system_user_dashboard()
                    return

            # Display error message if no match is found
            messagebox.showerror("Error", "Invalid email or password")

    # Create Login Page
    Login_page = ctk.CTkFrame(master=app, width=300, height=400, corner_radius=15)
    Login_page.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    # Create labels and entry widgets for login page
    Login_label_1 = ctk.CTkLabel(master=Login_page, text="Login", font=("Helvetica", 20, "bold"))
    Login_label_1.place(x=35, y=40)

    Email_entry = ctk.CTkEntry(master=Login_page, width=260, placeholder_text="Email", font=("Helvetica", 10))
    Email_entry.place(x=20, y=110)

    Password_entry = ctk.CTkEntry(master=Login_page, width=260, placeholder_text="Password", show="*", font=("Helvetica", 10))
    Password_entry.place(x=20, y=160)
    Password_shown_check = ctk.CTkCheckBox(master=Login_page, text="Show Password", command=show_hide_password, font=("Helvetica", 10))
    Password_shown_check.place(x=20, y=200)
    Password_shown_check.configure(checkbox_width=15, checkbox_height=15, border_width=3)
    # Create login button
    login_button = ctk.CTkButton(master=Login_page, text="Sign In", command=login_button_function, width=260,
                                font=("Helvetica", 12, "bold"))
    login_button.place(x=20, y=250)

    # Create a link to register page
    register_label = ctk.CTkLabel(master=Login_page, text="Doesn't have an account? Register", font=("Helvetica", 10), cursor="hand2")
    register_label.place(x=70, y=280)

    # Bind the label to the registration window function
    register_label.bind("<Button-1>", lambda event: forward_to_registration_page())


# Register window
def registration_page_functioin():
    # function to move back to login page
    def forward_to_login_page():
        registration_page.destroy()
        app.update()
        Login_page_function()


    # Function to hide and show password
    def show_hide_password():
        if Password_entry.cget("show") == "*":
            Password_entry.configure(show="")
        else:
            Password_entry.configure(show="*")


    # Register Button Function
    def register_button_function():
        first_name =First_name_entry.get()
        last_name = Last_name_entry.get()
        date_of_birth = Date_of_birth_entry.get()
        phone_number = Phone_number_entry.get()
        address1 = Address_entry1.get()
        address2 = Address_entry2.get()
        email = Email_entry.get()
        password = Password_entry.get()

        # Validation Check
        if not (
                is_present(first_name) or
                is_present(last_name) or
                is_present(date_of_birth) or
                is_present(phone_number) or
                is_present(address1) or
                is_present(address2) or
                is_present(email) or
                is_present(password)
            ):
            messagebox.showinfo("Error", "All data must be entered")

        elif not is_valid_date_of_birth(date_of_birth):
            messagebox.showinfo("Error", "Date Of Birth: Invalid Format")

        elif not is_valid_phone_number(phone_number):
            messagebox.showinfo("Error", "Invalid Phone Number")

        elif not is_valid_email(email):
            messagebox.showinfo("Error", "Invalid Email")

        elif not is_valid_password(password):
            messagebox.showinfo("Error", "Invalid Password")

        else:
            # Check if the file exists
            file_exists = os.path.isfile("user_accounts.csv")

            # Save user data to CSV file
            with open("user_accounts.csv", "a", newline="") as csvfile:
                writer = csv.writer(csvfile)

                # Write header only if the file is empty
                if not file_exists:
                    writer.writerow(["First Name", "Last Name", "Date Of Birth", "Phone Number", "Address", "Email", "Password", "Role"])
                else:
                    # Display the user's input information to doublecheck the entries
                    message = (
                        f"First Name:    {first_name} \n"
                        f"Last Name:     {last_name} \n"
                        f"Date of Birth: {date_of_birth} \n"
                        f"Phone Number:  {phone_number} \n"
                        f"Address:       {address1 + '' + address2} \n"
                        f"Email:         {email} \n"
                        f"Password:      {password}"
                    )
                    result = messagebox.askquestion("User Detail",
                                                    "You are about to enter the following information \n" + message)
                    # if user confirm, the data will be stored in the csv file
                    if result == "yes":
                        writer.writerow([first_name, last_name, date_of_birth, phone_number, address1 + address2, email, password, "End User"])
                        messagebox.showinfo("Info", message="Registration Successful! \n You can now login to the account!", icon="info")
                    else:
                        # clear the entry
                        first_name.set("")
                        last_name.set("")
                        date_of_birth.set("")
                        phone_number.set("")
                        address1.set("")
                        address2.set("")
                        email.set("")
                        password.set("")

    # Create registration age
    registration_page = ctk.CTkFrame(master=app, width=520, height=520, corner_radius=15)
    registration_page.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    # Create backward button
    backward_button = ctk.CTkButton(registration_page, text="←", font=("Helvetica", 10, "bold"), 
                                text_color= "black", fg_color="lightgray", hover_color="lightgray", width=3, command=forward_to_login_page)
    backward_button.place(x=10, y=35)

    # Create labels and entry widgets for registration
    Register_label_1 = ctk.CTkLabel(registration_page, text="REGISTER HERE", font=("Helvetica", 20, "bold"))
    Register_label_1.place(x=45, y=35)

    # Set the scope of Varibles globally
    global First_name_entry, Last_name_entry, Date_of_birth_entry, Phone_number_entry, Address_entry1, Address_entry2, Email_entry, Password_entry

    First_name_entry = ctk.CTkEntry(registration_page, width=200, placeholder_text="First Name", font=("Helvetica", 10))
    First_name_entry.place(x=48, y=90)

    Last_name_entry = ctk.CTkEntry(registration_page, width=200, placeholder_text="Last Name", font=("Helvetica", 10))
    Last_name_entry.place(x=280, y=90)

    Date_of_birth_entry = ctk.CTkEntry(registration_page, width=200, placeholder_text="Date Of Birth (DD/MM/YYYY)",
                                       font=("Helvetica", 10))
    Date_of_birth_entry.place(x=48, y=150)

    Phone_number_entry = ctk.CTkEntry(registration_page, width=200, placeholder_text="Phone Number (09xxxxxxxxx)",
                                      font=("Helvetica", 10))
    Phone_number_entry.place(x=280, y=150)

    Address_entry1 = ctk.CTkEntry(registration_page, width=300, placeholder_text="Address 1", font=("Helvetica", 10))
    Address_entry1.place(x=48, y=220)

    Address_entry2 = ctk.CTkEntry(registration_page, width=300, placeholder_text="Address 2", font=("Helvetica", 10))
    Address_entry2.place(x=48, y=270)

    Email_entry = ctk.CTkEntry(registration_page, width=300, placeholder_text="Email", font=("Helvetica", 10))
    Email_entry.place(x=48, y=320)

    Password_entry = ctk.CTkEntry(registration_page, width=300, placeholder_text="Password", show="*",
                                  font=("Helvetica", 10))
    Password_entry.place(x=48, y=370)
    Password_shown_check = ctk.CTkCheckBox(registration_page, text="Show Password", command=show_hide_password,
                                           font=("Helvetica", 10))
    Password_shown_check.place(x=48, y=400)

    # create register button
    register_button = ctk.CTkButton(registration_page, text="Register", command=register_button_function,
                                    font=("Helvetica", 12, "bold"))
    register_button.place(x=150, y=450)


def system_user_account_function():
    system_user_dashboard = ctk.CTkFrame(master=app, width=600, height=600, corner_radius=15)
    system_user_dashboard.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    # Add labels and display system user information
    system_user_label = ctk.CTkLabel(system_user_profile_window, text="System User Profile", font=("Helvetica", 16, "bold"))
    system_user_label.pack(pady=10)

    # Add more labels and display relevant information for the system user
    


def end_user_account_function():
    pic_path = tk.StringVar()
    pic_path.set("")

    def open_pic():
        path = askopenfilename()

        if path:
            img = ImageTk.PhotoImage(Image.open(path).resize((105,105)))
            pic_path.set(path)

            profile_picture_button.configure(image=img)
            profile_picture_button.image = img


    end_user_dashboard = ctk.CTkFrame(master=app, width=600, height=600, corner_radius=15)
    end_user_dashboard.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    # import default pic
    user_profile_pic = ctk.CTkImage(light_image=Image.open("user_profile_pic.jpg"), dark_image=Image.open("user_profile_pic.jpg"), size=(105,105))

    # Create profile picture frame
    profile_picture = ctk.CTkFrame(end_user_dashboard, width=105, height=105, border_color="black", border_width=2)
    profile_picture.place(x=10, y=10)
    # Create clickable picture  
    profile_picture_button = ctk.CTkButton(profile_picture, image=user_profile_pic, text="",
                                            fg_color="lightgray", anchor="center", width=100,
                                            border_spacing=0, border_width=0, hover_color="lightgray", command=open_pic)
    profile_picture_button.pack()

Login_page_function()
app.mainloop()

"""
# Function to display found user accounts
def display_found_accounts(accounts):
    message = "Found Accounts:\n\n"
    for account in accounts:
        formatted_account = (
            f"First Name: {account[0]} \n"
            f"Last Name: {account[1]}, \n"
            f"Date of Birth: {account[2]}, \n"
            f"Phone Number: {account[3]}, \n"
            f"Address: {account[4]}, \n"
            f"Password: {account[5]}"
        )
        message += f"{formatted_account}\n"
    messagebox.showinfo("Search Results", message)


# Function to display all user accounts
def display_user_accounts():
    with open("user_accounts.csv", "r", newline="") as csvfile:
        reader = csv.reader(csvfile)
        data = list(reader)

    if len(data) > 0:
        # create a new window to display the user account
        display_window = ctk.CTkToplevel(frame_2)
        display_window.title("User Accounts")
        display_window.geometry("800x400")
        display_window.resizable(False, False)

        header_data = data[0]
        for col_num, header in enumerate(header_data):
            header_label = ctk.CTkLabel(master=display_window, text=header, font=("Helvetica", 12, "bold"))
            header_label.grid(row=0, column=col_num, padx=5, pady=5)

        # Data Rows
        for row_num in range(1, len(data)):
            row_data = data[row_num]
            for col_num in range(len(row_data)):
                col_value = row_data[col_num]
                data_label = ctk.CTkLabel(master=display_window, text=col_value, font=("Helvetica", 10))
                data_label.grid(row=row_num, column=col_num, padx=5, pady=5)
    else:
        messagebox.showinfo("User Accounts", "No user accounts found.")


# Function to search user accounts
def search_function():
    search_term = search_entry.get()
    # Validate the present of entry
    if not is_present(search_term):
        messagebox.showerror("Error", "Please enter a search term")
        return

    with open("user_accounts.csv", "r", newline="") as csvfile:
        reader = csv.reader(csvfile)
        data = list(reader)

    found_accounts = [row for row in data[1:] if any(search_term.lower() in col.lower() for col in row)]

    # check if the account is in the data list
    if not found_accounts:
        messagebox.showinfo("Info", "No matching accounts found")
    else:
        display_found_accounts(found_accounts)


# Search Window
def search_window():
    # create a new window for the search
    search_window = ctk.CTkToplevel(system_user_profile_window)
    search_window.title("Search User Accounts")
    search_window.geometry("400x200")

    search_label = ctk.CTkLabel(search_window, text="Enter search term:", font=("Helvetica", 10))
    search_label.pack(pady=10)

    # Set the scope of varible globally
    global search_entry
    search_entry = ctk.CTkEntry(search_window, width=200, font=("Helvetica", 10))
    search_entry.pack(pady=5)

    # create search button
    search_button = ctk.CTkButton(search_window, text="Search", command=search_function, font=("Helvetica", 10))
    search_button.pack(pady=5)


def show_password_rules():
    rules_text = (
        "Password Rules:\n"
        "1. Minimum length: 8 characters\n"
        "2. At least one letter\n"
        "3. At least one digit\n"
        "4. At least one special character"
    )


# create another frame on the right
frame_2 = ctk.CTkFrame(master=app, width=530, height=530, corner_radius=15)
frame_2.place(relx=0.76, rely=0.5, anchor=tk.CENTER)

frame_3 = ctk.CTkFrame(master=app, width=530, height=430, corner_radius=15)
frame_3.place(relx=0.66, rely=0.5, anchor=tk.CENTER)

# create search user account button
search_user_account_button = ctk.CTkButton(master=frame_3, text="Search User Account", command=search_window, font=("Helvetica", 12, "bold"))
search_user_account_button.place(x=25, y=125)

# create display user accounts button
display_user_accounts_button = ctk.CTkButton(master=frame_3, text="Display User Accounts", command=display_user_accounts, font=("Helvetica", 12, "bold"))
display_user_accounts_button.place(x=25, y=195)

# create update user accounts button
Update_Account_button = ctk.CTkButton(master=frame_3, text="Update User Accounts", command=update_user_accounts, font=("Helvetica", 12, "bold"))
Update_Account_button.place(x=25, y=125)
""" 



