import os
import re
from collections import Counter
from clp3 import clp

folder_path = "teksty"
file_list = [f for f in os.listdir(folder_path) if f.endswith(".txt")]

# liczniki
counter_all = Counter()
counter_first_half = Counter()   # 001-050
counter_second_half = Counter()  # 051-100

for filename in file_list:
    file_number = int(filename.replace(".txt", ""))
    file_path = os.path.join(folder_path, filename)
    
    with open(file_path, "rt", encoding="utf-8") as f:
        text = f.read().lower()
    
    # usunięcie znaków niealfabetycznych
    text = re.sub(r"[^a-zA-Ząćęłńóśźż\s]", "", text)

    words = text.split()
    normalized_words = []

    for w in words:
        ids = clp.rec(w)
        if ids:
            base = clp.bform(ids[0])
            normalized_words.append(base)
        else:
            normalized_words.append(w)

    # zliczanie słów
    licznik = Counter(normalized_words)

    # aktualizacja liczników globalnych
    for word, count in licznik.items():
        counter_all[word] += count
        if 1 <= file_number <= 50:
            counter_first_half[word] += count
        elif 51 <= file_number <= 100:
            counter_second_half[word] += count

# formatowanie liczników do typu csv
def save_counter_clp(counter_obj, filename):
    with open(filename, "w", encoding="utf-8") as f:
        f.write("lp,slowo,liczba,etykieta\n")
        for i, (word, count) in enumerate(counter_obj.most_common(), start=1):
            ids = clp.rec(word)
            etykieta = clp.label(ids[0]) if ids else "-"
            f.write(f"{i},{word},{count},{etykieta}\n")

# zapis plików csv
save_counter_clp(counter_all, "lista_frekwencyjna_clp_wszystkie.csv")
save_counter_clp(counter_first_half, "lista_frekwencyjna_clp_na_temat.csv")
save_counter_clp(counter_second_half, "lista_frekwencyjna_clp_nie_na_temat.csv")