from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk, ImageSequence, ImageDraw, ImageFilter
import os
import auth_module

# =====================================================
# Initialize Database
# =====================================================
auth_module.create_db()


# =====================================================
# Eye Loading Animation
# =====================================================
def show_loading_screen():
    load = Tk()
    load.title("Activating Smart Surveillance")
    load.state('zoomed')
    load.configure(bg="#0f172a")

    screen_w = load.winfo_screenwidth()
    screen_h = load.winfo_screenheight()

    # Background label for fullscreen GIF
    bg_label = Label(load, bg="#0f172a")
    bg_label.place(x=0, y=0, width=screen_w, height=screen_h)

    # Overlay text label
    text_label = Label(
        load,
        text="Activating Smart Surveillance...",
        font=("Arial", 36, "bold"),
        fg="#000000",  # start black (invisible)
    
    )
    text_label.place(relx=0.5, rely=0.5, anchor=CENTER)

    # Load and resize GIF frames
    try:
        eye_gif = Image.open(r"C:\Users\Sumit Patil\project\ui-ux\eye_open.gif")
        frames = []
        for frame in ImageSequence.Iterator(eye_gif):
            frame = frame.convert("RGBA").resize((screen_w, screen_h))
            frames.append(ImageTk.PhotoImage(frame))
    except Exception as e:
        print("Error loading GIF:", e)
        frames = []

    load._frames = frames  # Keep references

    # Animate GIF in background
    def animate(index=0):
        if not bg_label.winfo_exists():
            return
        if frames:
            bg_label.config(image=frames[index])
            load.after(100, animate, (index + 1) % len(frames))
    animate()

    # Fade-in text effect
    fade_colors = ["#000000", "#000000", "#00000000", "#000000","#000000",
                   "#000000", "#000000", "#000000", "#000000", "#000000", "#000000"]

    def fade_in(index=0):
        if index < len(fade_colors):
            text_label.config(fg=fade_colors[index])
            load.after(150, fade_in, index + 1)
    fade_in()

    # After animation, open main dashboard
    load.after(5000, lambda: [load.destroy(), open_main_dashboard()])
    load.mainloop()


# =====================================================
# Main Dashboard
# =====================================================
def open_main_dashboard():
    dash = Tk()
    dash.title("Smart Surveillance Dashboard")
    dash.state('zoomed')
    dash.configure(bg="#0f172a")

    Label(
        dash, text="🎥 Smart Surveillance System",
        font=("Arial", 28, "bold"), fg="white", bg="#0f172a"
    ).pack(pady=40)

    Label(
        dash, text="Camera feed and alerts will appear here.",
        font=("Arial", 14), fg="#cbd5e1", bg="#0f172a"
    ).pack(pady=10)

    Button(
        dash, text="Exit", command=dash.destroy,
        bg="#ef4444", fg="white", activebackground="#dc2626",
        font=("Arial", 14, "bold"), padx=25, pady=8, relief="flat"
    ).pack(pady=40)

    dash.mainloop()


# =====================================================
# Create Account Window
# =====================================================
def show_create_account(parent):
    reg = Toplevel(parent)
    reg.title("Create Account")
    reg.geometry("420x420")
    reg.resizable(False, False)
    reg.configure(bg="#0f172a")

    Label(
        reg, text="Create Account",
        font=("Arial", 18, "bold"), fg="white", bg="#0f172a"
    ).pack(pady=15)

    Label(reg, text="Username:", fg="white", bg="#0f172a").pack(pady=(10, 0))
    in_user = Entry(reg, font=("Arial", 12), width=30, justify="center")
    in_user.pack(pady=5, ipady=4)

    Label(reg, text="Password:", fg="white", bg="#0f172a").pack(pady=(10, 0))
    in_pass = Entry(reg, font=("Arial", 12), width=30, justify="center", show="*")
    in_pass.pack(pady=5, ipady=4)

    Label(reg, text="Confirm Password:", fg="white", bg="#0f172a").pack(pady=(10, 0))
    in_conf = Entry(reg, font=("Arial", 12), width=30, justify="center", show="*")
    in_conf.pack(pady=5, ipady=4)

    def try_register():
        u = in_user.get().strip()
        p = in_pass.get()
        c = in_conf.get()

        if not u or not p or not c:
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

    Button(
        reg, text="Create Account", command=try_register,
        bg="#22c55e", fg="white", font=("Arial", 12, "bold"),
        relief="flat", padx=10, pady=6, width=18
    ).pack(pady=18)

    Button(
        reg, text="Cancel", command=reg.destroy,
        bg="#ef4444", fg="white", font=("Arial", 10, "bold"),
        relief="flat", padx=6, pady=4, width=12
    ).pack()


