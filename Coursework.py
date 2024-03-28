import csv
import calendar
import datetime
import os.path
import random
import re
import string

import customtkinter as ctk
from tkinter import filedialog, messagebox, ttk
from tkinter import messagebox as mb
import tkinter as tk
from PIL import Image, ImageDraw, ImageFont, ImageTk
from captcha.image import ImageCaptcha
from tkcalendar import DateEntry




# create the desktop window
app = ctk.CTk()

# set the dimension to the window
app.geometry("700x600")

# set the dimension of the window to be permanent
app.resizable(False, False)

# set the title of window
app.title("User Account Registration System")

# Set the background color
app.configure(bg="light grey")

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


# Function to check if the date of birth is today's date
def is_today_date_of_birth(date_of_birth):
    # Get today's date
    today = datetime.date.today()
    
    # Convert the date_of_birth string to a datetime object
    date_of_birth = datetime.datetime.strptime(date_of_birth, "%m/%d/%y").date()
    
    # Check if the date of birth is the same as today's date
    return date_of_birth == today


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


# Login window
def Login_page_function():
    # Function to direct to Registration Page
    def forward_to_registration_page():
        Login_page.destroy()
        app.update()
        registration_page_function()


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
    Login_page = ctk.CTkFrame(master=app, width=300, height=400, corner_radius=15, fg_color="#DDDDDD")
    Login_page.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    # Create labels and entry widgets for login page
    Login_label_1 = ctk.CTkLabel(master=Login_page, text="Login", font=(font_style, 30, "bold"))
    Login_label_1.place(x=30, y=40)

    Email_entry = ctk.CTkEntry(master=Login_page, width=260, placeholder_text="Email", font=(font_style, 11))
    Email_entry.place(x=20, y=110)

    Password_entry = ctk.CTkEntry(master=Login_page, width=260, placeholder_text="Password", show="*", font=(font_style, 11))
    Password_entry.place(x=20, y=160)
    Password_shown_check = ctk.CTkCheckBox(master=Login_page, text="Show Password", command=show_hide_password, font=(font_style, 11))
    Password_shown_check.place(x=20, y=200)
    Password_shown_check.configure(checkbox_width=15, checkbox_height=15, border_width=3)
    # Create login button
    login_button = ctk.CTkButton(master=Login_page, text="Sign In", command=login_button_function, width=260,
                                font=(font_style, 12))
    login_button.place(x=20, y=250)

    # Create a link to register page
    register_label = ctk.CTkLabel(master=Login_page, text="Doesn't have an account? Register", font=(font_style, 10), cursor="hand2")
    register_label.place(x=70, y=280)

    # Bind the label to the registration window function
    register_label.bind("<Button-1>", lambda event: forward_to_registration_page())


