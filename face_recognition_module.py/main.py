# main.py
from tkinter import *
from tkinter import messagebox
import auth_module

# Initialize DB (in case not created yet)
auth_module.create_db()

# -------------------------
# LOGIN WINDOW FUNCTIONALITY
# -------------------------
def login():
    username = entry_username.get()
    password = entry_password.get()

    if auth_module.verify_user(username, password):
        messagebox.showinfo("Login Success", "Welcome, " + username)
        root.destroy()  # Close login window
        open_main_dashboard()
    else:
        messagebox.showerror("Login Failed", "Invalid username or password")

# -------------------------
# MAIN DASHBOARD (after login)
# -------------------------
def open_main_dashboard():
    dash = Tk()
    dash.title("Smart Surveillance Dashboard")
    dash.geometry("400x300")
    Label(dash, text="🎥 Surveillance System Active", font=("Arial", 16)).pack(pady=20)
    Label(dash, text="This is your main interface.\nCamera feed and alerts will show here.", font=("Arial", 10)).pack(pady=10)
    Button(dash, text="Exit", command=dash.destroy).pack(pady=20)
    dash.mainloop()

# -------------------------
# GUI DESIGN (LOGIN WINDOW)
# -------------------------
root = Tk()
root.title("Login - Smart Surveillance System")
root.geometry("400x250")

Label(root, text="User Login", font=("Arial", 16)).pack(pady=10)

Label(root, text="Username:").pack()
entry_username = Entry(root)
entry_username.pack()

Label(root, text="Password:").pack()
entry_password = Entry(root, show="*")
entry_password.pack()

Button(root, text="Login", command=login).pack(pady=10)

root.mainloop()
