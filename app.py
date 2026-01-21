from flask import Flask, render_template, request
import os
import re

# próba zaimportowania CLP
try:
    from clp3 import clp
    CLP_AVAILABLE = True
except Exception:
    clp = None
    CLP_AVAILABLE = False
    print("wersja bez CLP")

app = Flask(__name__)

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

# funkcje pomocnicze CLP
def get_all_forms(word):
    forms = set()

    if CLP_AVAILABLE:
        try:
            ids = clp.rec(word)
            if ids:
                for f in clp.forms(ids[0]):
                    forms.add(f.lower())
        except Exception:
            pass

    if not forms:
        forms.add(word.lower())

    return forms

class Text:
    def __init__(self, text, filename):
        self.text = text
        self.filename = filename
        self.categories = []
        self.category_sum = 0


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
        for text_obj in self.texts:
            for key, (words, weight, color) in keyword_dict.items():

                all_forms = set()
                for word in words:
                    all_forms.update(get_all_forms(word))

                for form in all_forms:
                    pattern = fr'(?<!\w)({re.escape(form)})(?!\w)'

                    def repl(match):
                        if key not in text_obj.categories:
                            text_obj.categories.append(key)
                            text_obj.category_sum += weight
                        return (
                            f'<span style="background-color: {color}; font-weight:bold;">'
                            f'{match.group(0)}</span>'
                        )

                    text_obj.text = re.sub(
                        pattern,
                        repl,
                        text_obj.text,
                        flags=re.IGNORECASE
                    )


all_texts = AllTexts(folder='teksty')
all_texts.run()

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

    category_colors = {k: v[2] for k, v in keyword_dict.items()}

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
        filename = "lista_frekwencyjna_wszystkie.csv"
    elif lista_typ == "na_temat":
        filename = "lista_frekwencyjna_na_temat.csv"
    elif lista_typ == "nie_na_temat":
        filename = "lista_frekwencyjna_nie_na_temat.csv"
    else:
        return "nieznany typ listy", 404

    import csv
    with open(filename, "r", encoding="utf-8") as f:
        slowa = list(csv.DictReader(f))

    return render_template("words_table.html", words=slowa, title=lista_typ)


if __name__ == "__main__":
    app.run(
        host='0.0.0.0',
        port=12221,
        debug=True
    )