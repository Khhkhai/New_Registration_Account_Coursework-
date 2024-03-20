import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox
from tkinter import messagebox as mb
from tkinter import ttk
from tkinter import filedialog
import csv
import re
import os.path
from PIL import Image, ImageTk
import string
import random
import datetime
import calendar
from captcha.image import ImageCaptcha
import PIL.ImageTk
from PIL import ImageDraw, ImageFont





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

# Store system user's email & password in csv file

# Check if the CSV file exists
if not os.path.isfile("user_accounts.csv"):
    # Create the CSV file and write the header row
    with open("user_accounts.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["User ID", "First Name", "Last Name", "Date Of Birth", "Phone Number", "Address", "Email", "Password", "Role", "Registration Date"])
        writer.writerow(["","","","","","","admin13@gmail.com","P@ssw0rd!", "System User", "",""])

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
        system_user_dashboard_function()


    # Function to direct to End User's Dashboard
    def forward_to_end_user_dashboard(user_email):
        Login_page.destroy()
        app.update()
        end_user_dashboard_function(user_email)


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
                stored_email, stored_password, user_type = row[6], row[7], row[8]

                if email == stored_email and password == stored_password:
                    if user_type == "End User":
                        # Display End User's Dashboard
                        forward_to_end_user_dashboard(Email_entry.get())

                    elif user_type == "System User":
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


    # Function to direct to End User's Dashboard
    def forward_to_end_user_dashboard():
        registration_page.destroy()
        app.update()
        end_user_dashboard_function()


    # Function to hide and show password
    def show_hide_password():
        if Password_entry.cget("show") == "*":
            Password_entry.configure(show="")
        else:
            Password_entry.configure(show="*")

    generated_user_ids = set()  # Set to store generated user IDs

    # generate unique id for new registered users
    def generate_user_id():
        while True:
            # Generate 2 random letters
            letters = ''.join(random.choice(string.ascii_uppercase) for _ in range(2))

            # Generate 4 random digits
            digits = ''.join(random.choice(string.digits) for _ in range(4))

            # Combine letters and digits to form the user ID
            user_id = f"{letters}{digits}"

            # Check if the generated user ID is unique
            if user_id not in generated_user_ids:
                generated_user_ids.add(user_id)
                return user_id

    # Length of CAPTCHA text
    CAPTCHA_LENGTH = 6 

    # Variable to track CAPTCHA validation status
    captcha_validated = False

    # Function to generate a random CAPTCHA text
    def generate_captcha_text():      
        captcha_characters = string.ascii_letters + string.digits
        captcha_challenge = ''.join(random.choice(captcha_characters) for _ in range(6))
        return captcha_challenge

    # Function to generate CAPTCHA image and return as a PIL Image
    def generate_captcha_image():
        captcha_obj = ImageCaptcha(height=100, width=250)
        captcha_text = generate_captcha_text()
        captcha_image = captcha_obj.generate(captcha_text)
        captcha_image = Image.open(captcha_image)
        return captcha_text, captcha_image

    # Function to update the CAPTCHA image on the GUI
    def update_captcha_image():
        captcha_text, captcha_image = generate_captcha_image()
        photo = ImageTk.PhotoImage(captcha_image)
        captcha_label.configure(image=photo)
        captcha_label.image = photo  # Keep a reference to avoid garbage collection

    # Function to validate CAPTCHA entered by the user
    def validate_captcha():
        global captcha_validated
        # Get the user's input from the entry widget
        entered_captcha = captcha_entry.get()

        # Compare the entered CAPTCHA with the generated one
        if entered_captcha == captcha_text:
            # If CAPTCHA is correct, set the validation status to True
            captcha_validated = True

            # Enable the register button
            register_button.configure(state="normal")
        else:
            # If CAPTCHA is incorrect, set the validation status to False
            captcha_validated = False
            # Show error message
            messagebox.showerror("Error", "Incorrect CAPTCHA. Please try again.")
            # Disable the register button
            register_button.configure(state="disabled")


    # Register Button Function
    def register_button_function():
        first_name = First_name_entry.get()
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
            # Generate a unique user ID
            user_id = generate_user_id()

            # Get the current date and time
            registration_date_time = datetime.datetime.now()

            # Check if the file exists
            file_exists = os.path.isfile("user_accounts.csv")

            # Save user data to CSV file
            with open("user_accounts.csv", "a", newline="") as csvfile:
                writer = csv.writer(csvfile)

                # Write header only if the file is empty
                if not file_exists:
                    writer.writerow(["User ID", "First Name", "Last Name", "Date Of Birth", "Phone Number", "Address", "Email", "Password", "Role", "Registration Date"])

                # Display the user's input information to doublecheck the entries
                message = (
                    f"User ID:    {user_id} \n"
                    f"First Name:    {first_name} \n"
                    f"Last Name:     {last_name} \n"
                    f"Date of Birth: {date_of_birth} \n"
                    f"Phone Number:  {phone_number} \n"
                    f"Address:       {address1 + '' + address2} \n"
                    f"Email:         {email} \n"
                )
                result = messagebox.askquestion("User Detail",
                                                "You are about to enter the following information \n" + message)
                # if user confirms, the data will be stored in the csv file
                if result == "yes":
                    writer.writerow([user_id, first_name, last_name, date_of_birth, phone_number, address1 + address2, email, password, "End User", registration_date_time])
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

            forward_to_login_page()

    # Create registration age
    registration_page = ctk.CTkFrame(master=app, width=550, height=600, corner_radius=15)
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

    First_name_label = ctk.CTkLabel(registration_page, text="First Name *", font=("Helvetica", 12))
    First_name_label.place(x=48, y=70)
    First_name_entry = ctk.CTkEntry(registration_page, width=200)
    First_name_entry.place(x=48, y=95)

    Last_name_label = ctk.CTkLabel(registration_page, text="Last Name *", font=("Helvetica", 12))
    Last_name_label.place(x=280, y=70)
    Last_name_entry = ctk.CTkEntry(registration_page, width=200)
    Last_name_entry.place(x=280, y=95)

    Date_of_birth_label = ctk.CTkLabel(registration_page, text="Date Of Birth (DD/MM/YYYY) *", font=("Helvetica", 12))
    Date_of_birth_label.place(x=48, y=130)
    Date_of_birth_entry = ctk.CTkEntry(registration_page, width=200)
    Date_of_birth_entry.place(x=48, y=155)

    Phone_number_label = ctk.CTkLabel(registration_page, text="Phone Number (09xxxxxxxxx) *", font=("Helvetica", 12))
    Phone_number_label.place(x=280, y=130)
    Phone_number_entry = ctk.CTkEntry(registration_page, width=200)
    Phone_number_entry.place(x=280, y=155)

    Address_label1 = ctk.CTkLabel(registration_page, text="Address 1 *", font=("Helvetica", 12))
    Address_label1.place(x=48, y=190)
    Address_entry1 = ctk.CTkEntry(registration_page, width=300)
    Address_entry1.place(x=48, y=215)

    Address_label2 = ctk.CTkLabel(registration_page, text="Address 2 *", font=("Helvetica", 12))
    Address_label2.place(x=48, y=250)
    Address_entry2 = ctk.CTkEntry(registration_page, width=300)
    Address_entry2.place(x=48, y=275)

    Email_label = ctk.CTkLabel(registration_page, text="Email *", font=("Helvetica", 12))
    Email_label.place(x=48, y=310)
    Email_entry = ctk.CTkEntry(registration_page, width=300)
    Email_entry.place(x=48, y=335)
    
    Password_label = ctk.CTkLabel(registration_page, text="Password (Min 8 chars, letter, digit, special char) *", font=("Helvetica", 12))
    Password_label.place(x=48, y=370)
    Password_entry = ctk.CTkEntry(registration_page, width=300)
    Password_entry.place(x=48, y=395)
    
   
    # Create a label and entry to enter the CAPTCHA 
    captcha_text_label = ctk.CTkLabel(registration_page, text='Enter CAPTCHA *', font=("Helvetica", 12))
    captcha_text_label.place(x=48, y=430)
    captcha_entry = ctk.CTkEntry(registration_page, width=150)
    captcha_entry.place(x=48, y=455)
    captcha_entry_button = ctk.CTkButton(registration_page, text="Submit", command=validate_captcha)
    captcha_entry_button.place(x=48, y=530)


    # Button to generate CAPTCHA
    Captcha_button = ctk.CTkButton(registration_page, text="Generate CAPTCHA", command=update_captcha_image)
    Captcha_button.place(x=48, y=490)
    
    # Label to display the CAPTCHA image
    captcha_label = ctk.CTkLabel(registration_page)  
    captcha_label.place(x=230, y=430)

    # create register button
    register_button = ctk.CTkButton(registration_page, text="Register", command=register_button_function,
                                    font=("Helvetica", 12, "bold"), state="disabled")
    register_button.place(x=300, y=530)  


def system_user_dashboard_function():

    # Function of home button in system user dashboard
    def system_user_home_button_function():
        home_page = ctk.CTkFrame(master=system_user_dashboard, width=550, height=600)
        home_page.place(x=150, y=0)
        
        def calculate_start_end_date_of_month():
            today = datetime.date.today()
            start_of_month = datetime.date(today.year, today.month, 1)
            end_of_month = datetime.date(today.year, today.month, calendar.monthrange(today.year, today.month)[1])
            return (start_of_month, end_of_month)
       
        # Function to calculate the new monthly registered users 
        def get_total_monthly_new_users():

            # Open the CSV file
            with open("user_accounts.csv", "r") as csvfile:
                reader = csv.reader(csvfile)
                next(reader)  # Skip the header row
                
                total_new_users = 0
                start_date, end_date = calculate_start_end_date_of_month()
                for row in reader:
                    if row[8] == "End User":  
                        registration_date = datetime.datetime.strptime(row[9], "%Y-%m-%d %H:%M:%S.%f").date()
                        # Check if the registration date falls within the current month
                        if start_date <= registration_date <= end_date:
                            total_new_users += 1
                return total_new_users


        # Function to calculate the total registered users
        def get_total_end_users():
            # Initialize a counter for total end users
            total_end_users = 0
            
            # Open the CSV file
            with open("user_accounts.csv", "r") as csvfile:
                reader = csv.reader(csvfile)
                next(reader)  # Skip the header row
                
                # Iterate through each row and increment the total_end_users counter for end users only
                for row in reader:
                    if row[8] == "End User":
                        total_end_users += 1
                return total_end_users


        # Function to display user accounts for a month
        def display_user_accounts_for_month():
            # Fetch the month from the box's tag
            month = canvas.gettags(monthly_new_users_box)[0]

            # Open the CSV file and read the data
            with open("user_accounts.csv", "r", newline="") as csvfile:
                reader = csv.reader(csvfile)
                next(reader)  # Skip the header row
                data = list(reader)
                start_date, end_date = calculate_start_end_date_of_month()

            # Filter the data for the specified month
            filtered_data = []
            for row in data:
                if row[8] != "System User":  # Skip if role is "System User"
                    if row[8] == "End User":  # Check if the role is "End User"
                        if row[9]:  # Check if registration date is not an empty string
                            registration_date = datetime.datetime.strptime(row[9], "%Y-%m-%d %H:%M:%S.%f").date()
                            if start_date <= registration_date <= end_date:
                                filtered_data.append([row[0], row[1], row[2], row[3], row[4], row[5] + row[6]])
            
            
            # Create a new window to display the user accounts
            display_window = ctk.CTkToplevel(home_page)
            display_window.title(f"User Accounts for {month}")
            display_window.geometry("800x400")
                        
                    
            # Display the filtered data in the existing frame
            if len(filtered_data) > 0:
                # Display the user accounts in a table format
                columns = ["User ID", "First Name", "Last Name", "Date of Birth", "Phone Number", "Address", "Email"]
                table = ttk.Treeview(display_window, columns=columns, show="headings")
                for col in columns:
                    table.heading(col, text=col)
                for row_data in filtered_data:
                    table.insert("", "end", values=row_data)
                table.pack(fill="both", expand=False)
            else:
                messagebox.showinfo("User Accounts", f"No user accounts found for {month}.")
                
        
        # Function to display all user accounts
        def display_all_user_accounts():
            # Open the CSV file and read the data
            with open("user_accounts.csv", "r", newline="") as csvfile:
                reader = csv.reader(csvfile)
                data = list(reader)

            # Filter out system users
            filtered_data = [row for row in data[1:] if row[8] != "System User"]
            
            
            # Create a new window to display the user accounts
            display_window = ctk.CTkToplevel(home_page)
            display_window.title("All User Accounts")
            display_window.geometry("800x400")
            display_window.resizable(False, False)

            # Display the data in a table format
            columns = ["User ID", "First Name", "Last Name", "Date of Birth", "Phone Number", "Address", "Email"]
            table = ttk.Treeview(display_window, columns=columns, show="headings")
            for col in columns:
                table.heading(col, text=col)
            for row_data in data[1:]:
                table.insert("", "end", values=row_data[:7])  # Display only the required columns
            table.pack(fill="both", expand=False)

        
        # Display the total number of new registered users
        def draw_rectangle_for_monthly_new_users(canvas):
            total_monthly_new_users = get_total_monthly_new_users()
            # Draw a rectangle
            global monthly_new_users_rectangle
            monthly_new_users_rectangle = canvas.create_rectangle(0, 0, 230, 60, fill="blue", tags=f"Total number of new registered users: {total_monthly_new_users}")
            canvas.create_text(110, 30, text=f"Monthly New Users: {total_monthly_new_users}", fill="white", font=("Helvetica", 12))
            canvas.tag_bind(monthly_new_users_rectangle, "<Button-1>", lambda event: display_user_accounts_for_month())

            
        # Display the total number of all registered users
        def draw_rectangle_for_total_end_users(canvas):
            total_end_users = get_total_end_users()
            # Draw a rectangle
            global total_users_rectangle
            total_users_rectangle = canvas.create_rectangle(250, 0, 500, 60, fill="blue", tags=f"Total number of registered users: {total_end_users}")
            canvas.create_text(375, 30, text=f"Total Registered Users: {total_end_users}", fill="white", font=("Helvetica", 12))
            canvas.tag_bind(total_users_rectangle, "<Button-1>", lambda event: display_all_user_accounts())

        welcome_label = ctk.CTkLabel(home_page, text="Welcome Admin!", font=("Helvetica", 35, "bold"))
        welcome_label.place(x=180, y=100)
        
        # Display default profile picture
        user_profile_pic = ctk.CTkImage(light_image=Image.open("user_profile_pic.jpg"), 
                                        dark_image=Image.open("user_profile_pic.jpg"), size=(105,105))
            
        # Create profile picture frame
        profile_picture_frame = ctk.CTkFrame(home_page, width=105, height=105, border_color="black", border_width=2)
        profile_picture_frame.place(x=30, y=50)

        # Create a label to display the profile picture
        profile_picture_label = ctk.CTkLabel(profile_picture_frame, image=user_profile_pic)
        profile_picture_label.pack(fill="both", expand=True)

        # Create a Canvas widget
        canvas = tk.Canvas(home_page, width=500, height=60, background="lightgray")
        canvas.place(x=100, y=300)
        draw_rectangle_for_monthly_new_users(canvas)
        draw_rectangle_for_total_end_users(canvas)

    # Function of search button in system user dashboard
    def system_user_search_button_function():
        search_page = ctk.CTkFrame(master=system_user_dashboard, width=550, height=600)
        search_page.place(x=150, y=0)
        
        def search_account():
            pass

        search_entry = ctk.CTkEntry(search_page, width=300)
        search_entry.place(x=48, y=90)
        
        # Search Criteria Combobox
        search_criteria_label = ctk.CTkLabel(search_page, text="Search Criteria:")
        search_criteria_label.place(x=350, y=90)
        search_criteria_combobox = ctk.CTkComboBox(search_page, values=["First Name", "Last Name", "User ID", "Email"])
        search_criteria_combobox.set("First Name")
        search_criteria_combobox.set("Last Name")
        search_criteria_combobox.set("User ID")
        search_criteria_combobox.set("Email")
        search_criteria_combobox.place(x=350, y=90)

        search_button = ctk.CTkButton(search_page, text="Search", command=search_account, font=("Helvetica", 12))
        search_button.place(x=150, y=120)


    # Function of delete account button in system user dashboard
    def system_user_delete_account_button_function():
        delete_page = ctk.CTkFrame(master=system_user_dashboard, width=550, height=600)
        delete_page.place(x=150, y=0)


    # Function of logout button in system user dashboard
    def system_user_logout_button_function():
        logout_page = ctk.CTkFrame(master=system_user_dashboard, width=550, height=600)
        logout_page.place(x=150, y=0)

        confirm = mb.askquestion("Logout", "Are you sure you want to logout?")
        if confirm == "yes":
            system_user_dashboard.destroy()
            app.update()
            Login_page_function()
        else:
            system_user_dashboard_function(user_email)




    # main frame of end user dashboard 
    system_user_dashboard = ctk.CTkFrame(master=app, width=700, height=600, border_color="black", border_width=1.5)
    system_user_dashboard.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    # menu frame of end user dashboard
    system_user_menu = ctk.CTkFrame(master=system_user_dashboard, width=150, height=600, border_color="black", border_width=1.5)
    system_user_menu.place(relx=0, rely=0)

    # Create funtion button for end user menu
    system_user_home_button = ctk.CTkButton(system_user_menu, text="Home", 
                                            command=system_user_home_button_function,
                                            font=("Helvetica", 12, "bold"))
    system_user_home_button.place(x=5, y=200)

    system_user_search_button = ctk.CTkButton(system_user_menu, text="Search", 
                                              command=system_user_search_button_function,
                                              font=("Helvetica", 12, "bold"))
    system_user_search_button.place(x=5, y=250)


    system_user_delete_account_button = ctk.CTkButton(system_user_menu, text="Delete Account", 
                                                      command=system_user_delete_account_button_function, 
                                                      font=("Helvetica", 12, "bold"))
    system_user_delete_account_button.place(x=5, y=300)


    system_user_logout_button = ctk.CTkButton(system_user_menu, text="Log Out", 
                                              command=system_user_logout_button_function,
                                              font=("Helvetica", 12, "bold"))
    system_user_logout_button.place(x=5, y=450)
    
    system_user_home_button_function()


# https://www.youtube.com/watch?v=kxo50SdrZMQ&t=35s to link with file and each user 
def end_user_dashboard_function(user_email):
    # Store references to the current page widgets
    current_page_widgets = []

    # Function to destroy widgets of the current page
    def destroy_current_page_widgets():
        for widget in current_page_widgets:
            widget.destroy()
        current_page_widgets.clear()
    
    
    # Forward to home page
    def navigate_to_home_page(user_email):
        destroy_current_page_widgets()
        app.update()
        end_user_home_button_function(user_email)

    # Forward to edit profile page
    def navigate_to_edit_profile_page(user_email):
        destroy_current_page_widgets()
        app.update()
        end_user_edit_button_function(user_email)

    # Forward to change password page
    def navigate_to_change_password_page(user_email):
        destroy_current_page_widgets()
        app.update()
        end_user_change_password_button_function(user_email)

    # Forward to logout page
    def navigate_to_logout_page(user_email):
        destroy_current_page_widgets()
        app.update()
        end_user_logout_button_function(user_email)


    # get user's information from ccsv file 
    def get_user_information(user_email):
        with open("user_accounts.csv", "r", newline="") as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # Skip the header row

            for row in reader:
                if row[6] == user_email and row[8] == "End User":
                    user_info = {
                        "User ID": row[0],
                        "First Name": row[1],
                        "Last Name": row[2],
                        "Date of Birth": row[3],
                        "Phone Number": row[4],
                        "Address": row[5],
                        "Email": row[6]
                    }
                    return user_info

        return None

    # Function to get the path of the user's profile picture
    def get_profile_picture_path(user_id):
        picture_directory = "user_pictures"
        file_extensions = [".png", ".jpg", ".jpeg"]  # Add more extensions if needed
        for ext in file_extensions:
            picture_path = os.path.join(picture_directory, f"{user_id}{ext}")
            if os.path.exists(picture_path):
                return picture_path
        return None


    # Function of home page button in end user dashboard
    def end_user_home_button_function(user_email):
        # create home page frame
        home_page = ctk.CTkFrame(master=end_user_dashboard, width=550, height=600)
        home_page.place(x=150, y=0)

        user_info = get_user_information(user_email)
        profile_picture_path = get_profile_picture_path(user_info['User ID'])

        # display all the information of user 
        if user_info: 
            # welcome statement
            welcome_label = ctk.CTkLabel(home_page, text=f"Welcome {user_info['Last Name']}!", font=("Helvetica", 35, "bold"))
            welcome_label.place(x=180, y=100)

            user_ID_label = ctk.CTkLabel(home_page, text=f"User ID: {user_info['User ID']}", font=("Helvetica", 20))
            user_ID_label.place(x=30, y=200)

            first_name_label = ctk.CTkLabel(home_page, text=f"First Name: {user_info['First Name']}", font=("Helvetica", 20))
            first_name_label.place(x=30, y=250)

            last_name_label = ctk.CTkLabel(home_page, text=f"Last Name: {user_info['Last Name']}", font=("Helvetica", 20))
            last_name_label.place(x=30, y=300)

            dob_label = ctk.CTkLabel(home_page, text=f"Date of Birth: {user_info['Date of Birth']}", font=("Helvetica", 20))
            dob_label.place(x=30, y=350)

            address_label = ctk.CTkLabel(home_page, text=f"Address: {user_info['Address']}", font=("Helvetica", 20))
            address_label.place(x=30, y=400)

            phone_number_label = ctk.CTkLabel(home_page, text=f"Phone Number: {user_info['Phone Number']}", font=("Helvetica", 20))
            phone_number_label.place(x=30, y=450)

            email_label = ctk.CTkLabel(home_page, text=f"Email: {user_info['Email']}", font=("Helvetica", 20))
            email_label.place(x=30, y=500)
        
            
        if profile_picture_path:
            # Display user's profile picture
            user_profile_pic = ctk.CTkImage(light_image=Image.open(profile_picture_path), 
                                            dark_image=Image.open(profile_picture_path), size=(105,105))
        else:
            # Display default profile picture
            user_profile_pic = ctk.CTkImage(light_image=Image.open("user_profile_pic.jpg"), 
                                            dark_image=Image.open("user_profile_pic.jpg"), size=(105,105))
            
        # Create profile picture frame
        profile_picture_frame = ctk.CTkFrame(home_page, width=105, height=105, border_color="black", border_width=2)
        profile_picture_frame.place(x=30, y=50)

        # Create a label to display the profile picture
        profile_picture_label = ctk.CTkLabel(profile_picture_frame, image=user_profile_pic)
        profile_picture_label.pack(fill="both", expand=True)
        

        

    # Function of edit button in end user dashboard
    def end_user_edit_button_function(user_email):
        # create edit profile page frame
        edit_profile_page = ctk.CTkFrame(master=end_user_dashboard, width=550, height=600)
        edit_profile_page.place(x=150, y=0)
        
        pic_path = tk.StringVar()
        pic_path.set("")
    

        user_info = get_user_information(user_email)
        profile_picture_path = get_profile_picture_path(user_info['User ID'])
        
        def done_button_function():
            first_name = First_name_entry.get()
            last_name = Last_name_entry.get()
            date_of_birth = Date_of_birth_entry.get()
            phone_number = Phone_number_entry.get()
            address1 = Address_entry1.get()
            address2 = Address_entry2.get()
            email = Email_entry.get()

            # Validation Check
            if not is_valid_date_of_birth(date_of_birth):
                messagebox.showinfo("Error", "Date Of Birth: Invalid Format")

            elif not is_valid_phone_number(phone_number):
                messagebox.showinfo("Error", "Invalid Phone Number")

            elif not is_valid_email(email):
                messagebox.showinfo("Error", "Invalid Email")

            else:

                # Check if the file exists
                file_exists = os.path.isfile("user_accounts.csv")

                # Save user data to CSV file
                with open("user_accounts.csv", "a", newline="") as csvfile:
                    writer = csv.writer(csvfile)

                    # Write header only if the file is empty
                    if not file_exists:
                        writer.writerow(["User ID", "First Name", "Last Name", "Date Of Birth", "Phone Number", "Address", "Email", "Password", "Role", "Registration Date"])

                    # Display the user's input information to doublecheck the entries
                    message = (
                        f"User ID:    {user_id} \n"
                        f"First Name:    {first_name} \n"
                        f"Last Name:     {last_name} \n"
                        f"Date of Birth: {date_of_birth} \n"
                        f"Phone Number:  {phone_number} \n"
                        f"Address:       {address1 + '' + address2} \n"
                        f"Email:         {email} \n"
                    )
                    result = messagebox.askquestion("User Detail",
                                                    "You are about to enter the following information \n" + message)
                    # if user confirms, the data will be stored in the csv file
                    if result == "yes":
                        writer.writerow([user_id, first_name, last_name, date_of_birth, phone_number, address1 + address2, email, password, "End User", registration_date_time])
                        messagebox.showinfo("Info", message="Your information has been successfully updated", icon="info")
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



        def handle_picture_upload(user_id):
            # Open file dialog to select picture
            file_path = filedialog.askopenfilename()

            if file_path:
                _, file_extension = os.path.splitext(file_path)
                # Validate file type
                if file_extension.lower() not in ['.jpg', '.jpeg', '.png']:
                    print("Invalid file type. Please upload a JPG or PNG file.")
                    return

                # Create directory if it doesn't exist
                picture_directory = "user_pictures"
                if not os.path.exists(picture_directory):
                    os.makedirs(picture_directory)

                # Check if a picture with the same user ID already exists
                existing_picture_path = os.path.join(picture_directory, f"{user_id}{file_extension}")
                if os.path.exists(existing_picture_path):
                    os.remove(existing_picture_path)  # Delete the existing picture

                new_file_name = f"{user_id}{file_extension}"
                new_file_path = os.path.join(picture_directory, new_file_name)
                os.rename(file_path, new_file_path)
                # Open the uploaded image and resize it
                img = Image.open(new_file_path).resize((105, 105))
                # Convert the image to Tkinter PhotoImage format
                photo = ImageTk.PhotoImage(img)
                # Configure the button with the uploaded image
                profile_picture_button.configure(image=photo)
                profile_picture_button.image = photo


        # Create profile picture frame
        profile_picture = ctk.CTkFrame(edit_profile_page, width=105, height=105, border_color="black", border_width=2)
        profile_picture.place(x=40, y=30)

        # Check if profile picture path exists and create appropriate image
        if profile_picture_path:
            user_profile_pic = ctk.CTkImage(light_image=Image.open(profile_picture_path), 
                                            dark_image=Image.open(profile_picture_path), size=(105, 105))
        else:
            # Display default profile picture if path doesn't exist
            user_profile_pic = ctk.CTkImage(light_image=Image.open("user_profile_pic.jpg"), 
                                            dark_image=Image.open("user_profile_pic.jpg"), size=(105, 105))

        # Create profile picture button
        profile_picture_button = ctk.CTkButton(profile_picture, image=user_profile_pic, text="",
                                                fg_color="lightgray", anchor="center", width=100,
                                                border_spacing=0, border_width=0, hover_color="lightgray",
                                                command=lambda: handle_picture_upload(user_info['User ID']))
        profile_picture_button.pack()



        # Create labels and entry boxes
        user_ID_label = ctk.CTkLabel(edit_profile_page, text=f"User ID: {user_info['User ID']}", font=("Helvetica", 20))
        user_ID_label.place(x=200, y=70)

        First_name_label = ctk.CTkLabel(edit_profile_page, text="First Name *", font=("Helvetica", 16))
        First_name_label.place(x=40, y=150)
        First_name_entry = ctk.CTkEntry(edit_profile_page, width=230)
        First_name_entry.place(x=40, y=175)

        Last_name_label = ctk.CTkLabel(edit_profile_page, text="Last Name *", font=("Helvetica", 16))
        Last_name_label.place(x=280, y=150)
        Last_name_entry = ctk.CTkEntry(edit_profile_page, width=230)
        Last_name_entry.place(x=280, y=175)

        Date_of_birth_label = ctk.CTkLabel(edit_profile_page, text="Date Of Birth (DD/MM/YYYY) *", font=("Helvetica", 16))
        Date_of_birth_label.place(x=40, y=210)
        Date_of_birth_entry = ctk.CTkEntry(edit_profile_page, width=230)
        Date_of_birth_entry.place(x=40, y=235)

        Phone_number_label = ctk.CTkLabel(edit_profile_page, text="Phone Number (09xxxxxxxxx) *", font=("Helvetica", 16))
        Phone_number_label.place(x=280, y=210)
        Phone_number_entry = ctk.CTkEntry(edit_profile_page, width=230)
        Phone_number_entry.place(x=280, y=235)

        Address_label1 = ctk.CTkLabel(edit_profile_page, text="Address 1 *", font=("Helvetica", 16))
        Address_label1.place(x=40, y=270)
        Address_entry1 = ctk.CTkEntry(edit_profile_page, width=330)
        Address_entry1.place(x=40, y=295)

        Address_label2 = ctk.CTkLabel(edit_profile_page, text="Address 2 *", font=("Helvetica", 16))
        Address_label2.place(x=40, y=330)
        Address_entry2 = ctk.CTkEntry(edit_profile_page, width=330)
        Address_entry2.place(x=40, y=355)

        Email_label = ctk.CTkLabel(edit_profile_page, text="Email *", font=("Helvetica", 16))
        Email_label.place(x=40, y=390)
        Email_entry = ctk.CTkEntry(edit_profile_page, width=330)
        Email_entry.place(x=40, y=415)

        # Create function button for end user menu
        done_button = ctk.CTkButton(edit_profile_page, text="Done", command=done_button_function,
                                    font=("Helvetica", 12, "bold"))
        done_button.place(x=40, y=500)

        

    # Function of change password button in end user dashboard
    def end_user_change_password_button_function(user_email):

        # Function to hide and show password
        def show_hide_password(password):
            if password.cget("show") == "*":
                password.configure(show="")
            else:
                password.configure(show="*")

        def confirm_button(): #####3
            pass


        # creating change password page
        change_button_page = ctk.CTkFrame(master=end_user_dashboard, width=550, height=600)
        change_button_page.place(x=150, y=0)

        # creating current password label and entry box
        current_password_label = ctk.CTkLabel(change_button_page, text="Your Current Password", font=("Helvetica", 20, "bold"))
        current_password_label.place(x=120, y=80)

        current_password_entry = ctk.CTkEntry(change_button_page, width=300, show="*")
        current_password_entry.place(x=80, y=130)

        current_password_shown_check = ctk.CTkCheckBox(change_button_page, text="Show Password", 
                                        command=lambda:show_hide_password(current_password_entry),
                                        font=("Helvetica", 8))
        current_password_shown_check.place(x=400, y=130)


        # creating new password label and entry box
        new_password_label = ctk.CTkLabel(change_button_page, text="Your New Password", font=("Helvetica", 20, "bold"))
        new_password_label.place(x=120, y=190)

        new_password_entry = ctk.CTkEntry(change_button_page, width=300, show="*")
        new_password_entry.place(x=80, y=240)

        new_password_shown_check = ctk.CTkCheckBox(change_button_page, text="Show Password", 
                                        command=lambda:show_hide_password(new_password_entry), 
                                        font=("Helvetica", 8))
        new_password_shown_check.place(x=400, y=240)


        # creating confirm new password label and entry box
        confirm_new_password_label = ctk.CTkLabel(change_button_page, text="Confirm New Password", font=("Helvetica", 20, "bold"))
        confirm_new_password_label.place(x=120, y=300)

        confirm_new_password_entry = ctk.CTkEntry(change_button_page, width=300, show="*")
        confirm_new_password_entry.place(x=80, y=340)

        confirm_password_shown_check = ctk.CTkCheckBox(change_button_page, text="Show Password", 
                                        command=lambda:show_hide_password(confirm_new_password_entry),
                                        font=("Helvetica", 8))
        confirm_password_shown_check.place(x=400, y=340)     


        # create register button
        confirm_button = ctk.CTkButton(change_button_page, text="Confirm", command=confirm_button,
                                        font=("Helvetica", 12, "bold"))
        confirm_button.place(x=150, y=450)   

        

    # Function of logout button in end user dashboard
    def end_user_logout_button_function(user_email):
        logout_page = ctk.CTkFrame(master=end_user_dashboard, width=550, height=600)
        logout_page.place(x=150, y=0)

        confirm = mb.askquestion("Logout", "Are you sure you want to logout?")
        if confirm == "yes":
            end_user_dashboard.destroy()
            app.update()
            Login_page_function()
        else:
            end_user_dashboard_function(user_email)


    
    # main frame of end user dashboard 
    end_user_dashboard = ctk.CTkFrame(master=app, width=700, height=600, border_color="black", border_width=1.5)
    end_user_dashboard.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    # menu frame of end user dashboard
    end_user_menu = ctk.CTkFrame(master=end_user_dashboard, width=150, height=600, border_color="black", border_width=1.5)
    end_user_menu.place(relx=0, rely=0)

    # Create funtion button for end user menu
    end_user_home_button = ctk.CTkButton(end_user_menu, text="Home", 
                                         command=lambda: navigate_to_home_page(user_email),
                                        font=("Helvetica", 12, "bold"))
    end_user_home_button.place(x=5, y=200)


    end_user_edit_button = ctk.CTkButton(end_user_menu, text="Edit Profile", 
                                         command=lambda: navigate_to_edit_profile_page(user_email),
                                        font=("Helvetica", 12, "bold"))
    end_user_edit_button.place(x=5, y=250)


    end_user_change_password_button = ctk.CTkButton(end_user_menu, text="Change Password", 
                                                    command=lambda: navigate_to_change_password_page(user_email),
                                                    font=("Helvetica", 12, "bold"))
    end_user_change_password_button.place(x=5, y=300)


    end_user_logout_button = ctk.CTkButton(end_user_menu, text="Logout", 
                                           command=lambda: navigate_to_logout_page(user_email),
                                            font=("Helvetica", 12, "bold"))
    end_user_logout_button.place(x=5, y=450)

    end_user_edit_button_function(user_email)



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

"""      
    def generate_captcha_text():      
        captcha_characters = string.ascii_letters + string.digits
        captcha_challenge = ''.join(random.choice(captcha_characters) for _ in range(6))
        return captcha_challenge

    def generate_captcha():
        global img
        captcha_obj = ImageCaptcha(height=150, width=250)
        captcha_obj.write(chars=generate_captcha_text(), putput= "_captcha.png")
        img =  PhotoImage(_file="_captcha.png")
        captcha_image.configure(image=img)
"""