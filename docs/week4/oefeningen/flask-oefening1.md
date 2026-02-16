# Flask Oefening 1: Artiestennaam Generator

Deze oefening hoort bij [Flask Deel 3](../flask-deel3.md) en [Deel 4](../flask-deel4.md).

## Achtergrond

Veel cursisten van de muziekschool dromen van een carrière in de muziek. Voor de meesten hoort daar een gave artiestennaam bij! In deze oefening bouw je een **artiestennaam generator** die automatisch een artiestennaam maakt op basis van de echte naam.

## De regels

De artiestennaam wordt als volgt gegenereerd:

1. **Eindigt de naam op `s`?** → Voeg `SY` toe
2. **Eindigt de naam op iets anders?** → Voeg `TEZY` toe
3. **Converteer naar hoofdletters** (de artiestennaam)

**Voorbeelden:**
- `Truus` → `TRUUSSY`
- `Rob` → `ROBTEZY`
- `Joyce` → `JOYCETEZY`
- `Thomas` → `THOMASSY`

## Opdracht

Maak een Flask applicatie met een dynamische route die een artiestennaam genereert.

### Vereisten

✅ **Route**: `http://localhost:5000/artiestennaam/<naam>`
✅ **Template**: Gebruik Jinja2 template (niet HTML in string!)
✅ **Type hints**: Gebruik moderne Python type hints
✅ **Logica**: Implementeer de naam-generatie regels correct
✅ **Project setup**: Gebruik `uv` zoals in Week 2/3/4

## Stappenplan

### Stap 1: Project setup

```console
mkdir artiestennaam-generator
cd artiestennaam-generator
uv init
uv add flask
```

### Stap 2: Template aanmaken

Maak directory en template:

```console
mkdir templates
```

Maak `templates/artiestennaam.html`:

```html
<!DOCTYPE html>
<html lang="nl">
    <head>
        <meta charset="UTF-8">
        <title>Artiestennaam Generator</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                max-width: 600px;
                margin: 50px auto;
                padding: 20px;
                text-align: center;
            }
            .artist-name {
                font-size: 3em;
                color: #e91e63;
                font-weight: bold;
                margin: 30px 0;
            }
            .normal-name {
                font-size: 1.2em;
                color: #666;
            }
        </style>
    </head>
    <body>
        <h1>🎤 Artiestennaam Generator 🎸</h1>

        <p class="normal-name">Echte naam: {{ TODO }}</p>
        <p class="artist-name">{{ TODO }}</p>

        <p>
            <a href="/">Genereer een nieuwe naam</a>
        </p>
    </body>
</html>
```

**TODO:** Vul de `{{ TODO }}` placeholders in met de juiste variabelen!

### Stap 3: Flask app schrijven

Maak `app.py`:

```python
from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def index() -> str:
    """Homepage met instructies."""
    # TODO: Implementeer deze route
    # Geef een simpele HTML string terug met uitleg
    pass


@app.route("/artiestennaam/<naam>")
def artiestennaam(naam: str) -> str:
    """Genereer artiestennaam op basis van echte naam.

    Regels:
    - Naam eindigt op 's' → voeg 'SY' toe
    - Anders → voeg 'TEZY' toe
    - Converteer naar hoofdletters

    Args:
        naam: De echte naam van de cursist

    Returns:
        HTML met gegenereerde artiestennaam
    """
    # TODO: Implementeer de logica
    # 1. Check of naam eindigt op 's'
    # 2. Voeg juiste suffix toe
    # 3. Converteer naar uppercase
    # 4. Render template met beide namen

    pass


if __name__ == "__main__":
    app.run(debug=True)
```

### Stap 4: Implementatie tips

**Hint 1 - Check laatste letter:**
```python
if naam.lower().endswith('s'):
    # Eindigt op 's'
else:
    # Eindigt op iets anders
```

**Hint 2 - String concatenatie:**
```python
artiestennaam = naam + suffix
```

**Hint 3 - Uppercase:**
```python
artiestennaam = artiestennaam.upper()
```

**Hint 4 - Template renderen:**
```python
return render_template(
    "artiestennaam.html",
    echte_naam=naam,
    artiest_naam=artiestennaam
)
```

### Stap 5: Testen

Run je app:

```console
uv run python app.py
```

Test met verschillende namen:
- `http://localhost:5000/artiestennaam/Truus` → TRUUSSY
- `http://localhost:5000/artiestennaam/Rob` → ROBTEZY
- `http://localhost:5000/artiestennaam/Joyce` → JOYCETEZY
- `http://localhost:5000/artiestennaam/Thomas` → THOMASSY

## Bonusopdracht 1: Homepage met voorbeelden

Maak de `/` route dynamischer met een template die voorbeelden toont:

