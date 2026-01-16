import os
import re
from collections import Counter

folder_path = "teksty"
file_list = [f for f in os.listdir(folder_path) if f.endswith(".txt")]

counter = Counter()

for filename in file_list:
    file_path = os.path.join(folder_path, filename)
    with open(file_path, "rt", encoding="utf-8") as file:
        text = file.read()

    for word in text.split():
        word = re.sub(r"[^a-zA-Ząćęłóśżź_]", "", word).lower()
        if word:
            counter[word] += 1

with open("lista_frekwencyjna.csv", "w", encoding="utf-8") as f:
    f.write("lp,slowo,liczba\n")
    for i, (word, count) in enumerate(counter.most_common(), start=1):
        f.write(f"{i},{word},{count}\n")