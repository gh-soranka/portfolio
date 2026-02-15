import tkinter as tk

class Wert:
    def __init__(self, betrag, name, beschreibung):
        self.betrag = betrag
        self.name = name
        self.beschreibung = beschreibung

    @property
    def betrag(self):
        return self._betrag
    
    @betrag.setter
    def betrag(self, value):
        if value is None:
            raise ValueError("Betrag darf nicht leer sein")
        try:
            value = float(value)
        except (ValueError, TypeError):
            raise ValueError("Betrag muss eine Zahl sein")
        if value < 1:
            raise ValueError("Betrag kann nicht negativ oder Null sein")
        self._betrag = value

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if value is None:
            raise ValueError("Name darf nicht leer sein")
        if not isinstance(value, str):
            raise ValueError("Name muss ein String sein")
        if value.strip() == "":
            raise ValueError("Name kann nicht leer sein")
        self._name = value

    @property
    def beschreibung(self):
        return self._beschreibung

    @beschreibung.setter
    def beschreibung(self, value):
        # if value is None:
        #     raise ValueError("Beschreibung darf nicht leer sein")
        if not isinstance(value, str):
            raise ValueError("Beschreibung muss ein String sein")
        # if value.strip() == "":
        #     raise ValueError("Beschreibung kann nicht leer sein")
        self._beschreibung = value


class Einnahme(Wert):
    anzahl_einnahmen = 0
    def __init__(self, betrag, name, beschreibung, income, monthly):
        super().__init__(betrag, name, beschreibung)
        self._income = bool(income)
        self._monthly = bool(monthly)
        Einnahme.anzahl_einnahmen += 1

    @property
    def income(self):
        return self._income

    @income.setter
    def income(self, value):
        if not isinstance(value, bool):
            raise ValueError("Income muss bool sein")
        self._income = value

    @property
    def monthly(self):
        return self._monthly
    
    @monthly.setter
    def monthly(self, value):
        if not isinstance(value, bool):
            raise ValueError("Monthly muss bool sein")
        self._monthly = value

    def __str__(self):
        typ = "monatlich" if self.monthly else "jährlich"
        return f"{self.name} | Betrag: {self.betrag} € | Beschreibung: {self.beschreibung} | Income: {self.income} | {typ}"


class Ausgabe(Wert):
    anzahl_ausgaben = 0
    def __init__(self, betrag, name, beschreibung, payment, monthly):
        super().__init__(betrag, name, beschreibung)
        self._payment = bool(payment)
        self._monthly = bool(monthly)
        Ausgabe.anzahl_ausgaben += 1

    @property
    def payment(self):
        return self._payment

    @payment.setter
    def payment(self, value):
        if not isinstance(value, bool):
            raise ValueError("Payment muss bool sein")
        self._payment = value

    @property
    def monthly(self):
        return self._monthly
    
    @monthly.setter
    def monthly(self, value):
        if not isinstance(value, bool):
            raise ValueError("Monthly muss bool sein")
        self._monthly = value

    def __str__(self):
        typ = "monatlich" if self.monthly else "jährlich"
        return f"{self.name} | Betrag: {self.betrag} € | Beschreibung: {self.beschreibung} | Payment: {self.payment} | {typ}"


class ToolTip():
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip_window = None

        widget.bind("<Enter>", self.show_tooltip)
        widget.bind("<Leave>", self.hide_tooltip)

    def show_tooltip(self, event=None):
        if self.tooltip_window:
            return

        x = self.widget.winfo_rootx() + 40
        y = self.widget.winfo_rooty() + 40

        self.tooltip_window = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")

        label = tk.Label(
            tw,
            text=self.text,
            background="#222222",
            foreground="white",
            relief="solid",
            borderwidth=1,
            font=("Verdana", 9)
        )
        label.pack(ipadx=5, ipady=3)

    def hide_tooltip(self, event=None):
        if self.tooltip_window:
            self.tooltip_window.destroy()
            self.tooltip_window = None