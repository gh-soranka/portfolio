import tkinter as tk
from tkinter import Tk
import psutil


"""
WORK IN PROGRESS    WORK IN PROGRESS    WORK IN PROGRESS    WORK IN PROGRESS    WORK IN PROGRESS
"""


# ----- Window Settings & Config | Titlebar -----

window = Tk()

window_width = 600
window_height = 250

screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

placement_x = (screen_width - window_width) // 2
placement_y = (screen_height - window_height) // 2

window.geometry(f"{window_width}x{window_height}+{placement_x}+{placement_y}")

window.title("PC Monitoring")
window_title = window.title()
window.overrideredirect(True)

# Window Moving

def start_move(event):
    window.x = event.x_root
    window.y = event.y_root

def move_window(event):
    dx = event.x_root - window.x
    dy = event.y_root - window.y

    x = window.winfo_x() + dx
    y = window.winfo_y() + dy

    window.geometry(f"+{x}+{y}")

    window.x = event.x_root
    window.y = event.y_root


# Fonts
title_font = ("Verdana", 16)
label_font = ("Verdana", 12)

# Titlebar

dummy = tk.Label(window, text="Test", font=title_font)
dummy.update_idletasks()
title_height = dummy.winfo_height() + 10

titlebar = tk.Frame(window, bg="#ACACAC", height=title_height)
titlebar.pack(fill="x")

titlebar.bind("<Button-1>", start_move)
titlebar.bind("<B1-Motion>", move_window)

title_label = tk.Label(
    titlebar,
    text=str(window_title),
    bg="#ACACAC",
    fg="Black",
    font=title_font
)
title_label.pack(side="left", padx=10)

title_label.bind("<Button-1>", start_move)
title_label.bind("<B1-Motion>", move_window)

close_button = tk.Button(
    titlebar,
    text="✕",
    bg="#ff5555",
    fg="white",
    border=0,
    command=window.destroy
)
close_button.pack(side="right", padx=5)

window.config(bg="#ffffff")


# ----- Funktionen -----

# close + own message box
def custom_confirm_exit():
    # Neues Fenster
    dialog = tk.Toplevel(window)
    dialog.title("Beenden")
    dialog.geometry("300x120")
    dialog.transient(window)  
    dialog.grab_set()         

    # Hintergrund
    dialog.config(bg="#ACACAC")

    # Nachricht
    tk.Label(
        dialog,
        text="Möchtest du das Programm wirklich beenden?",
        bg="#ACACAC",
        fg="black",
        font=("Verdana", 12),
        wraplength=280,
        justify="center"
    ).pack(padx=10, pady=20)

    # Buttons
    button_frame = tk.Frame(dialog, bg="#ACACAC")
    button_frame.pack(pady=5)

    def yes():
        dialog.grab_release()
        window.destroy()

    def no():
        dialog.grab_release()
        dialog.destroy()

    tk.Button(button_frame, text="Ja", bg="#ff5555", fg="white", font=label_font, command=yes).pack(side="left", padx=10)
    tk.Button(button_frame, text="Nein", bg="#555555", fg="white", font=label_font, command=no).pack(side="left", padx=10)

    # Fenster zentrieren
    dialog.update_idletasks()
    x = window.winfo_x() + (window.winfo_width() - dialog.winfo_width()) // 2
    y = window.winfo_y() + (window.winfo_height() - dialog.winfo_height()) // 2
    dialog.geometry(f"+{x}+{y}")

    # Fenster moven
    def start_move(event):
        dialog.x = event.x_root
        dialog.y = event.y_root

    def move_window(event):
        dx = event.x_root - dialog.x
        dy = event.y_root - dialog.y
        dialog.geometry(f"+{dialog.winfo_x()+dx}+{dialog.winfo_y()+dy}")
        dialog.x = event.x_root
        dialog.y = event.y_root

    dialog.bind("<Button-1>", start_move)
    dialog.bind("<B1-Motion>", move_window)


# CPU Temp Helper
def get_cpu_temp():
    try:
        if not hasattr(psutil, "sensors_temperatures"):
            return None

        temps = psutil.sensors_temperatures()
        if not temps:
            return None

        for name in temps:
            if temps[name]:
                return temps[name][0].current
    except Exception:
        return None

    return None


def update_stats():
    cpu_temp = get_cpu_temp()
    if cpu_temp is not None:
        cpu_label.config(text=f"CPU Temperatur: {cpu_temp:.1f} °C")
    else:
        cpu_label.config(text="CPU Temperatur: N/A (Windows)")

    ram = psutil.virtual_memory()
    ram_label.config(text=f"RAM Nutzung: {ram.percent:.1f} %")

    window.after(1000, update_stats)


# ----- Content -----

content_height = window_height - title_height

content = tk.Frame(
    window,
    bg="#ffffff",
    width=window_width,
    height=content_height
)
content.pack()
content.pack_propagate(False)


# +++++ FRAME +++++

frame = tk.Frame(content, bg="#595959")
frame.pack(fill="both", expand=True)

frame.grid_rowconfigure(2, weight=1)
frame.grid_columnconfigure(0, weight=1)

cpu_label = tk.Label(frame, text="CPU Temperatur: -- °C",
                     bg="#595959", fg="white", font=label_font)
cpu_label.grid(row=0, column=0, sticky="nw", padx=10, pady=(10, 5))

ram_label = tk.Label(frame, text="RAM Nutzung: -- %",
                     bg="#595959", fg="white", font=label_font)
ram_label.grid(row=1, column=0, sticky="nw", padx=10, pady=5)

exit_button = tk.Button(
    frame,
    text="Beenden",
    font=label_font,
    bg="#ff5555",
    fg="white",
    command=custom_confirm_exit
)
exit_button.grid(
    row=2,
    column=0,
    sticky="s",
    pady=10
)


update_stats()

# ----- Main Loop -----

window.mainloop()
