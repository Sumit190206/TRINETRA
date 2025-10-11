import os
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk, ImageSequence, ImageDraw, ImageFilter
import auth_module

auth_module.create_db()

# -----------------------------
# Main Dashboard with Fullscreen Eye Animation + Animated Text
# -----------------------------
def open_main_dashboard(username):
    dash = Tk()
    dash.title("Smart Surveillance Dashboard")
    dash.state('zoomed')
    dash.configure(bg="#0f172a")

    screen_w = dash.winfo_screenwidth()
    screen_h = dash.winfo_screenheight()

    # Fullscreen GIF label
    eye_label = Label(dash, bg="#0f172a")
    eye_label.place(x=0, y=0, width=screen_w, height=screen_h)

    # Overlay text labels
    message_label = Label(dash, text=f"Welcome {username}!\nInitializing System...",
                          font=("Arial", 36, "bold"), fg="#ffffff", bg="#0f172a", justify=CENTER)
    message_label.place(relx=0.5, rely=0.45, anchor=CENTER)

    loading_label = Label(dash, text="Loading...", font=("Arial", 24, "italic"), fg="#ffffff", bg="#0f172a")
    loading_label.place(relx=0.5, rely=0.55, anchor=CENTER)

    # Load GIF frames
    try:
        from PIL import ImageSequence
        eye_gif = Image.open(r"C:\Users\Sumit Patil\project\ui-ux\eye_open.gif")
        frames = [ImageTk.PhotoImage(frame.convert("RGBA").resize((screen_w, screen_h)))
                  for frame in ImageSequence.Iterator(eye_gif)]
    except Exception as e:
        print("Error loading GIF:", e)
        frames = []

    dash._frames = frames  # Keep reference

    # Animate GIF
    def animate_gif(index=0):
        if not eye_label.winfo_exists(): return
        if frames:
            eye_label.config(image=frames[index])
            dash.after(100, animate_gif, (index + 1) % len(frames))
    animate_gif()

    # Glowing text effect
    # Glowing text effect
    glow_colors = ["#ffffff", "#00ffff", "#22c55e", "#3b82f6", "#ffffff"]
    def glow_text(index=0):
        if message_label.winfo_exists():  # ✅ Check existence
            message_label.config(fg=glow_colors[index % len(glow_colors)])
            dash.after(200, glow_text, index+1)

    # Blinking "Loading..." animation
    def blink_loading(state=[True]):
        if loading_label.winfo_exists():  # ✅ Check existence
            loading_label.config(text="Loading..." if state[0] else "")
            state[0] = not state[0]
            dash.after(500, blink_loading, state)

    # Dashboard widgets (hidden initially)
    title_label = Label(dash, text=f"🎥 Smart Surveillance System",
                        font=("Arial", 28, "bold"), fg="white", bg="#0f172a")
    info_label = Label(dash, text="Camera feed and alerts will appear here.",
                       font=("Arial", 14), fg="#cbd5e1", bg="#0f172a")
    exit_btn = Button(dash, text="Exit", bg="#ef4444", fg="white",
                      activebackground="#dc2626", font=("Arial", 14, "bold"),
                      padx=25, pady=8, relief="flat", command=dash.destroy)

    title_label.place_forget()
    info_label.place_forget()
    exit_btn.place_forget()

    # Show dashboard after animation
    total_duration = max(len(frames)*100, len(message_label.cget("text"))*80 + 500)
    def show_dashboard():
        if eye_label.winfo_exists(): eye_label.destroy()
        if message_label.winfo_exists(): message_label.destroy()
        if loading_label.winfo_exists(): loading_label.destroy()
        title_label.place(relx=0.5, rely=0.2, anchor=CENTER)
        info_label.place(relx=0.5, rely=0.35, anchor=CENTER)
        exit_btn.place(relx=0.5, rely=0.7, anchor=CENTER)

    dash.after(total_duration, show_dashboard)
    dash.mainloop()

