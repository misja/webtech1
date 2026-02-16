# SQLite in Python: JOINs en Queries

In het vorige deel heb je gewerkt met een eenvoudige contacts database. Nu gaan we werken met een realistische database met meerdere tabellen en **JOIN** queries. Je kent JOINs al van het vak Databases - hier leer je hoe je ze gebruikt vanuit Python.

## De music database

Download de [`music.sqlite`](bestanden/music.sqlite) database. Deze bevat drie tabellen die je ook bij OOP hebt gezien, maar nu met veel meer data:

- `artists` - Artiesten (201 records)
- `albums` - Albums (439 records)
- `songs` - Songs (5350 records)

### Database structuur inspecteren

Laten we eerst de database verkennen vanuit Python:

```python
import sqlite3
from sqlite3 import Row

def inspect_database(db_path: str = "music.sqlite") -> None:
    """Toon database structuur en basisstatistieken."""
    with sqlite3.connect(db_path) as conn:
        conn.row_factory = Row

        # Haal schema informatie op
        cursor = conn.execute("""
            SELECT name, sql
            FROM sqlite_master
            WHERE type='table'
        """)

        print("Database tabellen:\n")
        for table in cursor.fetchall():
            print(f"Tabel: {table['name']}")

            # Tel records per tabel
            count_cursor = conn.execute(f"SELECT COUNT(*) as count FROM {table['name']}")
            count = count_cursor.fetchone()['count']
            print(f"Aantal records: {count}\n")

# Gebruik
inspect_database()
```

Output:
```
Database tabellen:

Tabel: artists
Aantal records: 201

Tabel: albums
Aantal records: 439

Tabel: songs
Aantal records: 5350
```

!!! info "PRIMARY KEY AUTOINCREMENT"
    SQLite vult automatisch de primary key kolom `_id` in wanneer je een nieuwe record toevoegt:

    ```python
    cursor = conn.execute("INSERT INTO artists (name) VALUES (?)", ("Travis",))
    new_id = cursor.lastrowid  # 202
    ```

    Dit werkt hetzelfde als PostgreSQL's `SERIAL` type.

## Eenvoudige queries

Laten we beginnen met een paar eenvoudige queries om weer in te komen:

```python
def get_album_by_id(album_id: int, db_path: str = "music.sqlite") -> Row | None:
    """Haal één album op op basis van ID."""
    with sqlite3.connect(db_path) as conn:
        conn.row_factory = Row
        cursor = conn.execute(
            "SELECT * FROM albums WHERE _id = ?",
            (album_id,)
        )
        return cursor.fetchone()

# Gebruik
album = get_album_by_id(167)
if album:
    print(f"Album {album['_id']}: {album['name']}")
```

Output:
```
Album 167: Blurring The Edges
```

### Sorteren met ORDER BY

Je kunt resultaten sorteren met `ORDER BY`:

```python
def get_artists_sorted(db_path: str = "music.sqlite", desc: bool = False) -> list[Row]:
    """Haal alle artiesten op, gesorteerd op naam."""
    with sqlite3.connect(db_path) as conn:
        conn.row_factory = Row

        order = "DESC" if desc else "ASC"
        cursor = conn.execute(f"SELECT * FROM artists ORDER BY name {order}")

        return cursor.fetchall()

# Gebruik
artists = get_artists_sorted(desc=True)
for artist in artists[:5]:  # Toon eerste 5
    print(f"{artist['_id']}: {artist['name']}")
```

Output:
```
23: ZZ Top
179: Yngwie Malmsteen
148: Yardbirds
97: Yes
14: Who
```

!!! warning "SQL injection bij ORDER BY"
    In het voorbeeld hierboven gebruiken we f-string voor `order` (`ASC`/`DESC`). Dit is veilig omdat we de waarde zelf controleren (boolean → "ASC" of "DESC").

    Doe dit NOOIT met user input:
    ```python
    # GEVAARLIJK - SQL injection risico!
    order = input("ASC or DESC? ")
    cursor.execute(f"SELECT * FROM artists ORDER BY name {order}")
    ```

