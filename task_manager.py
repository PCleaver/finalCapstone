# Notes: 
# 1. Use the following username and password to access the admin rights 
# username: admin
# password: password
# 2. Ensure you open the whole folder for this task in VS Code otherwise the 
# program will look in your root directory for the text files.

#=====importing libraries===========
import os
from datetime import datetime, date

DATETIME_STRING_FORMAT = "%Y-%m-%d"

# Create tasks.txt if it doesn't exist
if not os.path.exists("tasks.txt"):
    with open("tasks.txt", "w") as default_file:
        pass

with open("tasks.txt", 'r') as task_file:
    task_data = task_file.read().split("\n")
    task_data = [t for t in task_data if t != ""]

task_list = []
for t_str in task_data:
    curr_t = {}

    # Split by semicolon and manually add each component
    task_components = t_str.split(";")
    curr_t['username'] = task_components[0]
    curr_t['title'] = task_components[1]
    curr_t['description'] = task_components[2]
    curr_t['due_date'] = datetime.strptime(task_components[3], DATETIME_STRING_FORMAT)
    curr_t['assigned_date'] = datetime.strptime(task_components[4], DATETIME_STRING_FORMAT)
    curr_t['completed'] = True if task_components[5] == "Yes" else False

    task_list.append(curr_t)

#====Login Section====
'''This code reads usernames and password from the user.txt file to 
    allow a user to login.
'''
# If no user.txt file, write one with a default account
if not os.path.exists("user.txt"):
    with open("user.txt", "w") as default_file:
        default_file.write("admin;password")

# Read in user_data
with open("user.txt", 'r') as user_file:
    user_data = user_file.read().split("\n")

# Convert to a dictionary
username_password = {}
for user in user_data:
    username, password = user.split(';')
    username_password[username] = password    

# Function to register a new user
def reg_user():
    print()
    new_username = input("New Username: ")

    # Check if the username already exists
    while new_username in username_password.keys():
        print("Username already exists. Please choose a different username.")
        new_username = input("New Username: ")

    new_password = input("New Password: ")
    confirm_password = input("Confirm Password: ")

    if new_password == confirm_password:
        print("New user added")
        username_password[new_username] = new_password

        with open("user.txt", "w") as out_file:
            user_data = [f"{k};{username_password[k]}" for k in username_password]
            out_file.write("\n".join(user_data))
    else:
        print("Passwords do not match")

       
# Function to add a new task
def add_task():
    task_username = input("Name of person assigned to task: ")
    if task_username not in username_password.keys():
        print("User does not exist. Please enter a valid username")
        return

    task_title = input("Title of Task: ")
    task_description = input("Description of Task: ")

    while True:
        try:
            task_due_date = input("Due date of task (YYYY-MM-DD): ")
            due_date_time = datetime.strptime(task_due_date, DATETIME_STRING_FORMAT)
            break
        except ValueError:
            print("Invalid datetime format. Please use the format specified")

    curr_date = date.today()
    new_task = {
        "username": task_username,
        "title": task_title,
        "description": task_description,
        "due_date": due_date_time,
        "assigned_date": curr_date,
        "completed": False
    }

    task_list.append(new_task)
    with open("tasks.txt", "w") as task_file:
        task_list_to_write = [";".join([
            t['username'],
            t['title'],
            t['description'],
            t['due_date'].strftime(DATETIME_STRING_FORMAT),
            t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
            "Yes" if t['completed'] else "No"
        ]) for t in task_list]

        task_file.write("\n".join(task_list_to_write))
    print("Task successfully added.")

# Function to view all tasks
def view_all():
    for t in task_list:
        disp_str = f"Task: \t\t {t['title']}\n"
        disp_str += f"Assigned to: \t {t['username']}\n"
        disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Task Description: \n {t['description']}\n"
        print(disp_str)