# -----------------------------
# Create Account window
# -----------------------------
def show_create_account(parent):
    reg = Toplevel(parent)
    reg.title("Create Account")
    reg.geometry("420x420")
    reg.resizable(False, False)
    reg.configure(bg="#0f172a")

    Label(reg, text="Create Account", font=("Arial", 18, "bold"), fg="white", bg="#0f172a").pack(pady=15)
    Label(reg, text="Username:", fg="white", bg="#0f172a").pack(pady=(10,0))
    in_user = Entry(reg, font=("Arial", 12), width=30, justify="center")
    in_user.pack(pady=5, ipady=4)

    Label(reg, text="Password:", fg="white", bg="#0f172a").pack(pady=(10,0))
    in_pass = Entry(reg, font=("Arial", 12), width=30, justify="center", show="*")
    in_pass.pack(pady=5, ipady=4)

    Label(reg, text="Confirm Password:", fg="white", bg="#0f172a").pack(pady=(10,0))
    in_conf = Entry(reg, font=("Arial", 12), width=30, justify="center", show="*")
    in_conf.pack(pady=5, ipady=4)

    def try_register():
        u = in_user.get().strip()
        p = in_pass.get()
        c = in_conf.get()
        if not u or not p:
            messagebox.showwarning("Missing", "Please fill all fields.")
            return
        if p != c:
            messagebox.showerror("Mismatch", "Passwords do not match.")
            return
        ok = auth_module.register_user(u, p)
        if ok:
            messagebox.showinfo("Done", "Account created successfully.")
            reg.destroy()
        else:
            messagebox.showerror("Error", "Username already exists or registration failed.")

    Button(reg, text="Create Account", command=try_register,
           bg="#22c55e", fg="white", font=("Arial", 12, "bold"),
           relief="flat", padx=10, pady=6, width=18).pack(pady=18)
    Button(reg, text="Cancel", command=reg.destroy,
           bg="#ef4444", fg="white", font=("Arial", 10, "bold"),
           relief="flat", padx=6, pady=4, width=12).pack()

# -----------------------------
# Login action
# -----------------------------
def login_action(root, username_entry, password_entry):
    username = username_entry.get().strip()
    password = password_entry.get()
    if auth_module.verify_user(username, password):
        messagebox.showinfo("Login Success", f"Welcome, {username}!")
        root.destroy()
        open_main_dashboard(username)  # ✅ Call the dashboard directly
    else:
        messagebox.showerror("Login Failed", "Invalid username or password")

# -----------------------------
# Build Login UI
# -----------------------------
def build_login_ui():
    root = Tk()
    root.title("Login - Smart Surveillance System")
    root.state('zoomed')
    root.configure(bg="#0f172a")

    screen_w = root.winfo_screenwidth()
    screen_h = root.winfo_screenheight()

    # Background image
    bg_path = r"C:\Users\Sumit Patil\project\ui-ux\background.jpg"
    if os.path.exists(bg_path):
        bg_image = Image.open(bg_path).resize((screen_w, screen_h))
        bg_photo = ImageTk.PhotoImage(bg_image)
        bg_label = Label(root, image=bg_photo)
        bg_label.image = bg_photo
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)
    else:
        root.configure(bg="#0f172a")

    # Login Frame
    frame = Frame(root, bg="#000000", bd=0)
    frame.place(relx=0.5, rely=0.5, anchor=CENTER, width=480, height=360)

    Label(frame, text="Smart Surveillance", font=("Arial", 20, "bold"), fg="white", bg="#000000").pack(pady=12)
    Label(frame, text="Sign in to continue", font=("Arial", 10), fg="#cbd5e1", bg="#000000").pack(pady=6)

    Label(frame, text="Username", fg="#cbd5e1", bg="#000000", anchor="w").pack(fill="x", padx=30)
    entry_username = Entry(frame, font=("Arial", 12))
    entry_username.pack(padx=30, pady=6, ipady=4, fill="x")

    Label(frame, text="Password", fg="#cbd5e1", bg="#000000", anchor="w").pack(fill="x", padx=30)
    entry_password = Entry(frame, font=("Arial", 12), show="*")
    entry_password.pack(padx=30, pady=6, ipady=4, fill="x")

    # Buttons
    btn_frame = Frame(frame, bg="#000000")
    btn_frame.pack(pady=12)
    Button(btn_frame, text="Login", font=("Arial", 12, "bold"),
           bg="#2563eb", fg="white", relief="flat", padx=18, pady=8,
           command=lambda: login_action(root, entry_username, entry_password)).grid(row=0, column=0, padx=8)
    Button(btn_frame, text="Create Account", font=("Arial", 12, "bold"),
           bg="#22c55e", fg="white", relief="flat", padx=14, pady=8,
           command=lambda: show_create_account(root)).grid(row=0, column=1, padx=8)

    root.mainloop()

if __name__ == "__main__":
    build_login_ui()