## JOINs: meerdere tabellen combineren

Tot nu toe hebben we met één tabel gewerkt. Maar de echte kracht van SQL komt pas bij JOINs. Je kent dit al van PostgreSQL - in Python werkt het precies hetzelfde.

### Simpele JOIN: Songs met Albums

Laten we songs combineren met albums om te zien op welk album elke song staat:

```python
def get_songs_with_albums(db_path: str = "music.sqlite") -> list[Row]:
    """Haal alle songs op met hun album naam."""
    with sqlite3.connect(db_path) as conn:
        conn.row_factory = Row

        cursor = conn.execute("""
            SELECT s.track, s.title, a.name AS album_name
            FROM songs s
            JOIN albums a ON s.album = a._id
            ORDER BY s.title
        """)

        return cursor.fetchall()

# Gebruik
songs = get_songs_with_albums()
for song in songs[:5]:  # Toon eerste 5
    print(f"Track {song['track']}: {song['title']} (op {song['album_name']})")
```

Output:
```
Track 4: #1 Zero (op The Colour And The Shape)
Track 1: 'Desolation Row' (op Desire)
Track 1: '74-'75 (op Sheer Heart Attack)
Track 6: (I Can't Get No) Satisfaction (op The Big Come Up)
Track 2: (I Can't Get No) Satisfaction (op Singles Collection: The London Years)
```

!!! info "JOIN syntax"
    De JOIN syntax is identiek aan PostgreSQL:

    ```sql
    SELECT kolommen
    FROM tabel1 alias1
    JOIN tabel2 alias2 ON alias1.foreign_key = alias2.primary_key
    ```

    - `s` en `a` zijn **aliases** (afkortingen)
    - `ON` specificeert de relatie tussen tabellen
    - `a.name AS album_name` geeft de kolom een duidelijke naam

### JOIN met WHERE: Artiesten met Albums

Nu gaan we artiesten ophalen met hun albums, alfabetisch gerangschikt:

```python
def get_artists_with_albums(db_path: str = "music.sqlite") -> list[Row]:
    """Haal alle artiesten op met hun albums."""
    with sqlite3.connect(db_path) as conn:
        conn.row_factory = Row

        cursor = conn.execute("""
            SELECT ar.name AS artist, al.name AS album
            FROM artists ar
            JOIN albums al ON ar._id = al.artist
            ORDER BY ar.name, al.name
        """)

        return cursor.fetchall()

# Gebruik
artists_albums = get_artists_with_albums()
for item in artists_albums[:10]:  # Toon eerste 10
    print(f"{item['artist']}: {item['album']}")
```

Output:
```
1000 Maniacs: Our Time in Eden
10cc: The Best Of The Early Years
AC DC: For Those About To Rock (We Salute You)
AC DC: If You Want Blood You've Got It
Aerosmith: Night In The Ruts
Aerosmith: Rocks
Alice Cooper: Beast Of Alice Cooper
...
```

### Dubbele JOIN: Artiesten, Albums, Songs

Nu wordt het interessanter: we combineren alle drie de tabellen. Hiervoor hebben we **twee JOINs** nodig:

```python
def get_complete_music_catalog(db_path: str = "music.sqlite") -> list[Row]:
    """Haal alle songs op met artiest en album informatie."""
    with sqlite3.connect(db_path) as conn:
        conn.row_factory = Row

        cursor = conn.execute("""
            SELECT
                ar.name AS artist,
                al.name AS album,
                s.track,
                s.title
            FROM songs s
            JOIN albums al ON s.album = al._id
            JOIN artists ar ON al.artist = ar._id
            ORDER BY ar.name, al.name, s.track
        """)

        return cursor.fetchall()

# Gebruik
catalog = get_complete_music_catalog()
for item in catalog[:10]:
    print(f"{item['artist']} - {item['album']} - Track {item['track']}: {item['title']}")
```

