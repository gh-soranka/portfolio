import os
import csv
from classes import Einnahme, Ausgabe

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_FILE = os.path.join(BASE_DIR,"data", "budget_data.csv")
IMAGES_DIR = os.path.join(BASE_DIR, "images")
PICON_PATH = os.path.join(BASE_DIR, "images", "icon.png")

def save_entries(einnahmen, ausgaben):
    with open(DATA_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Typ","Betrag","Name","Beschreibung","Monthly"])
        for e in einnahmen:
            writer.writerow(["Einnahme", e.betrag, e.name, e.beschreibung, e.monthly])
        for a in ausgaben:
            writer.writerow(["Ausgabe", a.betrag, a.name, a.beschreibung, a.monthly])

def load_entries():
    einnahmen = []
    ausgaben = []
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                typ = row["Typ"]
                betrag = float(row["Betrag"])
                name = row["Name"]
                beschreibung = row["Beschreibung"]
                monthly = row["Monthly"].lower() == "true"
                if typ == "Einnahme":
                    einnahmen.append(Einnahme(betrag, name, beschreibung, True, monthly))
                elif typ == "Ausgabe":
                    ausgaben.append(Ausgabe(betrag, name, beschreibung, True, monthly))
    except FileNotFoundError:
        pass
    return einnahmen, ausgaben
