# Context voor AI Agents & Contributors

Dit document beschrijft de ontwerpprincipes, schrijfstijl en architectuur beslissingen voor het Webtechnologie 1 cursusmateriaal. Lees dit **eerst** voordat je wijzigingen maakt.

## Projectdoel

Modernisering van het OOP/Flask cursusmateriaal voor HBO-ICT eerstejaars studenten. Focus op:
- Moderne Python conventies (type annotations, dataclasses)
- Voorbereiding op SQLAlchemy 2.0+ en Flask
- Web-ready code patterns (return values, separation of concerns)
- Pythonic code in plaats van Java-achtige patronen

## Schrijfstijl Principes

### 1. Schrijf naar de student toe

**Goed:**
```markdown
Je gaat nu werken met objecten in Python.
Vanaf nu gebruik je type annotaties standaard.
Je hebt nu twee objecten van de klasse Product.
```

**Fout:**
```markdown
In deze module gaan we werken met objecten.
We gebruiken type annotaties vanaf nu.
We hebben nu twee objecten van de klasse Product.
```

**Regel:** Gebruik consequent "je/jij", nooit "we/wij". De student doet het, niet "wij samen".

### 2. Vermijd docentenperspectief

**Goed:**
```markdown
Later (bij databases en webapplicaties) zijn ze vereist.
In Flask geef je data terug aan de browser.
```

**Fout:**
```markdown
In week 6 gebruiken we SQLAlchemy 2.0.
In de cursus gaan we Flask leren.
SQLAlchemy 2.0 vereist type annotaties (week 6).
```

**Regel:** Geen weeknummers, geen "de cursus", geen verwijzingen naar administratieve structuur. Focus op wat de student moet leren, niet op de cursusindeling.

### 3. Geen onbekende termen als motivatie

**Goed:**
```markdown
Type annotaties zijn nieuw voor je, maar hebben drie grote voordelen:
1. Je ziet direct wat een functie verwacht
2. Je editor helpt je met autocompletion
3. Later (bij databases en webapplicaties) zijn ze vereist
```

**Fout:**
```markdown
Type annotaties zijn belangrijk omdat:
1. Je code wordt duidelijker
2. Je editor kan helpen
3. SQLAlchemy 2.0 vereist ze
```

**Regel:** Motiveer niet met termen die studenten nog niet kennen (SQLAlchemy, ORM, etc.). Gebruik algemene begrippen (databases, webapplicaties).

### 4. Direct en praktisch

**Goed:**
```markdown
Met `class` definieer je een nieuwe klasse.
Methoden kunnen ook berekeningen doen:
```

**Fout:**
```markdown
Laten we eens kijken hoe we een klasse definiëren.
Het interessante van methoden is dat ze ook berekeningen kunnen doen:
```

**Regel:** Kom snel to the point. Geen omslachtige introducties of "laten we..." constructies.

### 5. Natuurlijk Nederlands

**Goed:**
- klassen, objecten, methoden, attributen
- "geeft terug" in plaats van "returnt"
- "Deze methode geeft True terug"

**Fout:**
- classes, objects, methods, attributes
- "returnt" in plaats van "geeft terug"
- "Deze method returnt True"

**Uitzonderingen** (Engels blijft):
- Technische termen zonder goede NL vertaling: constructor, docstring
- Code keywords: `class`, `def`, `return`, `self`
- Framework termen: Flask, SQLAlchemy
- Gangbare jargon: routes, templates, flash (Flask specifiek)

### 6. Geen AI tells

**Vermijd:**
- Emoji (✅ ❌ 🎯 etc.)
- "Oude stijl vs nieuwe stijl" vergelijkingen voor dingen die studenten niet kennen
- Over-enthusiaste taal ("Super!", "Geweldig!", "Perfect!")
- Kunstmatige structuren ("Stap 1, Stap 2, Stap 3...")

**Gebruik:**
- Natuurlijke, professionele docenttaal
- Heldere uitleg zonder overdrijving
- Praktische voorbeelden

## Technische Principes

### 1. Moderne Python vanaf het begin

**Altijd gebruiken:**
- Type annotations voor alle parameters en return types
- Dataclasses waar relevant (data containers)
- F-strings voor formatting
- Type hints uit `typing` waar nodig (`Optional`, `list[]`, etc.)

**Vermijden:**
- Java-achtige getters/setters
- Name mangling (`__private`)
- Underscore prefix (`_protected`) tenzij echt nodig
- Oude string formatting (%, .format())

### 2. Web-ready code patterns

**Altijd:**
```python
def verkoop(self, aantal: int) -> bool:
    if self.voorraad >= aantal:
        self.voorraad -= aantal
        return True
    return False
```

**Nooit:**
```python
def verkoop(self, aantal: int) -> None:
    if self.voorraad >= aantal:
        self.voorraad -= aantal
        print("Verkocht!")  # ❌ Print in business logic
    else:
        print("Onvoldoende voorraad")  # ❌
```

**Regel:** Business logic returnt values, geen print statements. Dit is essentieel voor Flask.

### 3. Separation of concerns

Studenten moeten vanaf het begin leren dat:
- **Models/Classes**: Business logic, data, berekeningen → RETURN values
- **Routes/Controllers**: HTTP handling, user feedback → PRINT/FLASH
- **Templates**: Presentatie

## Curriculumarchitectuur

### Week 2: OOP Focus

**Doel:** Voorbereiden op SQLAlchemy en Flask, niet algemene OOP mastery.