Output:
```
1000 Maniacs - Our Time in Eden - Track 1: These Are Days
1000 Maniacs - Our Time in Eden - Track 2: Eat For Two
1000 Maniacs - Our Time in Eden - Track 3: Candy Everybody Wants
1000 Maniacs - Our Time in Eden - Track 4: Tolerance
...
```

!!! tip "Meerdere JOINs"
    Bij meerdere JOINs werk je **van binnen naar buiten**:

    1. `songs` JOIN `albums` (via `s.album = al._id`)
    2. `albums` JOIN `artists` (via `al.artist = ar._id`)

    Dit is hetzelfde als bij PostgreSQL. De volgorde maakt uit!

### JOIN met WHERE: Zoeken in resultaten

We kunnen ook filteren op JOIN resultaten met een `WHERE` clausule. Bijvoorbeeld: zoek alle songs met "doctor" in de titel:

```python
def search_songs_by_title(
    search_term: str,
    db_path: str = "music.sqlite"
) -> list[Row]:
    """Zoek songs op basis van titel, inclusief artiest en album info."""
    with sqlite3.connect(db_path) as conn:
        conn.row_factory = Row

        cursor = conn.execute("""
            SELECT
                ar.name AS artist,
                al.name AS album,
                s.track,
                s.title
            FROM songs s
            JOIN albums al ON s.album = al._id
            JOIN artists ar ON al.artist = ar._id
            WHERE s.title LIKE ?
            ORDER BY ar.name, al.name, s.title
        """, (f"%{search_term}%",))

        return cursor.fetchall()

# Gebruik
doctor_songs = search_songs_by_title("doctor")
print(f"Gevonden {len(doctor_songs)} songs met 'doctor' in de titel:\n")
for song in doctor_songs:
    print(f"{song['artist']}: {song['title']} (op {song['album']})")
```

Output:
```
Gevonden 13 songs met 'doctor' in de titel:

Black Sabbath: Rock 'N' Roll Doctor (op Technical Ecstasy)
Dr Feelgood: You Shouldn't Call The Doctor (If You Can't Afford The Bills) (op Malpractice)
Dr Feelgood: Down At The Doctors (op Private Practice)
Fleetwood Mac: Doctor Brown (op The Best of)
...
```

!!! info "LIKE operator en wildcard"
    - `LIKE '%doctor%'` zoekt overal in de string
    - `%` is een wildcard (= 0 of meer karakters)
    - We gebruiken `?` placeholder met `f"%{search_term}%"` voor veiligheid

    Dit is identiek aan PostgreSQL's `LIKE` operator.

## Views (optioneel)

Een **view** is een virtuele tabel - een opgeslagen query die je kunt gebruiken alsof het een echte tabel is. Views worden gebruikt voor:

- **Security**: Gevoelige kolommen verbergen (zoals salaris)
- **Simplificatie**: Complexe queries herbruikbaar maken
- **Abstraction layer**: Database structuur verbergen voor gebruikers

!!! note "Views in modern Python apps"
    In Python/Flask apps gebruik je views minder vaak. Met SQLAlchemy (Week 6) schrijf je queries direct in Python en gebruik je geen SQL views meer.

    Views zijn wel handig als je een database deelt met andere applicaties of rapportage tools.

### View maken en gebruiken in Python

Laten we een view maken voor de "doctor songs" query van eerder:

```python
def create_doctor_songs_view(db_path: str = "music.sqlite") -> None:
    """Maak een view voor songs met 'doctor' in de titel."""
    with sqlite3.connect(db_path) as conn:
        # Verwijder view als deze al bestaat
        conn.execute("DROP VIEW IF EXISTS vDoctorSongs")

        # Maak nieuwe view
        conn.execute("""
            CREATE VIEW vDoctorSongs AS
            SELECT
                ar.name AS artist,
                al.name AS album,
                s.track,
                s.title
            FROM songs s
            JOIN albums al ON s.album = al._id
            JOIN artists ar ON al.artist = ar._id
            WHERE s.title LIKE '%doctor%'
            ORDER BY ar.name, al.name, s.title
        """)

        conn.commit()
        print("View 'vDoctorSongs' aangemaakt")

def query_view(view_name: str, db_path: str = "music.sqlite") -> list[Row]:
    """Haal data op uit een view."""
    with sqlite3.connect(db_path) as conn:
        conn.row_factory = Row
        cursor = conn.execute(f"SELECT * FROM {view_name}")
        return cursor.fetchall()

# Gebruik
create_doctor_songs_view()

# Query de view alsof het een tabel is
doctor_songs = query_view("vDoctorSongs")
for song in doctor_songs:
    print(f"{song['artist']}: {song['title']}")
```

