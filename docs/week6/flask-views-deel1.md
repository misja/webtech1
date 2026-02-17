# Flask en SQLAlchemy - Theorie

## Database koppeling

Je hebt formulieren gemaakt met Flask-WTF om gebruikersinput te verzamelen. De volgende stap is het opslaan van deze data in een database.

SQLite slaat gegevens op in tabelvorm:

|   |Kolom 1| Kolom 2| Kolom 3
|---|---|---|---|
regel 1| | | |
regel 2| | | |
regel 3| | | |

Voorbeeld met cursisten van de muziekschool. De eerste kolom is het sleutelveld (id) - deze waarde is uniek per rij:

| id	|Voornaam|	Achternaam|	Plaats
|---|--------|------------|--------|
1|	Joyce	|Rooth	|Groningen
2	|Timo |Bijl	|Drachten
3|	Fred|	Timmer|	Assen

In SQL haal je deze gegevens op met `SELECT`:

```sql
SELECT (één of meer velden)
FROM (naam tabel)
```

## ORM - Object Relational Mapper

Flask kan met verschillende SQL databases werken: PostgreSQL, MySQL, SQLite en anderen. Je gebruikt SQLite (hetzelfde als in Week 3).

Om Python en SQL te verbinden gebruik je een **Object Relational Mapper (ORM)**. Een ORM vertaalt tussen Python objecten en database tabellen. Je schrijft Python code, de ORM genereert de SQL.

De meest gebruikte ORM voor Python is **SQLAlchemy**. Voor Flask bestaat er een extensie: **Flask-SQLAlchemy**.

SQLAlchemy voegt een extra laag toe aan je applicatie architectuur:

![Complete architectuur van de webapp](imgs/architectuur.png)

## Installatie

Voeg Flask-SQLAlchemy toe aan je project:

```console
uv add flask-sqlalchemy
```

## CRUD operaties

Met een database voer je vier basis operaties uit - **CRUD**:

operatie | Beschrijving
---|---
`CREATE` | Nieuwe records toevoegen
`READ`   | Gegevens opvragen (`SELECT`)
`UPDATE `| Gegevens wijzigen
`DELETE` | Gegevens verwijderen

## Werkwijze

Om databases in Flask te gebruiken doorloop je deze stappen:

### 1. Database configuratie

- Flask app aanmaken
- SQLAlchemy configureren (database locatie, opties)
- SQLAlchemy koppelen aan je Flask app

Deze configuratie doe je één keer per project.

### 2. Models definiëren

**Models** zijn Python klassen die tabellen representeren. Je schrijft een class, SQLAlchemy maakt de tabel.

Vergelijkbaar met `FlaskForm`, maar dan voor database tabellen:

1. Maak een class
2. Laat het erven van `db.Model`
3. Geef optioneel een tabelnaam op
4. Definieer kolommen als class attributen
5. Voeg `__init__` en `__repr__` methoden toe

### 3. CRUD operaties uitvoeren

Je gebruikt SQLAlchemy methoden om records toe te voegen, op te vragen, te wijzigen en te verwijderen.

In de volgende delen zie je concrete voorbeelden van deze stappen.

**Volgende stap:** [Deel 2](flask-views-deel2.md) - Database setup en models.
