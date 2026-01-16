from flask import Flask, render_template
import csv

app = Flask(__name__)

# Funkcja do wczytania CSV do listy słów
def load_csv(filename):
    lista = []
    with open(filename, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            lista.append(row)
    return lista

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/word_lists")
def word_lists():
    # Strona z przyciskami do wyboru listy
    return render_template("word_lists.html")

@app.route("/word_lists/<lista_typ>")
def show_words(lista_typ):
    # Wybór pliku CSV w zależności od przycisku
    if lista_typ == "wszystkie":
        filename = "lista_frekwencyjna_clp_wszystkie.csv"
    elif lista_typ == "na_temat":
        filename = "lista_frekwencyjna_clp_na_temat.csv"
    elif lista_typ == "nie_na_temat":
        filename = "lista_frekwencyjna_clp_nie_na_temat.csv"
    else:
        return "Nieznany typ listy", 404

    words = load_csv(filename)
    return render_template("words_table.html", words=words, title=lista_typ)