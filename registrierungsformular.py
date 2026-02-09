import tkinter as tk
from tkinter import Tk
from tkinter import messagebox

""" Registrierungsformular Vorlage """

# ----- Window Settings & Config | Titlebar -----

window = Tk()

window_width = 600
window_height = 250

screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

placement_x = (screen_width - window_width) // 2
placement_y = (screen_height - window_height) // 2

window.geometry(f"{window_width}x{window_height}+{placement_x}+{placement_y}")

window.title("Formulario [Registrierungsformular]")
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

title_label = tk.Label(titlebar, text=str(window_title), bg="#ACACAC", fg="Black", font=title_font)
title_label.pack(side="left", padx=10)
title_label.bind("<Button-1>", start_move)
title_label.bind("<B1-Motion>", move_window)

close_button = tk.Button(titlebar, text="✕", bg="#ff5555", fg="white", border=0, command=window.destroy)
close_button.pack(side="right", padx=5)

window.config(bg="#ffffff")

# ----- Funktionen -----

# register
def registrieren():
    vorname = entry_vorname.get()
    nachname = entry_nachname.get()
    email = entry_email.get()
    sonderzeichen = [" ", ",", ";", ":", "!", "?", "#", "$", "%", "^", "&", "*", "(", ")", "+", "=", "{",
                     "}", "[", "]", "|", "\\", "/", "<", ">", "~", "`"]
    email_endungen = [".com", ".de", ".net", ".org", ".edu", ".gov", ".io", ".co", ".us", ".uk", ".info",
                      ".biz", ".me", ".it", ".tv", ".ca", ".au", ".fr", ".jp", ".cn", ".ru", ".br", ".in"]

    try:
        if vorname and nachname and email:
            if not email.count("@") == 1 or email.startswith("@") or email.endswith("@"):
                raise ValueError("Ungültige E-Mail-Adresse. Fehlerhaftes @-Zeichen.")
            elif "." not in email.split("@")[1]:
                raise ValueError("Ungültige E-Mail-Adresse. Punkt fehlt im Domain-Teil.")
            elif not any(email.endswith(ending) for ending in email_endungen):
                raise ValueError("Ungültige E-Mail-Adresse. Ungültige Domain-Endung.")
            elif any(char in email for char in sonderzeichen):
                raise ValueError("Ungültige E-Mail-Adresse. Sonderzeichen sind nicht erlaubt.")
            elif not vorname.isalpha() or not nachname.isalpha():
                raise ValueError("Vorname und Nachname dürfen nur Buchstaben enthalten.")
        else:
            raise ValueError("Alle Felder müssen ausgefüllt sein.")

    except ValueError as e:
        output_label.config(text=str(e), fg="#ff5555")  # rot für Fehler
    else:
        ausgabe_text = f"Registrierung erfolgreich!\nName: {vorname} {nachname}\nE-Mail: {email}"
        output_label.config(text=ausgabe_text, fg="#00ff00")  # grün für Erfolg

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

# +++++ LEFT FRAME +++++

left_frame = tk.Frame(content, bg="#595959", width=300, height=content_height)
left_frame.grid(row=0, column=0)
left_frame.grid_propagate(False)

left_frame.grid_columnconfigure(0, minsize=90)
left_frame.grid_columnconfigure(1, minsize=190)

tk.Label(left_frame, text="[Vorname]", bg="#595959", fg="white", font=label_font)\
    .grid(row=0, column=0, padx=10, pady=5, sticky="w")

entry_vorname = tk.Entry(left_frame, width=22)
entry_vorname.grid(row=0, column=1, padx=10, pady=5)

tk.Label(left_frame, text="[Nachname]", bg="#595959", fg="white", font=label_font)\
    .grid(row=1, column=0, padx=10, pady=5, sticky="w")

entry_nachname = tk.Entry(left_frame, width=22)
entry_nachname.grid(row=1, column=1, padx=10, pady=5)

tk.Label(left_frame, text="[E-Mail]", bg="#595959", fg="white", font=label_font)\
    .grid(row=2, column=0, padx=10, pady=5, sticky="w")

entry_email = tk.Entry(left_frame, width=22)
entry_email.grid(row=2, column=1, padx=10, pady=5)

tk.Button(left_frame, text="Registrieren", command=registrieren)\
    .grid(row=3, column=1, padx=10, pady=(25,5), sticky="w")

tk.Button(left_frame, text="Beenden", command=custom_confirm_exit)\
    .grid(row=4, column=1, padx=10, pady=(10,5), sticky="w")

# +++++ RIGHT FRAME +++++

right_frame = tk.Frame(content, bg="#393939", width=300, height=content_height)
right_frame.grid(row=0, column=1)
right_frame.grid_propagate(False)

output_label = tk.Label(
    right_frame,
    text="",
    bg="#393939",
    fg="#00ff00",
    font=label_font,
    justify="left",
    anchor="nw",
    wraplength=280
)
output_label.place(x=10, y=10, width=280, height=content_height - 20)

# ----- Main Loop -----

window.mainloop()