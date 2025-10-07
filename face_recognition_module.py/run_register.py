# run_register.py
import auth_module

# Make sure the database exists
auth_module.create_db()

# Take input from user
username = input("Enter a username to register: ")
password = input("Enter a password: ")

# Save user in database
auth_module.register_user(username, password)

print("✅ User registered successfully.")