# Register window
def registration_page_function():
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
        global captcha_text
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

        elif not is_valid_phone_number(phone_number):
            messagebox.showinfo("Error", "Invalid Phone Number")
            
        elif is_today_date_of_birth(date_of_birth):
            messagebox.showinfo("Error", "Date of birth cannot be today's date")
            
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
    backward_button = ctk.CTkButton(registration_page, text="←", font=(font_style, 10, "bold"), 
                                text_color= "black", fg_color="lightgray", hover_color="lightgray", width=3, command=forward_to_login_page)
    backward_button.place(x=10, y=35)

    # Create labels and entry widgets for registration
    Register_label_1 = ctk.CTkLabel(registration_page, text="REGISTER HERE", font=(font_style, 20, "bold"))
    Register_label_1.place(x=45, y=35)

    # Set the scope of Varibles globally
    global First_name_entry, Last_name_entry, Date_of_birth_entry, Phone_number_entry, Address_entry1, Address_entry2, Email_entry, Password_entry

    First_name_label = ctk.CTkLabel(registration_page, text="First Name *", font=(font_style, 12))
    First_name_label.place(x=48, y=70)
    First_name_entry = ctk.CTkEntry(registration_page, width=200)
    First_name_entry.place(x=48, y=95)

    Last_name_label = ctk.CTkLabel(registration_page, text="Last Name *", font=(font_style, 12))
    Last_name_label.place(x=280, y=70)
    Last_name_entry = ctk.CTkEntry(registration_page, width=200)
    Last_name_entry.place(x=280, y=95)

    Date_of_birth_label = ctk.CTkLabel(registration_page, text="Date Of Birth (DD/MM/YYYY) *", font=(font_style, 12))
    Date_of_birth_label.place(x=48, y=130)
    Date_of_birth_entry = DateEntry(registration_page, width=30, background='darkblue',
                                    foreground='white', borderwidth=2)

    Date_of_birth_entry.place(x=70, y=250)

    Phone_number_label = ctk.CTkLabel(registration_page, text="Phone Number (09xxxxxxxxx) *", font=(font_style, 12))
    Phone_number_label.place(x=280, y=130)
    Phone_number_entry = ctk.CTkEntry(registration_page, width=200)
    Phone_number_entry.place(x=280, y=155)

    Address_label1 = ctk.CTkLabel(registration_page, text="Address 1 *", font=(font_style, 12))
    Address_label1.place(x=48, y=190)
    Address_entry1 = ctk.CTkEntry(registration_page, width=300)
    Address_entry1.place(x=48, y=215)

    Address_label2 = ctk.CTkLabel(registration_page, text="Address 2 *", font=(font_style, 12))
    Address_label2.place(x=48, y=250)
    Address_entry2 = ctk.CTkEntry(registration_page, width=300)
    Address_entry2.place(x=48, y=275)

    Email_label = ctk.CTkLabel(registration_page, text="Email *", font=(font_style, 12))
    Email_label.place(x=48, y=310)
    Email_entry = ctk.CTkEntry(registration_page, width=300)
    Email_entry.place(x=48, y=335)
    
    Password_label = ctk.CTkLabel(registration_page, text="Password (Min 8 chars, letter, digit, special char) *", font=(font_style, 12))
    Password_label.place(x=48, y=370)
    Password_entry = ctk.CTkEntry(registration_page, width=300)
    Password_entry.place(x=48, y=395)
    
   
    # Create a label and entry to enter the CAPTCHA 
    captcha_text_label = ctk.CTkLabel(registration_page, text='Enter CAPTCHA *', font=(font_style, 12))
    captcha_text_label.place(x=48, y=430)
    
    captcha_entry = ctk.CTkEntry(registration_page, width=150)
    captcha_entry.place(x=48, y=455)
    
    # Bind the <FocusIn> event to the captcha_entry widget
    captcha_entry.bind("<FocusIn>", lambda event: update_captcha_image())
    
    captcha_entry_button = ctk.CTkButton(registration_page, text="Submit", command=validate_captcha)
    captcha_entry_button.place(x=48, y=490)
    
    
    # Label to display the CAPTCHA image
    captcha_label = ctk.CTkLabel(registration_page)  
    captcha_label.place(x=230, y=430)

    # create register button
    register_button = ctk.CTkButton(registration_page, text="Register", command=register_button_function,
                                    font=(font_style, 12, "bold"), state="disabled")
    register_button.place(x=48, y=530)  


