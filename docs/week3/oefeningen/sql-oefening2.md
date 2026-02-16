# Oefening 2: JOINs met de Music Database

Deze oefening past bij [SQL Deel 3](../sql-deel3.md).

Download de [music.sqlite](../bestanden/music.sqlite) database en plaats deze in je project folder.

## Voorbereiding

Maak een Python bestand `music_queries.py` met een basis class:

```python
import sqlite3
from sqlite3 import Row

class MusicDatabase:
    """Database voor music queries."""

    def __init__(self, db_path: str = "music.sqlite"):
        self.db_path = db_path

    def _execute_query(self, query: str, params: tuple = ()) -> list[Row]:
        """Helper method om queries uit te voeren."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = Row
            cursor = conn.execute(query, params)
            return cursor.fetchall()
```

## Opgave 1: Songs van een Album

**Vraag:** Toon alle songs van het album 'Forbidden'.

Implementeer deze method:

```python
def get_songs_by_album(self, album_name: str) -> list[Row]:
    """Haal alle songs op van een specifiek album."""
    # TODO: Implementeer deze query
    # - JOIN songs met albums
    # - WHERE album.name = ?
    # - Gebruik _execute_query helper
    pass
```

Test:
```python
db = MusicDatabase()
songs = db.get_songs_by_album("Forbidden")
for song in songs:
    print(f"{song['title']}")
```

## Opgave 2: Songs Gesorteerd op Track

**Vraag:** Toon dezelfde songs, maar nu gesorteerd op tracknummer.

```python
def get_songs_by_album_sorted(self, album_name: str) -> list[Row]:
    """Haal songs op gesorteerd op track nummer."""
    # TODO: Voeg ORDER BY track toe
    pass
```

Test opnieuw en vergelijk de output.

## Opgave 3: Songs van een Artiest

**Vraag:** Toon alle songs van de band 'Deep Purple'.

**Hint:** Dit vereist een **dubbele JOIN** (songs → albums → artists)

```python
def get_songs_by_artist(self, artist_name: str) -> list[Row]:
    """Haal alle songs op van een specifieke artiest."""
    # TODO: Implementeer dubbele JOIN
    # FROM songs s
    # JOIN albums al ON s.album = al._id
    # JOIN artists ar ON al.artist = ar._id
    # WHERE ar.name = ?
    pass
```

## Opgave 4: Artiest Naam Wijzigen

**Vraag:** Wijzig de naam van de band 'Mehitabel' in 'One Kitten'.

```python
def update_artist_name(self, old_name: str, new_name: str) -> bool:
    """Update artiest naam."""
    # TODO: Implementeer UPDATE met WHERE
    # Return True als gelukt, False anders
    # Gebruik cursor.rowcount om te checken of er iets is gewijzigd
    pass
```

Test:
```python
if db.update_artist_name("Mehitabel", "One Kitten"):
    print("Artiest naam bijgewerkt")

# Verifieer
songs = db.get_songs_by_artist("One Kitten")
print(f"One Kitten heeft {len(songs)} songs")
```

## Opgave 5: Unieke Song Titels

**Vraag:** Toon alle unieke song titels van 'Aerosmith' in alfabetische volgorde.

**Hint:** Gebruik `SELECT DISTINCT`

```python
def get_unique_song_titles(self, artist_name: str) -> list[Row]:
    """Haal unieke song titels op van een artiest."""
    # TODO: Gebruik SELECT DISTINCT s.title
    # ORDER BY s.title
    pass
```

Test:
```python
titles = db.get_unique_song_titles("Aerosmith")
print(f"Unieke Aerosmith songs: {len(titles)}")
for song in titles:
    print(f"  - {song['title']}")
```

## Opgave 6: Aantal Unieke Songs

**Vraag:** Tel het aantal unieke songs van 'Aerosmith'.

**Hint:** Gebruik `SELECT COUNT(DISTINCT ...)`

```python
def count_unique_songs(self, artist_name: str) -> int:
    """Tel unieke songs van een artiest."""
    # TODO: Gebruik COUNT(DISTINCT s.title)
    # Return 0 als artiest niet bestaat
    pass
```

## Opgave 7: Aantal Albums

**Vraag:** Tel het aantal unieke albums van 'Aerosmith'.

```python
def count_albums(self, artist_name: str) -> int:
    """Tel aantal albums van een artiest."""
    # TODO: JOIN artists met albums
    # COUNT(DISTINCT al._id) of COUNT(al._id) als elke album_id uniek is
    pass
```

## Bonusopdracht 1: Top 5 Artiesten

Maak een method die de top 5 artiesten met de meeste songs laat zien:

```python
def get_top_artists(self, limit: int = 5) -> list[Row]:
    """Haal top artiesten op basis van aantal songs."""
    # TODO: GROUP BY artist
    # COUNT(*) as song_count
    # ORDER BY song_count DESC
    # LIMIT ?
    pass
```

Verwachte output format:
```
Top 5 artiesten:
1. Deep Purple (57 songs)
2. Iron Maiden (45 songs)
...
```

## Bonusopdracht 2: Langste Album

Vind het album met de meeste songs:

```python
def get_longest_album(self) -> Row | None:
    """Vind album met meeste songs."""
    # TODO: GROUP BY album
    # COUNT(*) as song_count
    # ORDER BY song_count DESC
    # LIMIT 1
    # Include artiest naam (JOIN met artists)
    pass
```

## Bonusopdracht 3: Complete Catalogus

Maak een method die een complete artiest catalogus laat zien (artiest → albums → songs):

```python
def get_artist_catalog(self, artist_name: str) -> dict:
    """Haal complete catalogus op van een artiest."""
    # Return format:
    # {
    #     'artist': 'Deep Purple',
    #     'albums': [
    #         {
    #             'name': 'Machine Head',
    #             'songs': [
    #                 {'track': 1, 'title': 'Highway Star'},
    #                 {'track': 2, 'title': 'Maybe I'm a Leo'},
    #                 ...
    #             ]
    #         },
    #         ...
    #     ]
    # }
    pass
```

## Main Functie

Schrijf een main functie die alle queries demonstreert:

```python
def main():
    db = MusicDatabase()

    print("=== Opgave 1: Songs van Forbidden ===")
    # ...

    print("\n=== Opgave 2: Gesorteerd op Track ===")
    # ...

    # etc.

if __name__ == "__main__":
    main()
```

## Verwachte Output Voorbeelden

```
=== Opgave 1: Songs van Forbidden ===
After Forever
The Illusion of Power
Get a Grip
Can't Get Close Enough
Shaking Off The Chains
I Witness
Cross of Thorns
Psychophobia
The Hand That Rocks The Cradle
Cardinal Sin
Forbidden
Rusty Angels

=== Opgave 5: Unieke Aerosmith Songs ===
Unieke Aerosmith songs: 79
  - Adam's Apple
  - Ain't Got You
  - Amazing
  ...

=== Opgave 7: Aantal Albums ===
Aerosmith heeft 15 albums
```

## Checklist

✅ Alle queries gebruiken placeholders (`?`)
✅ Context managers (`with`) gebruikt
✅ Type hints op alle methods
✅ row_factory = Row gebruikt
✅ JOIN queries correct (INNER JOIN standaard)
✅ DISTINCT voor unieke waarden
✅ COUNT voor aggregaties
✅ ORDER BY voor sortering
✅ Helper method `_execute_query` gebruikt
