import os
import re
from collections import Counter

# próba zaimportowania CLP
try:
    from clp3 import clp
    CLP_AVAILABLE = True
except Exception:
    clp = None
    CLP_AVAILABLE = False
    print("wersja bez CLP")

# funkcje pomocnicze CLP
def normalize_word(word):
    if CLP_AVAILABLE:
        try:
            ids = clp.rec(word)
            if ids:
                return clp.bform(ids[0])
        except Exception:
            pass
    return word

def get_label(word):
    if CLP_AVAILABLE:
        try:
            ids = clp.rec(word)
            if ids:
                return clp.label(ids[0])
        except Exception:
            pass
    return "-"

folder_path = "teksty"
file_list = [f for f in os.listdir(folder_path) if f.endswith(".txt")]

merge_map = {
    'utöya': 'utøya',
    'utoyę': 'utøya',
    'utoeya': 'utøya',
    'utøya': 'utøya',
    'utoya': 'utøya',
    'utoyi': 'utøya',
    'utoi': 'utøya'
}

STOPWORDS = {"się", "być"}

counter_all = Counter()
counter_first_half = Counter()
counter_second_half = Counter()

for filename in file_list:
    file_number = int(filename.replace(".txt", ""))
    file_path = os.path.join(folder_path, filename)

    with open(file_path, "rt", encoding="utf-8") as f:
        text = f.read().lower()

    text = re.sub(r'[^a-zA-ZąćęłńóśżźĄĆĘŁŃÓŚŻŹøØ\s]', ' ', text)

    for form, merged in merge_map.items():
        text = text.replace(form, merged)

    words = text.split()
    normalized_words = [normalize_word(w) for w in words]

    licznik = Counter(normalized_words)

    for word, count in licznik.items():
        counter_all[word] += count
        if 1 <= file_number <= 50:
            counter_first_half[word] += count
        elif 51 <= file_number <= 100:
            counter_second_half[word] += count


def save_counter(counter_obj, filename):
    with open(filename, "w", encoding="utf-8") as f:
        f.write("lp,słowo,liczba,etykieta\n")
        i = 1

        for word, count in counter_obj.most_common():
            if word in STOPWORDS:
                continue

            label = get_label(word)

            if CLP_AVAILABLE and "G" in label:
                continue

            f.write(f"{i},{word},{count},{label}\n")
            i += 1


save_counter(counter_all, "lista_frekwencyjna_wszystkie.csv")
save_counter(counter_first_half, "lista_frekwencyjna_na_temat.csv")
save_counter(counter_second_half, "lista_frekwencyjna_nie_na_temat.csv")