# System User Dashboard window
def system_user_dashboard_function():
    
    # Store references to the current page widgets
    current_page_widgets = []

    # Function to destroy widgets of the current page
    def destroy_current_page_widgets():
        for widget in current_page_widgets:
            widget.destroy()
        current_page_widgets.clear()
    
    
    # Forward to home page
    def navigate_to_home_page():
        destroy_current_page_widgets()
        app.update()
        system_user_home_button_function()


    # Forward to search page
    def navigate_to_search_page():
        destroy_current_page_widgets()
        app.update()
        system_user_search_button_function()


    # Forward to change password page
    def navigate_to_delete_account_page():
        destroy_current_page_widgets()
        app.update()
        system_user_delete_account_button_function()


    # Forward to logout page
    def navigate_to_logout_page():
        destroy_current_page_widgets()
        app.update()
        system_user_logout_button_function()


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
            month = canvas_for_monthly_new_users.gettags(monthly_new_users_rectangle)[0]

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
                                filtered_data.append([row[0], row[1], row[2], row[3], row[4], row[5] , row[6]])
            
            
            # Create a new window to display the user accounts
            display_window = ctk.CTkToplevel(home_page)
            display_window.title(f"User Accounts for {month}")
            display_window.geometry("1300x400")
                        
                    
            # Display the filtered data in the existing frame
            if len(filtered_data) > 0:
                # Display the user accounts in a table format
                columns = ["User ID", "First Name", "Last Name", "Date of Birth", "Phone Number", "Address", "Email"]
                table = ttk.Treeview(display_window, columns=columns, show="headings")
                for col in columns:
                    table.heading(col, text=col)
                for row_data in filtered_data:
                    table.insert("", "end", values=row_data)
                table.pack(fill="both", expand=True)
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
            display_window.geometry("1300x400")
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
        def draw_rectangle_for_monthly_new_users(canvas_for_monthly_new_users):
            total_monthly_new_users = get_total_monthly_new_users()
            # Draw a rectangle
            global monthly_new_users_rectangle
            monthly_new_users_rectangle = canvas_for_monthly_new_users.create_rectangle(0, 0, 230, 60, fill="blue", tags=f"Total number of new registered users: {total_monthly_new_users}")
            canvas_for_monthly_new_users.create_text(110, 30, text=f"Monthly New Users: {total_monthly_new_users}", fill="white", font=("Helvetica", 12))
            canvas_for_monthly_new_users.tag_bind(monthly_new_users_rectangle, "<Button-1>", lambda event: display_user_accounts_for_month())

            
        # Display the total number of all registered users
        def draw_rectangle_for_total_end_users(canvas_for_total_end_users):
            total_end_users = get_total_end_users()
            # Draw a rectangle
            global total_users_rectangle
            total_users_rectangle = canvas_for_total_end_users.create_rectangle(0, 0, 250, 60, fill="#3D4633", tags=f"Total number of registered users: {total_end_users}")
            canvas_for_total_end_users.create_text(125, 30, text=f"Total Registered Users: {total_end_users}", fill="white", font=("Helvetica", 12))
            canvas_for_total_end_users.tag_bind(total_users_rectangle, "<Button-1>", lambda event: display_all_user_accounts())

        welcome_label = ctk.CTkLabel(home_page, text="Welcome Admin!", font=(font_style, 35, "bold"))
        welcome_label.place(x=180, y=100)
        
        # Display default profile picture
        user_profile_pic = ctk.CTkImage(light_image=Image.open("system_user_profile_pic.jpg"), 
                                        dark_image=Image.open("system_user_profile_pic.jpg"), size=(105,105))
            
        # Create profile picture frame
        profile_picture_frame = ctk.CTkFrame(home_page, width=105, height=105, border_color="black", border_width=2)
        profile_picture_frame.place(x=30, y=50)

        # Create a label to display the profile picture
        profile_picture_label = ctk.CTkLabel(profile_picture_frame, image=user_profile_pic, text="")
        profile_picture_label.pack(fill="both", expand=True)

        # Create a Canvas widget
        canvas_for_monthly_new_users = tk.Canvas(home_page, width=230, height=60, background="lightgray")
        canvas_for_monthly_new_users.place(x=100, y=300)
        canvas_for_total_end_users = tk.Canvas(home_page, width=250, height=60, background="lightgray")
        canvas_for_total_end_users.place(x=450, y=300)
        draw_rectangle_for_monthly_new_users(canvas_for_monthly_new_users)
        draw_rectangle_for_total_end_users(canvas_for_total_end_users)


    # Function of search button in system user dashboard
    def system_user_search_button_function():
        search_page = ctk.CTkFrame(master=system_user_dashboard, width=550, height=600)
        search_page.place(x=150, y=0)
                
        def search_account():
            # Get the search query from the entry field
            search_query = search_entry.get()

            # Get the selected search criteria from the combobox
            search_criteria = search_criteria_combobox.get()

            # Open the CSV file and read the data
            with open("user_accounts.csv", "r", newline="") as csvfile:
                reader = csv.reader(csvfile)
                next(reader)  # Skip the header row

                # Filter the data based on the search criteria and query
                filtered_data = []
                for row in reader:
                    # Check if the search query matches the data in the selected criteria
                    if search_criteria == "First Name" and row[1].lower() == search_query.lower():
                        filtered_data.append(row)
                    elif search_criteria == "Last Name" and row[2].lower() == search_query.lower():
                        filtered_data.append(row)
                    elif search_criteria == "User ID" and row[0].lower() == search_query.lower():
                        filtered_data.append(row)
                    elif search_criteria == "Email" and row[6].lower() == search_query.lower():
                        filtered_data.append(row)

            # Display the filtered data
            if filtered_data:
                display_search_results(filtered_data)
            else:
                messagebox.showinfo("Search Results", "No matching accounts found.")

        def display_search_results(data):
            # Create a new window to display the search results
            search_results_window = ctk.CTkToplevel(search_page)
            search_results_window.title("Search Results")
            search_results_window.geometry("1300x400")
            search_results_window.resizable(False, False)

            # Display the data in a table format
            columns = ["User ID", "First Name", "Last Name", "Date of Birth", "Phone Number", "Address", "Email"]
            table = ttk.Treeview(search_results_window, columns=columns, show="headings")
            for col in columns:
                table.heading(col, text=col)
            for row_data in data:
                table.insert("", "end", values=row_data)
            table.pack(fill="both", expand=False)

        search_entry = ctk.CTkEntry(search_page, width=300)
        search_entry.place(x=48, y=90)
        
        # Search Criteria Combobox
        search_criteria_label = ctk.CTkLabel(search_page, text="Find by:", font=(font_style, 14))
        search_criteria_label.place(x=350, y=60)
        search_criteria_combobox = ctk.CTkComboBox(search_page, values=["First Name", "Last Name", "User ID", "Email"])
        search_criteria_combobox.set("First Name")
        search_criteria_combobox.set("Last Name")
        search_criteria_combobox.set("User ID")
        search_criteria_combobox.set("Email")
        search_criteria_combobox.place(x=350, y=90)

        search_button = ctk.CTkButton(search_page, text="Search", command=search_account, font=(font_style, 12))
        search_button.place(x=150, y=120)

    # Function of delete account button in system user dashboard
    def system_user_delete_account_button_function():
        delete_page = ctk.CTkFrame(master=system_user_dashboard, width=550, height=600)
        delete_page.place(x=150, y=0)
        
        search_user_ID_label = ctk.CTkLabel(delete_page, text="Find by: User ID", font=(font_style, 15))
        search_user_ID_label.place(x=100, y=60)
               
        search_user_ID_entry = ctk.CTkEntry(delete_page, width=300)
        search_user_ID_entry.place(x=100, y=100)

        search_button = ctk.CTkButton(delete_page, text="Search", 
                                      command=lambda: delete_account(search_user_ID_entry.get()), 
                                      font=(font_style, 12))
        search_button.place(x=175, y=140)


    def delete_account(user_id):
        # Read the user's information from the CSV file
        with open("user_accounts.csv", "r") as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if row[0] == user_id:
                    # Display user information in a dialog box
                    info_message = f"User ID: {row[0]}\n" \
                                f"First Name: {row[1]}\n" \
                                f"Last Name: {row[2]}\n" \
                                f"Date of Birth: {row[3]}\n" \
                                f"Phone Number: {row[4]}\n" \
                                f"Address: {row[5]}\n" \
                                f"Email: {row[6]}"
                    confirmation = messagebox.askyesno("Confirmation", f"Do you want to delete this account?\n\n{info_message}")
                    if confirmation:
                        # Read the existing data from the CSV file
                        with open("user_accounts.csv", "r") as csvfile:
                            reader = csv.reader(csvfile)
                            data = list(reader)

                        # Find the index of the row to delete
                        index_to_delete = None
                        for i, row in enumerate(data):
                            if row[0] == user_id:  # Assuming user ID is in the first column
                                index_to_delete = i
                                break

                        if index_to_delete is not None:
                            # Remove the row from the data list
                            del data[index_to_delete]

                            # Write the updated data back to the CSV file
                            with open("user_accounts.csv", "w", newline="") as csvfile:
                                writer = csv.writer(csvfile)
                                writer.writerows(data)

                            messagebox.showinfo("Success", f"Account with User ID {user_id} has been deleted.")
                        else:
                            messagebox.showerror("Error", f"Account with User ID {user_id} not found.")
                    break
            else:
                messagebox.showerror("Error", f"Account with User ID {user_id} not found.")


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
            system_user_dashboard_function()


    # main frame of end user dashboard 
    system_user_dashboard = ctk.CTkFrame(master=app, width=700, height=600, border_color="black", border_width=1.5)
    system_user_dashboard.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    # menu frame of end user dashboard
    system_user_menu = ctk.CTkFrame(master=system_user_dashboard, width=150, height=600, border_color="black", border_width=1.5)
    system_user_menu.place(relx=0, rely=0)

    # Create funtion button for end user menu
    system_user_home_button = ctk.CTkButton(system_user_menu, text="Home", 
                                            command=navigate_to_home_page,
                                            font=(font_style, 12))
    system_user_home_button.place(x=5, y=150)

    system_user_search_button = ctk.CTkButton(system_user_menu, text="Search", 
                                              command=navigate_to_search_page,
                                              font=(font_style, 12))
    system_user_search_button.place(x=5, y=190)


    system_user_delete_account_button = ctk.CTkButton(system_user_menu, text="Delete Account", 
                                                      command=navigate_to_delete_account_page, 
                                                      font=(font_style, 12))
    system_user_delete_account_button.place(x=5, y=230)


    system_user_logout_button = ctk.CTkButton(system_user_menu, text="Log Out", 
                                              command=navigate_to_logout_page,
                                              font=(font_style, 12))
    system_user_logout_button.place(x=5, y=500)
    
    system_user_home_button_function()


