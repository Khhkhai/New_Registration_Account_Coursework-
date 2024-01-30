import tkinter
import customtkinter
import csv
import re
from CTkMessagebox import CTkMessagebox
import datetime


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
    if date_pattern.match(date_of_birth):
        return True
    else:
        return False

# Function to check the length of (11 digits) and starts with '09'
def is_valid_phone_number(phone_number):
    # Check if the phone number has a length of 11 digits including 09
    return len(str(phone_number)) == 11 and phone_number.startswith('09') and phone_number.isdigit()


# Function to check valid password
def is_valid_password(password):
    # Check if the password meets the criteria
    if (
        len(password) >= 8 and  # Check the length of password
        any(char.isdigit() for char in password) and  # Check the digits
        any(char.isalpha() for char in password) and  # Check the characters
        re.search(r'[!@#$%^&*(),.?":{}|<>]', password)  # Check the special character
    ):
        return True
    else:
        return False


# Functions associated with buttons
# Register Function
def register_button_function():
    First_name = First_name_entry.get()
    Last_name = Last_name_entry.get()
    Date_of_birth = Date_of_birth_entry.get()
    Phone_number = Phone_number_entry.get()
    Address = Address_entry.get()
    Password = Password_entry.get()

    # Validation Check
    if not (
        is_present(First_name) or
        is_present(Last_name) or
        is_present(Date_of_birth) or
        is_present(Phone_number) or
        is_present(Address) or
        is_present(Password)
    ):
        print("Error")
        CTkMessagebox(width=150, height=30, title="Error", message="All data must enter", icon="cancel")

    elif not is_valid_date_of_birth(Date_of_birth):
        CTkMessagebox(width=150, height=30, title="Error", message="Date Of Birth: Invalid Format", icon="cancel")

    elif not is_valid_phone_number(Phone_number):
        CTkMessagebox(width=150, height=30, title="Error", message="Invalid Phone Number", icon="cancel")

    elif not is_valid_password(Password):
        CTkMessagebox(width=150, height=30, title="Error", message="Invalid Password", icon="cancel")

    else:
        # Save user data to CSV file
        with open("user_accounts.csv", "a", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["First Name", " Last Name", " Date Of Birth", " Phone Number", " Address", " Password"])
            writer.writerow([First_name, Last_name, Date_of_birth, Phone_number, Address, Password])
        CTkMessagebox(width=150, height=30, title="Info", message="Account is successfully registered", icon="info")


# Function to shown hidden password
def show_password():
    if Password_entry.cget("show") == "*":
        Password_entry.configure(show="")
    else:
        Password_entry.configure(show="*")


# Function for menu
# Update Function
def update_user_account():
    # Placeholder function for updating user account
    CTkMessagebox(width=300, height=30, title="Search User Account", message="Update functionality will be implemented here.")


# Search Function
def search_user_account():
    # Placeholder function for searching user account
    CTkMessagebox(width=350, height=30, title="Search User Account", message="Search functionality will be implemented here.", icon="info")

# Display the message box
def show_message(message):
    error_box = customtkinter.CTkToplevel(frame_2)
    error_box.title("User Account")
    error_box.geometry("1000x300")
    error_box.resizable(False, False)

    text = customtkinter.CTkLabel(master=error_box, text=message, font=("Century Gothic", 16))
    text.place(x=0, y=0)


# Function to search user accounts
def search_user_account():
    search_window = customtkinter.CTkToplevel(app)
    search_window.title("Search Account")
    search_window.geometry("400x200")

    search_label = customtkinter.CTkLabel(search_window, text="Enter search term:")
    search_label.pack(pady=10)

    search_entry = customtkinter.CTkEntry(search_window, width=200)
    search_entry.pack(pady=5)

    def search_function():
        search_term = search_entry.get()
        if not is_present(search_term):
            CTkMessagebox(width=150, height=30, title="Error", message="Please enter a search term", icon="cancel")
            return

        with open("user_accounts.csv", "r", newline="") as csvfile:
            reader = csv.reader(csvfile)
            data = list(reader)

        found_accounts = []
        for row in data[1:]:  # Skip the header row
            if any(search_term.lower() in col.lower() for col in row):
                found_accounts.append(row)

        if not found_accounts:
            CTkMessagebox(width=150, height=30, title="Info", message="No matching accounts found", icon="info")
        else:
            display_found_accounts(found_accounts)

    def display_found_accounts(accounts):
        # This is a placeholder function. You can customize it based on your needs.
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
        CTkMessagebox(width=600, height=200, title="Search Results", message=message, icon="info")

    search_button = customtkinter.CTkButton(search_window, text="Search", command=search_function)
    search_button.pack(pady=5)


