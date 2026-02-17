# Flask en SQLAlchemy - CRUD operaties

## 3. CRUD operaties (`basic_CRUD.py`)

Je hebt de database en model aangemaakt. Nu voer je de vier basis operaties uit: **Create, Read, Update, Delete**.

Bestudeer het volledige bestand [`basic_CRUD.py`](bestanden/crud/basic_CRUD.py).

!!! note "Vereenvoudigd voorbeeld"
    Dit script toont de basis CRUD operaties. In een echte Flask applicatie gebruik je routes en templates in plaats van losse scripts.

## CREATE - Records toevoegen

```python
from basic_model_app import db, Cursist

# Maak nieuw object aan
elsje = Cursist('Elsje', 19)

# Voeg toe aan database sessie
db.session.add(elsje)

# Schrijf naar database
db.session.commit()
```

Drie stappen: object maken, toevoegen aan sessie, committen.

## READ - Gegevens opvragen

### Alle records ophalen

```python
alle_cursisten = Cursist.query.all()
print(*alle_cursisten, sep='\n')
```

`Cursist.query.all()` geeft een lijst met alle cursisten terug. De tekst komt uit de `__repr__()` methode.

Output:

```console
Cursist Joyce is 40 jaar oud
Cursist Bram is 24 jaar oud
Cursist Elsje is 19 jaar oud
```

### Specifiek record ophalen op ID

```python
cursist_twee = Cursist.query.get(2)
print(cursist_twee)
print(cursist_twee.leeftijd)
```

`Cursist.query.get(2)` haalt het record op met `id = 2`.

Output:

```console
Cursist Bram is 24 jaar oud
24
```

Je kunt direct attributen ophalen zoals `cursist_twee.leeftijd` of `cursist_twee.naam`.

!!! info "Query API"
    SQLAlchemy biedt veel query methoden:

    - `Model.query.all()` - Alle records
    - `Model.query.get(id)` - Record op ID
    - `Model.query.filter_by(naam='Joyce')` - Filteren op attribuut
    - `Model.query.first()` - Eerste record

## UPDATE - Gegevens wijzigen

```python
# Haal record op
cursist_joyce = Cursist.query.get(1)

# Wijzig attribuut
cursist_joyce.leeftijd = 40

# Voeg toe aan sessie
db.session.add(cursist_joyce)

# Schrijf wijziging naar database
db.session.commit()
```

Vier stappen:

1. Record ophalen met `query.get()`
2. Attribuut wijzigen
3. Toevoegen aan sessie
4. Committen

!!! tip "Update zonder add"
    Je kunt `db.session.add()` ook weglaten bij updates. SQLAlchemy houdt bij welke objecten gewijzigd zijn:

    ```python
    cursist_joyce = Cursist.query.get(1)
    cursist_joyce.leeftijd = 40
    db.session.commit()  # Dit werkt ook
    ```

## DELETE - Records verwijderen

```python
# Haal record op
cursist_elsje = Cursist.query.get(3)

# Verwijder uit database
db.session.delete(cursist_elsje)

# Schrijf wijziging naar database
db.session.commit()
```

Drie stappen:

1. Record ophalen
2. `delete()` aanroepen
3. Committen

Na deze wijzigingen blijven deze records over:

```console
Cursist Joyce is 40 jaar oud
Cursist Bram is 24 jaar oud
```

## Overzicht CRUD patterne

| Operatie | Code patroon |
|----------|-------------|
| **Create** | `obj = Model(...)`<br>`db.session.add(obj)`<br>`db.session.commit()` |
| **Read** | `Model.query.all()`<br>`Model.query.get(id)` |
| **Update** | `obj = Model.query.get(id)`<br>`obj.attribuut = nieuwe_waarde`<br>`db.session.commit()` |
| **Delete** | `obj = Model.query.get(id)`<br>`db.session.delete(obj)`<br>`db.session.commit()` |

!!! warning "Altijd committen"
    Vergeet `db.session.commit()` niet! Zonder commit worden wijzigingen niet opgeslagen in de database.

**Volgende stap:** [Deel 4](flask-views-deel4.md) - Relaties tussen tabellen.
