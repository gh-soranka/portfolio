import tkinter as tk
from tkinter import Tk, Toplevel, messagebox, PhotoImage
from settings import *
from classes import Einnahme, Ausgabe, ToolTip
from data import save_entries, load_entries

def truncate_name(name, max_length=MAX_NAME_LENGTH):
    return name if len(name) <= max_length else name[:max_length-1] + "…"

class BudgetApp:

    def __init__(self, master: Tk):
        self.master = master
        self.master.title("Budgetti")

        # Icon
        try:
            self.icon = PhotoImage(file=PICON_PATH)
            self.master.iconphoto(True, self.icon)
        except Exception as e:
            print("Icon konnte nicht geladen werden:", e)

        # Hintergrund
        self.master.config(bg=BG_COLOR)

        # Startgröße & zentrieren
        self.master.geometry(get_geometry(master))

        # Mindestgröße
        self.master.minsize(MIN_WINDOW_WIDTH, MIN_WINDOW_HEIGHT)

        # Daten laden
        self.einnahmen, self.ausgaben = load_entries()

        self.icon_edit = tk.PhotoImage(file="budgetti/images/edit.bmp")
        self.icon_delete = tk.PhotoImage(file="budgetti/images/delete.bmp")
        self.icon_info = tk.PhotoImage(file="budgetti/images/info.bmp")

        # Frames
        self.menu_frame = tk.Frame(master, bg=MENU_BG_COLOR, width=250)
        self.menu_frame.pack(side=tk.LEFT, fill=tk.Y)

        # Scrollbarer Content
        self.content_canvas = tk.Canvas(master, bg=BG_COLOR, highlightthickness=0)
        self.scrollbar = tk.Scrollbar(master, orient="vertical", command=self.content_canvas.yview)
        self.content_canvas.configure(yscrollcommand=self.scrollbar.set)

        self.content_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.content_frame = tk.Frame(self.content_canvas, bg=BG_COLOR)
        self.canvas_window = self.content_canvas.create_window((0,0), window=self.content_frame, anchor="nw")

        # Automatische Scrollregion
        self.content_frame.bind("<Configure>", lambda e: self.content_canvas.configure(scrollregion=self.content_canvas.bbox("all")))

        # Mausrad scrollen
        def _on_mousewheel(event):
            if event.num == 5 or event.delta < 0:
                self.content_canvas.yview_scroll(1, "units")
            elif event.num == 4 or event.delta > 0:
                self.content_canvas.yview_scroll(-1, "units")

        # Windows / Mac
        self.content_canvas.bind_all("<MouseWheel>", _on_mousewheel)
        # Linux
        self.content_canvas.bind_all("<Button-4>", _on_mousewheel)
        self.content_canvas.bind_all("<Button-5>", _on_mousewheel)

        # Menü Buttons
        btn_exit = tk.Button(
            self.menu_frame,
            text="EXIT",
            font=TEXT_FONT,
            command=self.master.destroy
        )
        btn_exit.pack(side=tk.BOTTOM, padx=5, pady=5, fill=tk.X)
        ToolTip(btn_exit, "Beendet das Programm")

        btn_add = tk.Button(
            self.menu_frame,
            text="ADD",
            font=TEXT_FONT,
            command=self.open_add_window
        )
        btn_add.pack(side=tk.BOTTOM, padx=5, pady=5, fill=tk.X)
        ToolTip(btn_add, "Erstellt eine neue Einnahme oder Ausgabe")

        # Content Labels und Container
        self.einnahmen_label = tk.Label(
            self.content_frame,
            text="Einnahmen",
            font=HIGHLIGHT_FONT,
            bg=BG_COLOR,
            fg="white"
        )
        self.einnahmen_label.pack(anchor="nw", pady=(5, 0))

        self.einnahmen_container = tk.Frame(self.content_frame, bg=BG_COLOR)
        self.einnahmen_container.pack(anchor="nw", fill=tk.X, padx=10, pady=(5, 20))

        self.ausgaben_label = tk.Label(
            self.content_frame,
            text="Ausgaben",
            font=HIGHLIGHT_FONT,
            bg=BG_COLOR,
            fg="white"
        )
        self.ausgaben_label.pack(anchor="nw", pady=(5, 0))

        self.ausgaben_container = tk.Frame(self.content_frame, bg=BG_COLOR)
        self.ausgaben_container.pack(anchor="nw", fill=tk.X, padx=10, pady=(5, 20))

        self.berechnung_label = tk.Label(
            self.content_frame,
            text="Berechnung",
            font=HIGHLIGHT_FONT,
            bg=BG_COLOR,
            fg="white"
        )
        self.berechnung_label.pack(anchor="nw", pady=(10,0))

        self.berechnung_container = tk.Frame(self.content_frame, bg=BG_COLOR)
        self.berechnung_container.pack(anchor="nw", fill=tk.X, padx=10, pady=(5, 10))

        # Berechnung Labels
        self.label_einnahmen_monatlich = tk.Label(self.berechnung_container, text="Einnahmen Monatlich: 0.00 €", font=TEXT_FONT, bg=BG_COLOR, fg="white")
        self.label_einnahmen_monatlich.pack(anchor="w")
        self.label_einnahmen_jaehrlich = tk.Label(self.berechnung_container, text="Einnahmen Jährlich: 0.00 €", font=TEXT_FONT, bg=BG_COLOR, fg="white")
        self.label_einnahmen_jaehrlich.pack(anchor="w")
        tk.Label(self.berechnung_container, text="", bg=BG_COLOR).pack()
        self.label_ausgaben_monatlich = tk.Label(self.berechnung_container, text="Ausgaben Monatlich: 0.00 €", font=TEXT_FONT, bg=BG_COLOR, fg="red")
        self.label_ausgaben_monatlich.pack(anchor="w")
        self.label_ausgaben_jaehrlich = tk.Label(self.berechnung_container, text="Ausgaben Jährlich: 0.00 €", font=TEXT_FONT, bg=BG_COLOR, fg="red")
        self.label_ausgaben_jaehrlich.pack(anchor="w")
        tk.Label(self.berechnung_container, text="", bg=BG_COLOR).pack()
        self.label_gewinn_monatlich = tk.Label(self.berechnung_container, text="Monatsbilanz: 0.00 €", font=TEXT_FONT, bg=BG_COLOR, fg="white")
        self.label_gewinn_monatlich.pack(anchor="w", pady=(5,0))
        self.label_gewinn_jaehrlich = tk.Label(self.berechnung_container, text="Jahresbilanz: 0.00 €", font=TEXT_FONT, bg=BG_COLOR, fg="white")
        self.label_gewinn_jaehrlich.pack(anchor="w")

        # Aktuelle Anzeige
        self.update_display()

        # Add-Window Referenz
        self.add_window = None

    # ---------- Anzeige Aktualisieren ----------
    def update_display(self):
        # Container leeren
        for widget in self.einnahmen_container.winfo_children():
            widget.destroy()
        for widget in self.ausgaben_container.winfo_children():
            widget.destroy()

        # ---------- EINNAHMEN ----------
        for e in self.einnahmen:
            frame = tk.Frame(self.einnahmen_container, bg="#555555", pady=2)
            frame.pack(fill=tk.X, padx=10, pady=1)

            name_label = tk.Label(frame, text=truncate_name(e.name), bg="#555555", fg="white", font=TEXT_FONT, width=MAX_NAME_LENGTH, anchor="w")
            name_label.pack(side=tk.LEFT, padx=(5,5))

            info_btn = tk.Label(frame, image=self.icon_info, bg="#555555", cursor="hand2")
            info_btn.pack(side=tk.LEFT, padx=(0,5))
            ToolTip(info_btn, e.beschreibung)

            tk.Label(frame, text=f"{float(e.betrag):.2f} €", bg="#555555", fg="white", font=TEXT_FONT, width=10, anchor="w").pack(side=tk.LEFT)
            typ_text = "mtl." if e.monthly else "jährl."
            tk.Label(frame, text=typ_text, bg="#555555", fg="white", font=TEXT_FONT, width=4, anchor="w").pack(side=tk.LEFT)

            btn_delete = tk.Button(frame, image=self.icon_delete, command=lambda entry=e: self.delete_entry(entry),
                                   bd=0, highlightthickness=0, bg="#555555", activebackground="#555555", cursor="hand2")
            btn_delete.pack(side=tk.RIGHT, padx=2)
            ToolTip(btn_delete, "Eintrag löschen")

            btn_edit = tk.Button(frame, image=self.icon_edit, command=lambda entry=e: self.open_add_window(edit_entry=entry),
                                 bd=0, highlightthickness=0, bg="#555555", activebackground="#555555", cursor="hand2")
            btn_edit.pack(side=tk.RIGHT, padx=2)
            ToolTip(btn_edit, "Eintrag bearbeiten")

        # ---------- AUSGABEN ----------
        for a in self.ausgaben:
            frame = tk.Frame(self.ausgaben_container, bg="#555555", pady=2)
            frame.pack(fill=tk.X, padx=10, pady=1)

            name_label = tk.Label(frame, text=truncate_name(a.name), bg="#555555", fg="white", font=TEXT_FONT, width=MAX_NAME_LENGTH, anchor="w")
            name_label.pack(side=tk.LEFT, padx=(5,5))

            info_btn = tk.Label(frame, image=self.icon_info, bg="#555555", cursor="hand2")
            info_btn.pack(side=tk.LEFT, padx=(0,5))
            ToolTip(info_btn, a.beschreibung)

            tk.Label(frame, text=f"{float(a.betrag):.2f} €", bg="#555555", fg="white", font=TEXT_FONT, width=10, anchor="w").pack(side=tk.LEFT)
            typ_text = "mtl." if a.monthly else "jährl."
            tk.Label(frame, text=typ_text, bg="#555555", fg="white", font=TEXT_FONT, width=4, anchor="w").pack(side=tk.LEFT)

            btn_delete = tk.Button(frame, image=self.icon_delete, command=lambda entry=a: self.delete_entry(entry),
                                   bd=0, highlightthickness=0, bg="#555555", activebackground="#555555", cursor="hand2")
            btn_delete.pack(side=tk.RIGHT, padx=2)
            ToolTip(btn_delete, "Eintrag löschen")

            btn_edit = tk.Button(frame, image=self.icon_edit, command=lambda entry=a: self.open_add_window(edit_entry=entry),
                                 bd=0, highlightthickness=0, bg="#555555", activebackground="#555555", cursor="hand2")
            btn_edit.pack(side=tk.RIGHT, padx=2)
            ToolTip(btn_edit, "Eintrag bearbeiten")

        self.update_berechnung()

    # ---------- Berechnung Aktualisieren ----------
    def update_berechnung(self):
        einnahmen_monatlich = einnahmen_jaehrlich = ausgaben_monatlich = ausgaben_jaehrlich = 0
        for e in self.einnahmen:
            betrag = float(e.betrag)
            if e.monthly:
                einnahmen_monatlich += betrag
                einnahmen_jaehrlich += betrag * 12
            else:
                einnahmen_jaehrlich += betrag
                einnahmen_monatlich += betrag / 12

        for a in self.ausgaben:
            betrag = float(a.betrag)
            if a.monthly:
                ausgaben_monatlich += betrag
                ausgaben_jaehrlich += betrag * 12
            else:
                ausgaben_jaehrlich += betrag
                ausgaben_monatlich += betrag / 12

        self.label_einnahmen_monatlich.config(text=f"Einnahmen Monatlich: {einnahmen_monatlich:.2f} €")
        self.label_einnahmen_jaehrlich.config(text=f"Einnahmen Jährlich: {einnahmen_jaehrlich:.2f} €")
        self.label_ausgaben_monatlich.config(text=f"Ausgaben Monatlich: {ausgaben_monatlich:.2f} €")
        self.label_ausgaben_jaehrlich.config(text=f"Ausgaben Jährlich: {ausgaben_jaehrlich:.2f} €")

        monatsbilanz = einnahmen_monatlich - ausgaben_monatlich
        jahresbilanz = einnahmen_jaehrlich - ausgaben_jaehrlich
        self.label_gewinn_monatlich.config(text=f"Monatsbilanz: {monatsbilanz:.2f} €", fg="green" if monatsbilanz >= 0 else "red")
        self.label_gewinn_jaehrlich.config(text=f"Jahresbilanz: {jahresbilanz:.2f} €", fg="green" if jahresbilanz >= 0 else "red")

    # ---------- Eintrag löschen ----------
    def delete_entry(self, entry):
        if entry in self.einnahmen:
            self.einnahmen.remove(entry)
        elif entry in self.ausgaben:
            self.ausgaben.remove(entry)
        save_entries(self.einnahmen, self.ausgaben)
        self.update_display()

    # ---------- Fenster zum Hinzufügen / Bearbeiten ----------
    def open_add_window(self, edit_entry=None):
        if self.add_window is not None and tk.Toplevel.winfo_exists(self.add_window):
            self.add_window.lift()
            return

        self.add_window = Toplevel(self.master)
        self.add_window.title("Hinzufügen")
        self.add_window.grab_set()
        self.add_window.maxsize(ENTRY_WIDTH, ENTRY_HEIGHT)
        self.add_window.minsize(ENTRY_WIDTH, ENTRY_HEIGHT)

        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        placement_x = (screen_width - ENTRY_WIDTH) // 2
        placement_y = (screen_height - ENTRY_HEIGHT) // 2
        self.add_window.geometry(f"{ENTRY_WIDTH}x{ENTRY_HEIGHT}+{placement_x}+{placement_y}")

        tk.Label(self.add_window, text="Name:").pack()
        name_entry = tk.Entry(self.add_window)
        name_entry.pack()

        tk.Label(self.add_window, text="Beschreibung:").pack()
        desc_entry = tk.Entry(self.add_window)
        desc_entry.pack()

        tk.Label(self.add_window, text="Betrag:").pack()
        amount_entry = tk.Entry(self.add_window)
        amount_entry.pack()

        type_var = tk.StringVar(value="Einnahme")
        tk.Radiobutton(self.add_window, text="Einnahme", variable=type_var, value="Einnahme").pack()
        tk.Radiobutton(self.add_window, text="Ausgabe", variable=type_var, value="Ausgabe").pack()

        monthly_var = tk.BooleanVar(value=True)
        tk.Radiobutton(self.add_window, text="Monatlich", variable=monthly_var, value=True).pack()
        tk.Radiobutton(self.add_window, text="Jährlich", variable=monthly_var, value=False).pack()

        if edit_entry:
            name_entry.insert(0, edit_entry.name)
            desc_entry.insert(0, edit_entry.beschreibung)
            amount_entry.insert(0, str(edit_entry.betrag))
            type_var.set("Einnahme" if isinstance(edit_entry, Einnahme) else "Ausgabe")
            monthly_var.set(edit_entry.monthly)

        def save():
            name = name_entry.get()
            desc = desc_entry.get()
            amount = amount_entry.get()
            typ = type_var.get()
            monthly = monthly_var.get()

            all_names = [e.name for e in self.einnahmen if e != edit_entry] + [a.name for a in self.ausgaben if a != edit_entry]
            if name in all_names:
                messagebox.showerror("Fehler", "Name darf nicht doppelt vorkommen")
                return

            try:
                if typ == "Einnahme":
                    entry = Einnahme(amount, name, desc, True, monthly)
                    if edit_entry: self.einnahmen[self.einnahmen.index(edit_entry)] = entry
                    else: self.einnahmen.append(entry)
                else:
                    entry = Ausgabe(amount, name, desc, True, monthly)
                    if edit_entry: self.ausgaben[self.ausgaben.index(edit_entry)] = entry
                    else: self.ausgaben.append(entry)

                save_entries(self.einnahmen, self.ausgaben)
                self.update_display()
                self.add_window.destroy()
            except ValueError as ve:
                messagebox.showerror("Fehler", str(ve))

        tk.Button(self.add_window, text="Save", command=save).pack(pady=10)


if __name__ == "__main__":
    root = Tk()
    app = BudgetApp(root)
    root.mainloop()