Output:
```
View 'vDoctorSongs' aangemaakt
Black Sabbath: Rock 'N' Roll Doctor
Dr Feelgood: You Shouldn't Call The Doctor (If You Can't Afford The Bills)
Dr Feelgood: Down At The Doctors
Fleetwood Mac: Doctor Brown
...
```

### View met filter

Je kunt de view ook filteren, net als een normale tabel:

```python
def search_in_view(
    view_name: str,
    artist_filter: str,
    db_path: str = "music.sqlite"
) -> list[Row]:
    """Zoek in een view met extra filtering."""
    with sqlite3.connect(db_path) as conn:
        conn.row_factory = Row
        cursor = conn.execute(
            f"SELECT * FROM {view_name} WHERE artist LIKE ?",
            (f"%{artist_filter}%",)
        )
        return cursor.fetchall()

# Gebruik
feelgood_songs = search_in_view("vDoctorSongs", "feelgood")
for song in feelgood_songs:
    print(f"{song['artist']}: {song['title']} (op {song['album']})")
```

Output:
```
Dr Feelgood: You Shouldn't Call The Doctor (If You Can't Afford The Bills) (op Malpractice)
Dr Feelgood: Down At The Doctors (op Private Practice)
```

!!! tip "Views bekijken"
    Je kunt alle views in de database opvragen:

    ```python
    cursor = conn.execute("""
        SELECT name, sql
        FROM sqlite_master
        WHERE type='view'
    """)
    ```

## Voorbereiding op SQLAlchemy

De patterns die je hier leert, komen terug bij SQLAlchemy (Week 6):

| sqlite3 pattern | SQLAlchemy equivalent |
|----------------|----------------------|
| **JOIN queries** | Relationships tussen models |
| **Placeholders (`?`)** | Automatisch escaped parameters |
| **row_factory = Row** | SQLAlchemy Row objects (standaard) |
| **Context managers** | Session management |
| **Views** | Queries in Python (niet SQL views) |

**Waarom dit leren?** Begrijpen hoe JOINs werken helpt je begrijpen wat SQLAlchemy doet. Bijvoorbeeld:

```python
# Wat je nu schrijft (sqlite3):
cursor.execute("""
    SELECT ar.name, al.name
    FROM artists ar
    JOIN albums al ON ar._id = al.artist
""")

# Wordt later (SQLAlchemy):
for artist in session.query(Artist):
    for album in artist.albums:  # Automatische JOIN!
        print(f"{artist.name}: {album.name}")
```

SQLAlchemy abstraheert de SQL weg, maar onder de motorkap gebruikt het precies dezelfde JOINs.

## Samenvatting

Je hebt geleerd:

- Database structuur inspecteren met `sqlite_master`
- **JOINs** gebruiken om meerdere tabellen te combineren
- Simpele JOIN (2 tabellen), dubbele JOIN (3 tabellen)
- **WHERE** clausules combineren met JOINs
- **LIKE** operator voor tekst zoeken met wildcards
- **Views** maken en gebruiken (optioneel)
- Placeholders gebruiken voor SQL injection preventie
- Link tussen sqlite3 patterns en SQLAlchemy

**Volgende stap:** In [Deel 4](sql-deel4.md) leer je werken met een complete MusicDatabase class die alle functionaliteit combineert.

**Oefening:** Maak nu [oefening 1](oefeningen/sql-oefening1.md).
