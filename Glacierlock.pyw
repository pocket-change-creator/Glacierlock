import tkinter as tk
from pynput import keyboard
from threading import Thread

# --- Configuration ---
PASSWORD = "1234"  # Set your password here
ALLOWED_KEYS = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")

# --- Keyboard Listener ---
def on_press(key):
    try:
        if hasattr(key, 'char') and key.char not in ALLOWED_KEYS:
            return False  # Block disallowed characters
    except AttributeError:
        return False  # Block special keys (Shift, Ctrl, etc.)

listener = keyboard.Listener(on_press=on_press)

# --- GUI Functions ---
def check_password():
    if entry.get() == PASSWORD:
        listener.stop()  # Stop blocking keys
        root.destroy()
    else:
        entry.delete(0, tk.END)
        status_label.config(text="Incorrect password. Try again.", fg="red")

def start_listener():
    listener.start()

# --- GUI Setup ---
root = tk.Tk()
root.title("GlacierLock")
root.attributes("-fullscreen", True)  # Fullscreen
root.configure(bg="#1E90FF")  # Blue background
root.protocol("WM_DELETE_WINDOW", lambda: None)  # Disable window close button

# Centered frame for input
frame = tk.Frame(root, bg="#1E90FF")
frame.place(relx=0.5, rely=0.5, anchor="center")

tk.Label(frame, text="🔒 GlacierLock", font=("Helvetica", 36, "bold"), bg="#1E90FF", fg="white").pack(pady=20)
tk.Label(frame, text="Enter password to unlock:", font=("Helvetica", 20), bg="#1E90FF", fg="white").pack(pady=10)

entry = tk.Entry(frame, show="*", font=("Helvetica", 20))
entry.pack(pady=10)
entry.focus_set()

tk.Button(frame, text="Unlock", command=check_password, font=("Helvetica", 18), bg="white", fg="#1E90FF").pack(pady=10)
status_label = tk.Label(frame, text="", font=("Helvetica", 16), bg="#1E90FF", fg="red")
status_label.pack(pady=5)

# Start the keyboard listener in a separate thread
Thread(target=start_listener, daemon=True).start()

root.mainloop()