# Function to view current user's tasks
def view_mine(curr_user):
    task_numbers = {}  # Dictionary to store task numbers
    count = 1

    for t in task_list:
        if t['username'] == curr_user:
            disp_str = f"Task {count}:\n"
            disp_str += f"Title: {t['title']}\n"
            disp_str += f"Due Date: {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Task Description: {t['description']}\n"
            disp_str += f"Status: {'Completed' if t['completed'] else 'Not Completed'}\n"
            print(disp_str)

            task_numbers[count] = task_list.index(t)
            count += 1

    while True:
        try:
            print("\nEnter the task number to select a task or enter '-1' to return to the main menu.")
            selected_task = int(input("Your choice: "))
        except ValueError:
            print("Invalid input. Please enter a valid task number.")
            continue  # This will restart the loop

        if selected_task == -1:
            return  # Return to the main menu
        elif selected_task in task_numbers:
            selected_index = task_numbers[selected_task]
            selected_task_dict = task_list[selected_index]
            
            print(f"\nSelected Task:\nTitle: {selected_task_dict['title']}\n"
                  f"Due Date: {selected_task_dict['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
                  f"Task Description: {selected_task_dict['description']}\n"
                  f"Status: {'Completed' if selected_task_dict['completed'] else 'Not Completed'}\n")

            edit_option = input("Choose an option: \n1. Mark as Complete\n2. Edit Task\nYour choice: ")

            if edit_option == '1' and not selected_task_dict['completed']:
                selected_task_dict['completed'] = True
                print("Task marked as complete.")
            elif edit_option == '2' and not selected_task_dict['completed']:
                edit_field = input("Choose field to edit (username or due date): ").lower()
                if edit_field == 'username':
                    new_username = input("Enter new username: ")
                    selected_task_dict['username'] = new_username
                elif edit_field == 'due date':
                    new_due_date = input("Enter new due date (YYYY-MM-DD): ")
                    try:
                        due_date_time = datetime.strptime(new_due_date, DATETIME_STRING_FORMAT)
                        selected_task_dict['due_date'] = due_date_time
                        print("Task due date updated.")
                    except ValueError:
                        print("Invalid datetime format. Task due date not updated.")
            else:
                print("Invalid option. Task not edited.")
            break  # Add a break here to exit the loop after performing the selected action
        else:
            print("Invalid task number. Task not selected.")

# Check if reports need to be generated 
        if not os.path.exists("task_overview.txt") or not os.path.exists("user_overview.txt"):
            generate_reports()

# Read and display task overview
        with open("task_overview.txt", 'r') as task_overview_file:
            task_overview_data = task_overview_file.read()
            print(task_overview_data)

# Read and display user overview
        with open("user_overview.txt", 'r') as user_overview_file:
            user_overview_data = user_overview_file.read()
            print(user_overview_data)

# Check if reports need to be generated
        if not os.path.exists("task_overview.txt") or not os.path.exists("user_overview.txt"):
            generate_reports()

# Read and display task overview
        with open("task_overview.txt", 'r') as task_overview_file:
            task_overview_data = task_overview_file.read()
            print(task_overview_data)

# Read and display user overview
        with open("user_overview.txt", 'r') as user_overview_file:
            user_overview_data = user_overview_file.read()
            print(user_overview_data)

from datetime import datetime, date

# Function to generate reports
def generate_reports():
    # Generate task overview
    total_tasks = len(task_list)
    completed_tasks = sum(1 for t in task_list if t['completed'])
    uncompleted_tasks = total_tasks - completed_tasks
    overdue_tasks = sum(1 for t in task_list if not t['completed'] and t['due_date'] < datetime.combine(date.today(), datetime.min.time()))

    incomplete_percentage = (uncompleted_tasks / total_tasks) * 100 if total_tasks > 0 else 0
    overdue_percentage = (overdue_tasks / total_tasks) * 100 if total_tasks > 0 else 0

    with open("task_overview.txt", "w") as task_overview_file:
        task_overview_file.write(f"Task Overview\n"
                                 f"Total Tasks: {total_tasks}\n"
                                 f"Completed Tasks: {completed_tasks}\n"
                                 f"Uncompleted Tasks: {uncompleted_tasks}\n"
                                 f"Overdue Tasks: {overdue_tasks}\n"
                                 f"Percentage of Incomplete Tasks: {incomplete_percentage:.2f}%\n"
                                 f"Percentage of Overdue Tasks: {overdue_percentage:.2f}%\n")

    # Generate user overview
    total_users = len(username_password)
    tasks_assigned_to_users = [t for t in task_list if t['username'] in username_password]

    with open("user_overview.txt", "w") as user_overview_file:
        user_overview_file.write(f"User Overview\n"
                                 f"Total Users: {total_users}\n"
                                 f"Total Tasks Assigned: {len(tasks_assigned_to_users)}\n")

        for user in username_password.keys():
            user_tasks = [t for t in tasks_assigned_to_users if t['username'] == user]
            total_user_tasks = len(user_tasks)

            if total_user_tasks > 0:
                completed_user_tasks = sum(1 for t in user_tasks if t['completed'])
                uncompleted_user_tasks = total_user_tasks - completed_user_tasks
                overdue_user_tasks = sum(1 for t in user_tasks if not t['completed'] and t['due_date'] < datetime.combine(date.today(), datetime.min.time()))
                percentage_assigned = (total_user_tasks / len(tasks_assigned_to_users)) * 100
                percentage_completed = (completed_user_tasks / total_user_tasks) * 100 if total_user_tasks > 0 else 0
                percentage_uncompleted = (uncompleted_user_tasks / total_user_tasks) * 100 if total_user_tasks > 0 else 0
                percentage_overdue = (overdue_user_tasks / total_user_tasks) * 100 if total_user_tasks > 0 else 0

                user_overview_file.write(f"\nUser: {user}\n"
                                         f"Total Tasks Assigned: {total_user_tasks}\n"
                                         f"Percentage of Total Tasks Assigned: {percentage_assigned:.2f}%\n"
                                         f"Percentage of Completed Tasks: {percentage_completed:.2f}%\n"
                                         f"Percentage of Uncompleted Tasks: {percentage_uncompleted:.2f}%\n"
                                         f"Percentage of Overdue Tasks: {percentage_overdue:.2f}%\n")