# =====================================================
# Login Window
# =====================================================
def build_login_ui():
    root = Tk()
    root.title("Login - Smart Surveillance System")
    root.state('zoomed')
    root.configure(bg="#0f172a")

    screen_w, screen_h = root.winfo_screenwidth(), root.winfo_screenheight()

    # Background image
    bg_path = r"C:\Users\Sumit Patil\project\ui-ux\background.jpg"
    if os.path.exists(bg_path):
        bg_image = Image.open(bg_path).resize((screen_w, screen_h))
        dark_layer = Image.new("RGB", (screen_w, screen_h), (6, 10, 25))
        bg_image = Image.blend(bg_image, dark_layer, 0.35)
    else:
        bg_image = Image.new("RGB", (screen_w, screen_h), "#0f172a")

    bg_photo = ImageTk.PhotoImage(bg_image)
    Label(root, image=bg_photo).place(x=0, y=0, relwidth=1, relheight=1)

    # Glassy login plate
    plate_w, plate_h = 480, 380
    plate = Image.new("RGBA", (plate_w, plate_h), (0, 0, 0, 180))
    draw = ImageDraw.Draw(plate)
    draw.rounded_rectangle((0, 0, plate_w, plate_h), radius=20,
                           fill=(8, 10, 20, 180), outline=(255, 255, 255, 18), width=2)
    plate = plate.filter(ImageFilter.GaussianBlur(1))
    plate_photo = ImageTk.PhotoImage(plate)
    Label(root, image=plate_photo, bd=0).place(
        relx=0.5, rely=0.5, anchor=CENTER, width=plate_w, height=plate_h
    )

    frame = Frame(root, bg="#000000", bd=0)
    frame.place(relx=0.5, rely=0.5, anchor=CENTER, width=plate_w - 20, height=plate_h - 20)

    Label(frame, text="Smart Surveillance", font=("Arial", 20, "bold"),
          fg="white", bg="#000000").pack(pady=(12, 6))
    Label(frame, text="Sign in to continue", font=("Arial", 10),
          fg="#cbd5e1", bg="#000000").pack(pady=(0, 10))

    Label(frame, text="Username", fg="#cbd5e1", bg="#000000", anchor="w").pack(fill="x", padx=30)
    entry_username = Entry(frame, font=("Arial", 12))
    entry_username.pack(padx=30, pady=(4, 8), ipady=6, fill="x")

    Label(frame, text="Password", fg="#cbd5e1", bg="#000000", anchor="w").pack(fill="x", padx=30)
    entry_password = Entry(frame, font=("Arial", 12), show="*")
    entry_password.pack(padx=30, pady=(4, 12), ipady=6, fill="x")

    # Buttons
    btn_frame = Frame(frame, bg="#000000")
    btn_frame.pack(pady=(4, 0))

    Button(
        btn_frame, text="Login", font=("Arial", 12, "bold"),
        bg="#2563eb", fg="white", activebackground="#1d4ed8", relief="flat",
        padx=18, pady=8,
        command=lambda: login_action(root, entry_username, entry_password)
    ).grid(row=0, column=0, padx=8)

    Button(
        btn_frame, text="Create Account", font=("Arial", 12, "bold"),
        bg="#22c55e", fg="white", activebackground="#16a34a", relief="flat",
        padx=14, pady=8,
        command=lambda: show_create_account(root)
    ).grid(row=0, column=1, padx=8)

    root.mainloop()


# =====================================================
# Login Action
# =====================================================
def login_action(root, username_entry, password_entry):
    username = username_entry.get().strip()
    password = password_entry.get()

    if not username or not password:
        messagebox.showwarning("Missing", "Enter both username and password.")
        return

    if auth_module.verify_user(username, password):
        messagebox.showinfo("Login Success", f"Welcome, {username}!")
        root.destroy()
        show_loading_screen()
    else:
        messagebox.showerror("Login Failed", "Invalid username or password.")


# =====================================================
# Run App
# =====================================================
if __name__ == "__main__":
    build_login_ui()