**Wat moet:**
- Klassen en objecten begrijpen
- Type annotations gebruiken
- Inheritance basics (voor `db.Model`)
- Object relaties (voorbereiding FK's)

**Wat NIET:**
- Complexe OOP patterns
- Getters/setters
- Properties (tenzij kort)
- Abstracte base classes
- Multiple inheritance

### Rode draad

**Consistent voorbeeld:** Webshop (Product, Klant, Bestelling)

**Progressie:**
1. **Deel 1:** Basic classes met type annotations
2. **Deel 2:** Dataclasses + validatie (Pydantic)
3. **Deel 3:** Inheritance basics
4. **Deel 4:** Object relaties

**Elk deel:**
- Preview naar SQLAlchemy/Flask waar relevant
- Praktische oefening
- Code die overdraagbaar is naar web context

## Admonitions Gebruik

MkDocs Material ondersteunt verschillende admonition types. Gebruik ze strategisch:

### `!!! info`
Voor nieuwe concepten die uitleg verdienen:
```markdown
!!! info "Waarom type annotaties?"
    Type annotaties zijn nieuw voor je, maar hebben drie grote voordelen:
    1. ...
```

### `!!! note`
Voor belangrijke details die opvallen:
```markdown
!!! note "`self` - het object zelf"
    `self` verwijst naar het object zelf. Wanneer je...
```

### `!!! warning`
Voor cruciale verschillen of waarschuwingen:
```markdown
!!! warning "Print vs Return in webapplicaties"
    De `verkoop()` methode geeft een boolean terug...
```

### `!!! tip`
Voor handige technieken:
```markdown
!!! tip "Default waarden"
    `btw_percentage: float = 21.0` is een default waarde...
```

**Regel:** Gebruik spaarzaam. Alleen voor echt belangrijke concepten die extra aandacht verdienen.

## Code Voorbeelden

### Structuur

```python
class Product:
    """Korte beschrijving."""

    def __init__(self, naam: str, prijs: float):
        self.naam = naam
        self.prijs = prijs

    def bereken_totaal(self, aantal: int) -> float:
        """Docstring met wat de methode doet."""
        return self.prijs * aantal
```

**Altijd:**
- Class docstring bovenaan
- Type annotations overal
- Methode docstrings waar functionaliteit niet obvious is
- Return types, ook voor `None`
- Betekenisvolle variabele namen

### Voorbeelddata

**Gebruik realistische waardes:**
```python
laptop = Product("Laptop", 799.99, 5)
muis = Product("Draadloze muis", 25.50, 20)
```

**Niet:**
```python
product1 = Product("Product A", 10.0, 5)
product2 = Product("Product B", 20.0, 10)
```

## Pull Request Workflow

### Branching

```
main (productie - deployed naar GitHub Pages)
  └── feature/oop-modernisering
        ├── feature/oop-deel1-herschrijven
        ├── feature/oop-deel2-dataclasses
        └── ...
```

### Commits

**Goed:**
```
Herschrijf OOP deel 1: moderne Python + type annotations

- Verwijder Java-achtige getters/setters
- Voeg type annotations toe overal
- Return values i.p.v. print statements
- Schrijfstijl: naar student toe, geen docentenperspectief
```

**Fout:**
```
Update oop-deel1.md
```

### PR's voor review

Alle wijzigingen via PR's:
- Collega-docenten kunnen reviewen
- Beslissen wanneer te mergen (dit jaar / volgend jaar)
- Discussie mogelijk over aanpak

## Technische Setup

### Dependencies

```toml
[project]
dependencies = [
    "mkdocs>=1.6.0",
    "mkdocs-material>=9.5.0",
    "pymdown-extensions>=10.11.0",
    "mknotebooks>=0.8.0",
]
```

### Development

```bash
# Setup
uv sync

# Live preview
uv run mkdocs serve

# Build
uv run mkdocs build
```

### File conventies

- Nieuwe versies: `oop-deel1-nieuw.md` (voor vergelijking)
- Na merge: hernoemen naar `oop-deel1.md`
- Oefeningen: `oefeningen/oop-oefening1.md`
- Bestanden: `bestanden/voorbeeld.py`

## Checklist voor nieuwe content

Voordat je content indient:

- [ ] Geschreven naar student toe (je/jij, geen we/wij)
- [ ] Geen docentenperspectief (weeknummers, cursusstructuur)
- [ ] Type annotations overal in code voorbeelden
- [ ] Return values in plaats van print in business logic
- [ ] Nederlandse termen waar mogelijk (klassen, methoden, objecten)
- [ ] Geen emoji of AI tells
- [ ] Admonitions alleen voor belangrijke concepten
- [ ] Realistische voorbeelddata
- [ ] Docstrings in code voorbeelden
- [ ] Link naar SQLAlchemy/Flask waar relevant (zonder jargon)
- [ ] Code is web-ready (separation of concerns)

## Flask Terminologie

Wanneer je over Flask schrijft:

**Blijft Engels:**
- routes (gangbaar in NL)
- templates (gangbaar)
- flash (Flask functie)
- request, response

**Wordt Nederlands:**
- models → **modellen**
- forms → **formulieren**
- views → **weergaven** (of houd "views" als gangbaar?)

**Nog te bepalen:** Consistente keuzes maken bij verdere materialen.

## Vragen?

Bij twijfel over stijlkeuzes:
1. Lees voorbeelden in deze guide
2. Bekijk bestaande herschreven materialen
3. Vraag in PR comments

**Kerndoel:** Studenten voorbereiden op moderne Flask development met helder, natuurlijk Nederlands lesmateriaal.
