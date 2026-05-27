# semantic text analysis (Flask + CLP)
> this web application is a course project for the "Information Extraction" class

a lightweight Python web application for semantic analysis of text corpus, focused on the 2011 Norway attacks, carried out by Anders Behring Breivik

the app highlights semantic roles directly in the text, computes topic relevance scores, and displays word frequency lists

designed to work with or without the university's CLP morphological analyzer by Paweł Chrząszcz



## features
- semantic role detection
- color-coded highlighting in text
- topic relevance scoring per document
- sorting texts by relevance or filename
- word frequency lists (CSV-based)
- automatic fallback when CLP is unavailable

## text corpus
- 50 polish texts related to the Breivik attack
- 50 polish texts unrelated to the topic
- the texts were collected from the internet – I do not claim ownership, they are used for educational purposes

## running the application

### prerequisites
- Python 3.9+ installed
- `pip` available in your environment

### 1. Create and activate a virtual environment
```bash
python3 -m venv .venv
source .venv/bin/activate
```
### 2. install dependencies
```bash
pip install flask
```

### 3. start the app
```bash
python3 app.py
```