# Display All Use Account Function
def display_user_accounts():
    # Placeholder function for displaying user accounts
    with open("user_accounts.csv", "r", newline="") as csvfile:
        reader = csv.reader(csvfile)
        data = list(reader)

        if len(data) > 0:
            display_window = customtkinter.CTkToplevel(frame_2)
            display_window.title("User Accounts")
            display_window.geometry("800x400")
            display_window.resizable(False, False)

            header_data = data[0]
            for col_num in range(len(header_data)):
                header_label = customtkinter.CTkLabel(master=display_window, text=header_data[col_num],
                                                      font=("Century Gothic", 12, "bold"))
                header_label.grid(row=0, column=col_num, padx=5, pady=5)

            # Data Rows
            for row_num in range(1, len(data)):
                row_data = data[row_num]
                for col_num in range(len(row_data)):
                    col_value = row_data[col_num]
                    data_label = customtkinter.CTkLabel(master=display_window, text=col_value,
                                                        font=("Century Gothic", 10))
                    data_label.grid(row=row_num, column=col_num, padx=5, pady=5)
        else:
            CTkMessagebox(width=150, height=30, title="User Accounts", message="No user accounts found.")


# set the color of the window
customtkinter.set_appearance_mode("dark")

# set the color of the objects
customtkinter.set_default_color_theme("green")

# create the desktop window
app = customtkinter.CTk()

# set the title of window
app.title("Account")

# set the dimension to the window
app.geometry("800x550")

# set the dimension of the window to be permanent
app.resizable(False, False)


# create a frame on the left
frame_1 = customtkinter.CTkFrame(master=app, width=245, height=430, corner_radius=15)
frame_1.place(relx=0.17, rely=0.5, anchor=tkinter.CENTER)
# create another frame on the right
frame_2 = customtkinter.CTkFrame(master=app, width=530, height=430, corner_radius=15)
frame_2.place(relx=0.66, rely=0.5, anchor=tkinter.CENTER)

# create registration form
Register_label_1 = customtkinter.CTkLabel(master=frame_2, text="REGISTER HERE", font=("Helvetica", 25, "underline"))
Register_label_1.place(x=45, y=35)

First_name_entry = customtkinter.CTkEntry(master=frame_2, width=200, placeholder_text="First Name")
First_name_entry.place(x=48, y=90)

Last_name_entry = customtkinter.CTkEntry(master=frame_2, width=200, placeholder_text="Last Name")
Last_name_entry.place(x=280, y=90)

Date_of_birth_entry = customtkinter.CTkEntry(master=frame_2, width=200, placeholder_text="Date Of Birth (DD/MM/YYYY)")
Date_of_birth_entry.place(x=48, y=150)

Phone_number_entry = customtkinter.CTkEntry(master=frame_2, width=200, placeholder_text="Phone Number (09xxxxxxxxx)")
Phone_number_entry.place(x=280, y=150)

Address_entry = customtkinter.CTkEntry(master=frame_2, width=260, placeholder_text="Address")
Address_entry.place(x=48, y=220)

Password_entry = customtkinter.CTkEntry(master=frame_2, width=260, placeholder_text="Password", show="*")
Password_entry.place(x=48, y=280)
Password_shown_check = customtkinter.CTkCheckBox(master=frame_2, text="show password", command=show_password)
Password_shown_check.place(x=48, y=320)

# create register button
register_button = customtkinter.CTkButton(master=frame_2, text="Register", command=register_button_function)
register_button.place(relx=0.225, rely=0.85, anchor=tkinter.CENTER)

# create Menu
label1 = customtkinter.CTkLabel(master=frame_1, text="MENU", font=("Arial", 25, "bold"))
label1.place(x=25, y=35)

New_Account_Register_button = customtkinter.CTkButton(master=frame_1, text="New Account Register", font=("Century Gothic", 16))
New_Account_Register_button.place(x=25, y=90)

Update_Account_button = customtkinter.CTkButton(master=frame_1, text="Update User Account", font=("Century Gothic", 16), command=update_user_account)
Update_Account_button.place(x=25, y=125)

Search_Account_button = customtkinter.CTkButton(master=frame_1, text="Search User Account", font=("Century Gothic", 16), command=search_user_account)
Search_Account_button.place(x=25, y=160)

Display_Account_button = customtkinter.CTkButton(master=frame_1, text="Display User Account", font=("Century Gothic", 16), command=display_user_accounts)
Display_Account_button.place(x=25, y=195)

app.mainloop()
