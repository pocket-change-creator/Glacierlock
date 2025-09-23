import tkinter as tk
from pynput import keyboard
from threading import Thread

# --- Configuration ---
PASSWORD = "1234"
ALLOWED_KEYS = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")

# Track pressed modifier keys
pressed_modifiers = set()

# --- Keyboard Control ---
def on_press(key):
    try:
        # Track modifier keys
        if key in {keyboard.Key.alt_l, keyboard.Key.alt_r, keyboard.Key.ctrl_l, keyboard.Key.ctrl_r, keyboard.Key.cmd, keyboard.Key.cmd_r}:
            pressed_modifiers.add(key)
        
        # Block Windows key, function keys, and disallowed combos
        if key in {keyboard.Key.esc, keyboard.Key.tab, keyboard.Key.delete, keyboard.Key.f1,
                   keyboard.Key.f2, keyboard.Key.f3, keyboard.Key.f4, keyboard.Key.f5,
                   keyboard.Key.f6, keyboard.Key.f7, keyboard.Key.f8, keyboard.Key.f9,
                   keyboard.Key.f10, keyboard.Key.f11, keyboard.Key.f12,
                   keyboard.Key.media_play_pause, keyboard.Key.media_volume_up, keyboard.Key.media_volume_down,
                   keyboard.Key.cmd, keyboard.Key.cmd_r}:
            return False

        # Block Ctrl+Alt+something
        if (keyboard.Key.ctrl_l in pressed_modifiers or keyboard.Key.ctrl_r in pressed_modifiers) and \
           (keyboard.Key.alt_l in pressed_modifiers or keyboard.Key.alt_r in pressed_modifiers):
            return False

        # Only allow letters/numbers
        if hasattr(key, 'char') and key.char not in ALLOWED_KEYS:
            return False

    except AttributeError:
        return False  # Block special keys

def on_release(key):
    if key in pressed_modifiers:
        pressed_modifiers.remove(key)

listener = keyboard.Listener(on_press=on_press, on_release=on_release)

# --- GUI Functions ---
def check_password():
    if entry.get() == PASSWORD:
        listener.stop()
        root.destroy()
    else:
        entry.delete(0, tk.END)
        status_label.config(text="Incorrect password. Try again.", fg="red")

def start_listener():
    listener.start()

# --- GUI Setup ---
root = tk.Tk()
root.title("GlacierLock")
root.attributes("-fullscreen", True)
root.configure(bg="#1E90FF")
root.protocol("WM_DELETE_WINDOW", lambda: None)  # Disable close button

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

Thread(target=start_listener, daemon=True).start()
root.mainloop()
