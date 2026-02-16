# SQLite in Python

In het vak Databases heb je geleerd werken met PostgreSQL - een krachtige relationele database. Voor webapplicaties gebruik je vaak dezelfde database, maar voor development, testing en kleine applicaties is **SQLite** een handige en lichtgewicht alternatief.

## Waarom SQLite?

SQLite verschilt op belangrijke punten van PostgreSQL:

| Aspect | PostgreSQL | SQLite |
|--------|-----------|--------|
| **Server** | Aparte database server | Geen server - gewoon een bestand |
| **Setup** | Installatie + configuratie | Built-in met Python |
| **Gebruik** | Productie webapplicaties | Development, testing, kleine apps |
| **Concurrency** | Veel gelijktijdige gebruikers | Beperkt (file locking) |
| **SQL dialect** | PostgreSQL SQL | SQLite SQL (kleine verschillen) |

!!! note "SQLite vs PostgreSQL SQL"
    De SQL syntax is grotendeels hetzelfde. Kleine verschillen:

    - SQLite heeft minder datatypes (TEXT, INTEGER, REAL, BLOB)
    - Geen `ALTER TABLE` voor het wijzigen van kolommen
    - Type validatie is minder strikt

## SQLite CLI (kort)

Je kunt SQLite via de command-line gebruiken (vergelijkbaar met `psql` voor PostgreSQL):

```console
$ sqlite3 test.db
SQLite version 3.39.5
Enter ".help" for usage hints.
sqlite> .tables
sqlite> .quit
```

Handige punt-commando's (vergelijkbaar met `\d` commando's in psql):

| Commando | Betekenis |
|----------|-----------|
| `.tables` | Toon alle tabellen |
| `.schema` | Toon tabelstructuur |
| `.quit` | Afsluiten |

!!! tip "Visueel werken met DB Browser for SQLite"
    Als je liever visueel werkt (vergelijkbaar met pgAdmin voor PostgreSQL), gebruik dan [DB Browser for SQLite](https://sqlitebrowser.org/).

    **Voordelen:**
    - Tabellen visueel bekijken en bewerken
    - SQL queries runnen met syntax highlighting
    - Database structure inspecteren
    - Handig tijdens Flask development om snel data te checken

    **Download:** [sqlitebrowser.org](https://sqlitebrowser.org/)

## SQLite in Python

Python heeft `sqlite3` built-in. In het volgende deel leer je hoe je SQLite gebruikt vanuit Python met moderne patterns zoals:

- Type annotations
- Context managers (`with` statements)
- Proper error handling

**Volgende stap:** In [Deel 2](sql-deel2.md) ga je direct aan de slag met SQLite in Python.
