import os
import re
from flask import Flask, render_template

app = Flask(__name__)

# Słowa, które chcemy podświetlać
KEYWORDS = ["Breivik", "anders", "utoya"]

@app.route("/")
def home():
    texts = []

    # Numeryczne sortowanie plików
    files = sorted(
        os.listdir("teksty"),
        key=lambda f: int(f.replace(".txt", ""))  # sortowanie po numerze
    )

    for file in files:
        with open(f"teksty/{file}", encoding="utf-8") as f:
            content = f.read()

        score = 0
        highlighted_content = content  # nowy tekst z podświetleniami

        for kw in KEYWORDS:
            # regex nieczuły na wielkość liter
            pattern = re.compile(re.escape(kw), re.IGNORECASE)
            
            # zliczanie wystąpień
            matches = pattern.findall(content)
            score += len(matches)

            # podświetlanie w tekście
            highlighted_content = pattern.sub(
                lambda m: f"<span style='background: yellow; font-weight: bold;'>{m.group(0)}</span>",
                highlighted_content
            )

        texts.append({
            "filename": file,
            "content": highlighted_content,
            "score": score
        })

    return render_template("index.html", texts=texts)


if __name__ == "__main__":
    app.run(debug=True)