# End User Dashboard window
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
            welcome_label = ctk.CTkLabel(home_page, text=f"Welcome {user_info['Last Name']}!", font=(font_style, 35, "bold"))
            welcome_label.place(x=180, y=100)

            user_ID_label = ctk.CTkLabel(home_page, text=f"User ID: {user_info['User ID']}", font=(font_style, 20))
            user_ID_label.place(x=30, y=200)

            first_name_label = ctk.CTkLabel(home_page, text=f"First Name: {user_info['First Name']}", font=(font_style, 20))
            first_name_label.place(x=30, y=250)

            last_name_label = ctk.CTkLabel(home_page, text=f"Last Name: {user_info['Last Name']}", font=(font_style, 20))
            last_name_label.place(x=30, y=300)

            dob_label = ctk.CTkLabel(home_page, text=f"Date of Birth: {user_info['Date of Birth']}", font=(font_style, 20))
            dob_label.place(x=30, y=350)

            address_label = ctk.CTkLabel(home_page, text=f"Address: {user_info['Address']}", font=(font_style, 20))
            address_label.place(x=30, y=400)

            phone_number_label = ctk.CTkLabel(home_page, text=f"Phone Number: {user_info['Phone Number']}", font=(font_style, 20))
            phone_number_label.place(x=30, y=450)

            email_label = ctk.CTkLabel(home_page, text=f"Email: {user_info['Email']}", font=(font_style, 20))
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
        profile_picture_label = ctk.CTkLabel(profile_picture_frame, image=user_profile_pic, text="")
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
        
        def change_button_function():
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
                if file_extension.lower() not in [".jpg", ".png"]:
                    print("Invalid file type. Please upload a JPG file.")
                    return

                # Create directory if it doesn't exist
                picture_directory = "user_pictures"
                if not os.path.exists(picture_directory):
                    os.makedirs(picture_directory)

                # Check if a picture with the same user ID already exists
                existing_picture_path = os.path.join(picture_directory, f"{user_id}{file_extension}")
                print(existing_picture_path)
                if os.path.exists(existing_picture_path):
                    print(existing_picture_path)

                    os.replace(existing_picture_path)  # Delete the existing picture

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
        user_ID_label = ctk.CTkLabel(edit_profile_page, text=f"User ID: {user_info['User ID']}", font=("Aptos SemiBold", 23))
        user_ID_label.place(x=200, y=70)

        First_name_label = ctk.CTkLabel(edit_profile_page, text="First Name *", font=(font_style, 16))
        First_name_label.place(x=40, y=150)
        First_name_entry = ctk.CTkEntry(edit_profile_page, width=230)
        First_name_entry.place(x=40, y=175)

        Last_name_label = ctk.CTkLabel(edit_profile_page, text="Last Name *", font=(font_style, 16))
        Last_name_label.place(x=280, y=150)
        Last_name_entry = ctk.CTkEntry(edit_profile_page, width=230)
        Last_name_entry.place(x=280, y=175)

        Date_of_birth_label = ctk.CTkLabel(edit_profile_page, text="Date Of Birth (DD/MM/YYYY) *", font=(font_style, 16))
        Date_of_birth_label.place(x=40, y=210)
        Date_of_birth_entry = ctk.CTkEntry(edit_profile_page, width=230)
        Date_of_birth_entry.place(x=40, y=235)

        Phone_number_label = ctk.CTkLabel(edit_profile_page, text="Phone Number (09xxxxxxxxx) *", font=(font_style, 16))
        Phone_number_label.place(x=280, y=210)
        Phone_number_entry = ctk.CTkEntry(edit_profile_page, width=230)
        Phone_number_entry.place(x=280, y=235)

        Address_label1 = ctk.CTkLabel(edit_profile_page, text="Address 1 *", font=(font_style, 16))
        Address_label1.place(x=40, y=270)
        Address_entry1 = ctk.CTkEntry(edit_profile_page, width=330)
        Address_entry1.place(x=40, y=295)

        Address_label2 = ctk.CTkLabel(edit_profile_page, text="Address 2 *", font=(font_style, 16))
        Address_label2.place(x=40, y=330)
        Address_entry2 = ctk.CTkEntry(edit_profile_page, width=330)
        Address_entry2.place(x=40, y=355)

        Email_label = ctk.CTkLabel(edit_profile_page, text="Email *", font=(font_style, 16))
        Email_label.place(x=40, y=390)
        Email_entry = ctk.CTkEntry(edit_profile_page, width=330)
        Email_entry.place(x=40, y=415)

        # Create function button for end user menu
        change_button = ctk.CTkButton(edit_profile_page, text="Done", command=change_button_function,
                                    font=(font_style, 12))
        change_button.place(x=40, y=500)

        
    # Function of change password button in end user dashboard
    def end_user_change_password_button_function(user_email):

        # Function to hide and show password
        def show_hide_password(password):
            if password.cget("show") == "*":
                password.configure(show="")
            else:
                password.configure(show="*")

        # Function to validate and amend password
        def confirm_button(): 
            # Get the values from entry boxes
            current_password = current_password_entry.get()
            new_password = new_password_entry.get()
            confirm_new_password = confirm_new_password_entry.get()

            # Read the CSV file and find the user's entry
            with open("user_accounts.csv", "r") as csvfile:
                reader = csv.reader(csvfile)
                rows = list(reader)

            user_index = None
            for i, row in enumerate(rows):
                if row[6] == user_email:  # Assuming email is at index 6
                    user_index = i
                    break

            if user_index is not None:
                stored_password = rows[user_index][7]  # Assuming password is at index 7
                
                # Check if the current password matches the stored password
                if current_password != stored_password:
                    messagebox.showinfo("Error", "Current password is incorrect.")
                elif new_password != confirm_new_password:
                    messagebox.showinfo("Error", "New password and confirm password do not match.")
                else:
                    # Update the password in the list of rows
                    rows[user_index][7] = new_password

                    # Write the updated rows back to the CSV file
                    with open("user_accounts.csv", "w", newline="") as csvfile:
                        writer = csv.writer(csvfile)
                        writer.writerows(rows)

                    messagebox.showinfo("Success", "Password updated successfully.")
            else:
                messagebox.showinfo("Error", "User not found.")


        # creating change password page
        change_button_page = ctk.CTkFrame(master=end_user_dashboard, width=550, height=600)
        change_button_page.place(x=150, y=0)

        # creating current password label and entry box
        current_password_label = ctk.CTkLabel(change_button_page, text="Your Current Password", font=(font_style, 23))
        current_password_label.place(x=120, y=80)

        current_password_entry = ctk.CTkEntry(change_button_page, width=300, show="*")
        current_password_entry.place(x=80, y=130)

        current_password_shown_check = ctk.CTkCheckBox(change_button_page, text="Show Password", 
                                        command=lambda:show_hide_password(current_password_entry),
                                        font=(font_style, 10))
        current_password_shown_check.place(x=400, y=130)


        # creating new password label and entry box
        new_password_label = ctk.CTkLabel(change_button_page, text="Your New Password", font=(font_style, 23))
        new_password_label.place(x=120, y=190)

        new_password_entry = ctk.CTkEntry(change_button_page, width=300, show="*")
        new_password_entry.place(x=80, y=240)

        new_password_shown_check = ctk.CTkCheckBox(change_button_page, text="Show Password", 
                                        command=lambda:show_hide_password(new_password_entry), 
                                        font=(font_style, 10))
        new_password_shown_check.place(x=400, y=240)


        # creating confirm new password label and entry box
        confirm_new_password_label = ctk.CTkLabel(change_button_page, text="Confirm New Password", font=(font_style, 23))
        confirm_new_password_label.place(x=120, y=300)

        confirm_new_password_entry = ctk.CTkEntry(change_button_page, width=300, show="*")
        confirm_new_password_entry.place(x=80, y=340)

        confirm_password_shown_check = ctk.CTkCheckBox(change_button_page, text="Show Password", 
                                        command=lambda:show_hide_password(confirm_new_password_entry),
                                        font=(font_style, 10))
        confirm_password_shown_check.place(x=400, y=340)     


        # create register button
        confirm_button = ctk.CTkButton(change_button_page, text="Confirm", command=confirm_button,
                                        font=(font_style, 12))
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
    end_user_menu = ctk.CTkFrame(master=end_user_dashboard, width=150, height=600, fg_color="#ECE9EE")
    end_user_menu.place(relx=0, rely=0)

    # Create funtion button for end user menu
    end_user_home_button = ctk.CTkButton(end_user_menu, text="Home", 
                                         command=lambda: navigate_to_home_page(user_email),
                                        font=(font_style, 12))
    end_user_home_button.place(x=5, y=150)


    end_user_edit_button = ctk.CTkButton(end_user_menu, text="Edit Profile", 
                                         command=lambda: navigate_to_edit_profile_page(user_email),
                                        font=(font_style, 12))
    end_user_edit_button.place(x=5, y=190)


    end_user_change_password_button = ctk.CTkButton(end_user_menu, text="Change Password", 
                                                    command=lambda: navigate_to_change_password_page(user_email),
                                                    font=(font_style, 12))
    end_user_change_password_button.place(x=5, y=230)


    end_user_logout_button = ctk.CTkButton(end_user_menu, text="Logout", 
                                           command=lambda: navigate_to_logout_page(user_email),
                                            font=(font_style, 12))
    end_user_logout_button.place(x=5, y=500)
    
    end_user_home_button_function(user_email)


font_style = "Congenial"


# Invocate the first page of the system (Login Page)
Login_page_function()
app.mainloop()