**`templates/index.html`:**
```html
<!DOCTYPE html>
<html lang="nl">
    <head>
        <meta charset="UTF-8">
        <title>Artiestennaam Generator</title>
    </head>
    <body>
        <h1>🎤 Artiestennaam Generator</h1>
        <p>Genereer jouw artiestennaam!</p>

        <h2>Voorbeelden:</h2>
        <ul>
            {% for naam in voorbeelden %}
                <li>
                    <a href="/artiestennaam/{{ naam }}">{{ naam }}</a>
                </li>
            {% endfor %}
        </ul>

        <h2>Probeer zelf:</h2>
        <p>Ga naar: <code>/artiestennaam/&lt;jouw-naam&gt;</code></p>
    </body>
</html>
```

**Update `app.py`:**
```python
@app.route("/")
def index() -> str:
    """Homepage met voorbeelden."""
    voorbeelden = ["Truus", "Rob", "Joyce", "Thomas", "Rens"]
    return render_template("index.html", voorbeelden=voorbeelden)
```

## Bonusopdracht 2: Template inheritance

Maak een `base.html` template en gebruik deze in beide pagina's:

**`templates/base.html`:**
```html
<!DOCTYPE html>
<html lang="nl">
    <head>
        <meta charset="UTF-8">
        <title>{% block title %}Artiestennaam Generator{% endblock %}</title>
        <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
    </head>
    <body>
        <nav>
            <a href="/">Home</a>
        </nav>

        <main>
            {% block content %}{% endblock %}
        </main>

        <footer>
            <p>&copy; 2024 Muziekschool Session</p>
        </footer>
    </body>
</html>
```

Update `artiestennaam.html` en `index.html` om `base.html` te extenden:

```html
{% extends "base.html" %}

{% block title %}{{ echte_naam }} - Artiestennaam{% endblock %}

{% block content %}
    <!-- Je huidige content hier -->
{% endblock %}
```

##Bonusopdracht 3: CSS styling

Maak `static/style.css`:

```console
mkdir static
```

**`static/style.css`:**
```css
body {
    font-family: 'Arial', sans-serif;
    max-width: 800px;
    margin: 0 auto;
    padding: 20px;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
}

.artist-name {
    font-size: 4em;
    font-weight: bold;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    animation: pulse 2s infinite;
}

@keyframes pulse {
    0%, 100% { transform: scale(1); }
    50% { transform: scale(1.05); }
}

a {
    color: #ffd700;
    text-decoration: none;
    font-weight: bold;
}

a:hover {
    text-decoration: underline;
}
```

## Bonusopdracht 4: Formulier toevoegen

Voeg een formulier toe zodat gebruikers hun naam kunnen invoeren zonder URL aan te passen:

**Update `index.html`:**
```html
<form action="/genereer" method="POST">
    <label for="naam">Jouw naam:</label>
    <input type="text" id="naam" name="naam" required>
    <button type="submit">Genereer!</button>
</form>
```

**Update `app.py`:**
```python
from flask import Flask, render_template, request, redirect, url_for

@app.route("/genereer", methods=["POST"])
def genereer() -> str:
    """Handle form submission en redirect naar artiestennaam route.

    Returns:
        Redirect naar artiestennaam route met ingevoerde naam
    """
    naam = request.form.get("naam", "")
    if naam:
        return redirect(url_for("artiestennaam", naam=naam))
    return redirect(url_for("index"))
```

## Verwachte Output

### Basis opdracht

**URL:** `http://localhost:5000/artiestennaam/Truus`

**Output:**
```
🎤 Artiestennaam Generator 🎸

Echte naam: Truus
TRUUSSY

← Genereer een nieuwe naam
```

## Checklist

✅ Project aangemaakt met `uv init` en `uv add flask`
✅ `templates/` directory met `artiestennaam.html`
✅ Flask route op `/artiestennaam/<naam>`
✅ Type hints gebruikt (`naam: str`, `-> str`)
✅ Logica correct:
- Naam eindigt op `s` → voeg `SY` toe
- Anders → voeg `TEZY` toe
- Converteer naar uppercase
✅ Template gebruikt (geen HTML in string!)
✅ Docstring bij route functie
✅ Werkt met verschillende namen

## Veelvoorkomende fouten

❌ **HTML in string returnen**
```python
return f"<h1>{artiestennaam}</h1>"  # FOUT!
```
✅ **Template gebruiken**
```python
return render_template("artiestennaam.html", ...)  # GOED!
```

❌ **Geen type hints**
```python
def artiestennaam(naam):  # FOUT!
```
✅ **Type hints toevoegen**
```python
def artiestennaam(naam: str) -> str:  # GOED!
```

❌ **Case-sensitive check**
```python
if naam.endswith('s'):  # FOUT! "Truus" != "truuS"
```
✅ **Case-insensitive check**
```python
if naam.lower().endswith('s'):  # GOED!
```

## Samenvatting

Na deze oefening heb je:

- ✅ Een Flask project opgezet met `uv`
- ✅ Dynamische routes gebruikt met URL parameters
- ✅ Templates gemaakt met Jinja2
- ✅ Type hints toegepast in Flask routes
- ✅ String manipulatie in Python gedaan
- ✅ Modern project structuur gebruikt (zoals Week 2/3)

**Tip:** Deze patterns gebruik je de rest van de cursus! In Week 5 leer je forms (gebruikersinput), en in Week 6 databases (SQLAlchemy).
