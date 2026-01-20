from flask import Flask, render_template, request
import os
import re
from clp3 import clp as clp

app = Flask(__name__)

# słowa kluczowe, wagi i kolory ról semantycznych
keyword_dict = {
    'Sprawca': (['anders', 'andersa', 'andersowi', 'andersem', 'andersie', 
                'breivik', 'breivika', 'breivikowi', 'breivikiem', 'breiviku',
                'zamachowiec', 'terrorysta', 'oskarżony', 'radykał','ekstremista'],
                0.3, "#ff0000"),
    'Zdarzenie': (['zamach', 'atak', 'eksplozja', 'strzelanina', 'masakra', 'terroryzm', 'zastrzelić'],
                  0.2, "#f70893"),
    'Obiekt': (['młodzież', 'imigrant', 'zabity', 'ofiara', 'uczestnik', 'ranny', 'cywil', 'dziecko'],
               0.15, "#8300fe"),
    'Narzędzie': (['broń', 'ładunek', 'materiał', 'pistolet', 'karabin', 'pojazd', 'ciężarówka', 'samochód'],
                  0.1, "#00a2ff"),
    'Miejsce': (['norwegia', 'norwegii', 'norwegię', 'norwegią', 'norwegio',
                 'oslo',
                 'utøya', 'utøyi', 'utøyę', 'utøyą', 'utøyo',
                 'utoya', 'utoyi', 'utoyę', 'utoyą', 'utoyo', 'utoi',
                 'wyspa'],
                0.2, "#04ff08"),
    'Cel': (['ideologia', 'polityka', 'system', 'ekstremizm', 'manifest', 'przekaz', 'symbol', 'społeczeństwo', 'demokracja', 'radykalizm'],
            0.1, "#b7d51f"),
}

# klasa pojedynczego tekstu
class Text:
    def __init__(self, text, filename):
        self.text = text
        self.filename = filename
        self.categories = []
        self.category_sum = 0

# klasa korpusu tekstów
class AllTexts:
    def __init__(self, folder='teksty'):
        self.folder = folder
        self.texts = []

    def run(self):
        self.read_texts()
        self.analyze_texts()

    def read_texts(self):
        for file in os.listdir(self.folder):
            if file.endswith(".txt"):
                with open(f"{self.folder}/{file}", "r", encoding="utf-8") as f:
                    self.texts.append(Text(f.read(), file))

    def analyze_texts(self):
        for text_obj in self.texts: # dla każdego tekstu z korpusu
            for key, (words, weight, color) in keyword_dict.items(): # dla każdej kategorii
                all_forms = set()
                for word in words: # dla każdego słowa kluczowego
                    try:
                        forms = clp.forms(clp.rec(word)[0]) # pobranie wszystkich form fleksyjnych
                        all_forms.update(w.lower() for w in forms) # dodanie form do zbioru
                    except Exception:
                        all_forms.add(word.lower())

                for form in all_forms: # dla każdej formy słowa kluczowego
                    pattern = fr'(?<!\w)({re.escape(form)})(?!\w)'
                    
                    def repl(match): # funkcja kolorująca znalezione słowa
                        if key not in text_obj.categories:
                            text_obj.categories.append(key)
                            text_obj.category_sum += weight
                        return f'<span style="background-color: {color}; font-weight:bold;">{match.group(0)}</span>'
                    
                    text_obj.text = re.sub(pattern, repl, text_obj.text, flags=re.IGNORECASE)
    
all_texts = AllTexts(folder='teksty')
all_texts.run()

# trasy Flaska
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/texts")
def texts():
    sort_by = request.args.get('sort_by', 'category_sum')
    sort_order = request.args.get('sort_order', 'desc')

    texts_list = all_texts.texts.copy()
    reverse = sort_order == 'desc'

    if sort_by == 'category_sum':
        texts_list.sort(key=lambda x: x.category_sum, reverse=reverse)
    elif sort_by == 'filename':
        texts_list.sort(key=lambda x: int(x.filename[:-4]), reverse=reverse)

    # mapa kolorów kategorii do template
    category_colors = { key: value[2] for key, value in keyword_dict.items() }

    return render_template(
        "texts.html",
        texts=texts_list,
        sort_by=sort_by,
        sort_order=sort_order,
        category_colors=category_colors
    )

@app.route("/word_lists")
def word_lists():
    return render_template("word_lists.html")

@app.route("/weights")
def weights():
    return render_template("weights.html")

@app.route("/word_lists/<lista_typ>")
def show_words(lista_typ):
    if lista_typ == "wszystkie":
        filename = "lista_frekwencyjna_clp_wszystkie.csv"
    elif lista_typ == "na_temat":
        filename = "lista_frekwencyjna_clp_na_temat.csv"
    elif lista_typ == "nie_na_temat":
        filename = "lista_frekwencyjna_clp_nie_na_temat.csv"
    else:
        return "Nieznany typ listy", 404

    import csv
    with open(filename, "r", encoding="utf-8") as f:
        slowa = list(csv.DictReader(f))

    return render_template("words_table.html", words=slowa, title=lista_typ)

# uruchomienie serwera aplikacji
if __name__ == "__main__":
    app.run(
        host='0.0.0.0',
        port=12221,
        debug=True
    )