def display_statistics():
    num_users = len(username_password.keys())
    num_tasks = len(task_list)

    print("-----------------------------------")
    print(f"Number of users: \t\t {num_users}")
    print(f"Number of tasks: \t\t {num_tasks}")
    print("-----------------------------------")    

def exit_menu():
    print('Goodbye!!!')


# Function to perform admin login
def admin_login():
    admin_username = "admin"
    admin_password = "password"
    attempts = 3  # Move attempts initialization here
    login = False

    while attempts > 0:
        entered_username = input("Admin Username: ")
        entered_password = input("Admin Password: ")

        if entered_username == admin_username and entered_password == admin_password:
            print(f"Welcome, {entered_username}!")
            login = True
            break  # Exit the loop if login is successful

        print("Invalid admin credentials. Please try again.")
        attempts -= 1

    if login:
        while True:
            print()
            menu = input('''Please select one of the following options:
            r - Register user
            a - Add task
            va - View all tasks
            vm - View my tasks
            gr - Generate reports
            ds - Display statistics
            e - Exit
            : ''').lower()

            if menu == 'r':
                reg_user()
            elif menu == 'a':
                add_task()
            elif menu == 'va':
                view_all()
            elif menu == 'vm':
                view_mine(curr_user)
            elif menu == 'gr':
                generate_reports()
                print("Reports generated successfully.")
                break
            elif menu == 'ds':
                display_statistics()
            elif menu == 'e':
                exit_menu()
                break
            else:
                print("Invalid option. Please try again.")
    else:
        print("Exceeded maximum login attempts. Exiting.")
    return False

def user_login():
    max_attempts = 3

    while max_attempts > 0:
        entered_username = input("Username: ")
        entered_password = input("Password: ")

        if entered_username in username_password and username_password[entered_username] == entered_password:
            print(f"Welcome, {entered_username}!")

            while True:
                print()
                menu = input('''Please select one of the following options:
                a - Add task
                va - View all tasks
                vm - View my tasks
                e - Exit
                : ''').lower()

                if menu == 'a':
                    add_task()
                elif menu == 'va':
                    view_all()
                elif menu == 'vm':
                    view_mine(entered_username)  # Pass entered_username to view_mine
                elif menu == 'e':
                    exit_menu()
                    return True, entered_username  # Return from the function when the user chooses to exit
                else:
                    print("Invalid option. Please try again.")
        else:
            print("Invalid credentials. Please try again.")
            max_attempts -= 1

    print("Exceeded maximum login attempts. Exiting.")
    return False, None

# Main part of the login
admin_logged_in = False
user_logged_in = False
curr_user = None

while not (admin_logged_in or user_logged_in):
    login_choice = input("Select login type (admin/user): ").lower()

    if login_choice == 'admin':
        admin_logged_in = admin_login()
    elif login_choice == 'user':
        user_logged_in, curr_user = user_login()
    else:
        print("Invalid login type. Please enter 'admin' or 'user'.")