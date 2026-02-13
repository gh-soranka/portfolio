import tkinter as tk
import time


letters = [
    ['X', 'E', 'S', 'X', 'X', 'X', 'X', 'I', 'S', 'T', 'X'],        # ES IST
    ['X', 'X', 'X', 'K', 'U', 'R', 'Z', 'X', 'V', 'O', 'R'],        # KURZ, VOR2
    ['X', 'X', 'V', 'I', 'E', 'R', 'T', 'E', 'L', 'X', 'X'],        # VIERTEL
    ['X', 'N', 'A', 'C', 'H', 'X', 'H', 'A', 'L', 'B', 'X'],        # NACH2, HALB
    ['X', 'F', 'Ü', 'N', 'F', 'X', 'Z', 'E', 'H', 'N', 'X'],        # FÜNF, ZEHN
    ['X', 'Z', 'W', 'A', 'N', 'Z', 'I', 'G', 'X', 'X', 'X'],        # ZWANZIG
    ['X', 'V', 'O', 'R', 'X', 'X', 'N', 'A', 'C', 'H', 'X'],        # VOR, NACH
    ['X', 'E', 'I', 'N', 'S', 'X', 'Z', 'W', 'E', 'I', 'X'],        # 1, 2
    ['X', 'D', 'R', 'E', 'I', 'X', 'V', 'I', 'E', 'R', 'X'],        # 3, 4
    ['X', 'F', 'Ü', 'N', 'F', 'X', 'S', 'E', 'C', 'H', 'S'],        # 5, 6   
    ['S', 'I', 'E', 'B', 'E', 'N', 'X', 'A', 'C', 'H', 'T'],        # 7, 8
    ['X', 'N', 'E', 'U', 'N', 'X', 'Z', 'E', 'H', 'N', 'X'],        # 9, 10
    ['X', 'E', 'L', 'F', 'X', 'Z', 'W', 'Ö', 'L', 'F', 'X']         # 11, 12
]


word_positions = {
    "ES": [(0, 1), (0, 2)],
    "IST": [(0, 7), (0, 8), (0, 9)],
    "KURZ": [(1, 3), (1, 4), (1, 5), (1, 6)],
    "VOR2": [(1, 8), (1, 9), (1, 10)],
    "VIERTEL": [(2, 2), (2, 3), (2, 4), (2, 5), (2, 6), (2, 7), (2, 8)],
    "NACH2": [(3, 1), (3, 2), (3, 3), (3, 4)],
    "HALB": [(3,6), (3,7), (3,8), (3,9)],
    "FÜNF": [(4,1), (4,2), (4,3), (4,4)],
    "ZEHN": [(4,6), (4,7), (4,8), (4,9)],
    "ZWANZIG": [(5,1), (5,2), (5,3), (5,4), (5,5), (5,6), (5,7)],
    "VOR": [(6,1), (6,2), (6,3)],
    "NACH": [(6,6), (6,7), (6,8), (6,9)],
    "EINS": [(7,1), (7,2), (7,3), (7,4)],
    "ZWEI": [(7,6), (7,7), (7,8), (7,9)],
    "DREI": [(8,1), (8,2), (8,3), (8,4)],
    "VIER": [(8,6), (8,7), (8,8), (8,9)],
    "FÜNF_H": [(9,1), (9,2), (9,3), (9,4)],
    "SECHS": [(9,6), (9,7), (9,8), (9,9), (9,10)],
    "SIEBEN": [(10,0), (10,1), (10,2), (10,3), (10,4), (10,5)],
    "ACHT": [(10,7), (10,8), (10,9), (10,10)],
    "NEUN": [(11,1), (11,2), (11,3), (11,4)],
    "ZEHN_H": [(11,6), (11,7), (11,8), (11,9)],
    "ELF": [(12,1), (12,2), (12,3)],
    "ZWÖLF": [(12,5), (12,6), (12,7), (12,8), (12,9)]
}


def get_time_in_words():
    current_time = time.localtime()
    stunden = current_time.tm_hour % 12
    minuten = current_time.tm_min

    words = ["ES", "IST"]

    if 0 <= minuten < 1:
        pass
    elif 1 <= minuten < 5:
        words += ["KURZ", "NACH"]
    elif 5 <= minuten < 10:
        words += ["FÜNF", "NACH"]
    elif 10 <= minuten < 15:
        words += ["ZEHN", "NACH"]
    elif 15 <= minuten < 20:
        words += ["VIERTEL", "NACH"]
    elif 20 <= minuten < 25:
        words += ["ZWANZIG", "NACH"]
    elif 25 <= minuten < 30:
        words += ["KURZ", "VOR2", "HALB"]
    elif 30 <= minuten < 33:
        words += ["HALB"] 
    elif 33 <= minuten < 40:
        words += ["KURZ", "NACH2", "HALB"]
    elif 40 <= minuten < 45:
        words += ["ZWANZIG", "VOR"]
    elif 45 <= minuten < 50:
        words += ["VIERTEL", "VOR"]
    elif 50 <= minuten < 55:
        words += ["ZEHN", "VOR"]
    elif 55 <= minuten < 56:
        words += ["FÜNF", "VOR"]
    elif 56 <= minuten < 60:
        words += ["KURZ", "VOR"]

    zeige_stunden = stunden
    if minuten >= 25:
        zeige_stunden = (stunden+1)%12
    if zeige_stunden == 0:
        zeige_stunden = 12
    
    stunden_words = ["EINS", "ZWEI", "DREI", "VIER", "FÜNF_H", "SECHS", "SIEBEN", "ACHT", "NEUN", "ZEHN_H", "ELF", "ZWÖLF"]

    words.append(stunden_words[zeige_stunden-1])
    
    return words


def update_canvas():
    canvas.delete("all")
    highlight_words = get_time_in_words()

    for i, row in enumerate(letters):
        for j, letter in enumerate(row):
            # Funktion um zu prüfen, ob ein Wort ge"highlighted" werden soll.
            highlight = any((i,j) in word_positions[w] for w in highlight_words if w in word_positions)
            color = "red" if highlight else "white"
            canvas.create_text(j*50+25,i*50+25,text=letter,fill=color,font=font)

    
    root.after(1000, update_canvas)


root = tk.Tk()
root.title("Wortuhr")


canvas = tk.Canvas(root, width=550, height=650, bg='black')
canvas.pack()
font = ("Helvetica", 18, "bold")


update_canvas()


root.mainloop()
