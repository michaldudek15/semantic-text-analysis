from flask import Flask, render_template
import csv

app = Flask(__name__)
keyword_dict = {
    'Sprawca': (['anders', 'andersa', 'andersowi', 'andersem', 'andersie', 
                'Anders', 'Andersa', 'Andersowi', 'Andersem', 'Andersie',
                'breivik', 'breivika', 'breivikowi', 'breivikiem', 'breiviku',
                'Breivik', 'Breivika', 'Breivikowi', 'Breivikiem', 'Breviviku',
                'zamachowiec', 'terrorysta', 'oskarżony', 'radykał','ekstremista'],
                0.25, "#ff0000"),
    'Zdarzenie': (['zamach', 'atak', 'eksplozja', 'strzelanina', 'masakra', 'terroryzm', 'zastrzelić'],
                  0.2, "#f70893"),
    'Obiekt': (['młodzież', 'imigrant', 'zabity', 'ofiara', 'uczestnik', 'ranny', 'cywil', 'dziecko'],
               0.15, "#8300fe"),
    'Narzędzie': (['broń', 'ładunek', 'materiał', 'środki', 'pistolet', 'karabin', 'pojazd', 'ciężarówka', 'samochód'],
                  0.1, "#00a2ff"),
    'Miejsce': (['norwegia', 'norwegii', 'norwegię', 'norwegią', 'norwegio',
                 'Norwegia', 'Norwegii', 'Norwegię', 'Norwegią', 'Norwegio',
                 'oslo',
                 'Oslo',
                 'utøya', 'utøyi', 'utøyę', 'utøyą', 'utøyo',
                 'Utøya', 'Utøyi', 'Utøyę', 'Utøyą', 'Utøyo',
                 'utoya', 'utoyi', 'utoyę', 'utoyą', 'utoyo',
                 'Utoya', 'Utoyi', 'Utoyę', 'Utoyą', 'Utoyo',
                 'wyspa'],
                0.2, "#04ff08"),
    'Cel': (['ideologia', 'polityka', 'system', 'ekstremizm', 'manifest', 'przekaz', 'symbol', 'społeczeństwo', 'demokracja', 'radykalizm'],
            0.1, "#b7d51f"),
}
znaki = "`.,;~!?  "


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

@app.route("/weights")
def weights():
    # Strona z przyciskami do wyboru listy
    return render_template("weights.html")

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