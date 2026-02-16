# Complete Database Class: MusicDatabase

In de vorige delen heb je afzonderlijke functies gezien voor database operaties. Nu gaan we alles combineren in een **database class** - een moderne, herbruikbare oplossing voor het werken met de music database.

## Waarom een database class?

Een database class biedt verschillende voordelen:

- **Encapsulation**: Alle database logica op één plek
- **Herbruikbaarheid**: Makkelijk te gebruiken in verschillende scripts
- **Consistency**: Altijd dezelfde patterns (context managers, placeholders, etc.)
- **Onderhoudbaarheid**: Aanpassingen hoef je maar op één plek te maken

## De complete MusicDatabase class

Hier is een complete implementatie met alle patterns die je tot nu toe hebt geleerd:

```python
import sqlite3
from sqlite3 import Row
from typing import Optional


class MusicDatabase:
    """Database manager voor de music.sqlite database.

    Deze class biedt methoden voor het ophalen van artiesten, albums en songs
    uit de music database, inclusief JOIN queries.

    Attributes:
        db_path (str): Pad naar de SQLite database file.
    """

    def __init__(self, db_path: str = "music.sqlite"):
        """Initialiseer de database manager.

        Args:
            db_path: Pad naar de database file (default: "music.sqlite")
        """
        self.db_path = db_path

    def _get_connection(self) -> sqlite3.Connection:
        """Maak database connectie met row_factory ingesteld.

        Returns:
            sqlite3.Connection: Database connectie object
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = Row
        return conn

    # ==================== ARTISTS ====================

    def get_all_artists(self, order_by: str = "name") -> list[Row]:
        """Haal alle artiesten op, gesorteerd.

        Args:
            order_by: Kolom om op te sorteren (default: "name")

        Returns:
            Lijst met alle artiesten
        """
        with self._get_connection() as conn:
            cursor = conn.execute(f"SELECT * FROM artists ORDER BY {order_by}")
            return cursor.fetchall()

    def get_artist_by_id(self, artist_id: int) -> Optional[Row]:
        """Haal één artiest op op basis van ID.

        Args:
            artist_id: ID van de artiest

        Returns:
            Artiest record of None als niet gevonden
        """
        with self._get_connection() as conn:
            cursor = conn.execute(
                "SELECT * FROM artists WHERE _id = ?",
                (artist_id,)
            )
            return cursor.fetchone()

    def search_artists(self, search_term: str) -> list[Row]:
        """Zoek artiesten op basis van naam.

        Args:
            search_term: Zoekterm voor artiest naam

        Returns:
            Lijst met matchende artiesten
        """
        with self._get_connection() as conn:
            cursor = conn.execute(
                "SELECT * FROM artists WHERE name LIKE ? ORDER BY name",
                (f"%{search_term}%",)
            )
            return cursor.fetchall()

    # ==================== ALBUMS ====================

    def get_all_albums(self) -> list[Row]:
        """Haal alle albums op met artiest informatie."""
        with self._get_connection() as conn:
            cursor = conn.execute("""
                SELECT
                    al._id,
                    al.name AS album,
                    ar.name AS artist
                FROM albums al
                JOIN artists ar ON al.artist = ar._id
                ORDER BY ar.name, al.name
            """)
            return cursor.fetchall()

    def get_albums_by_artist(self, artist_id: int) -> list[Row]:
        """Haal alle albums op van een specifieke artiest.

        Args:
            artist_id: ID van de artiest

        Returns:
            Lijst met albums van deze artiest
        """
        with self._get_connection() as conn:
            cursor = conn.execute(
                "SELECT * FROM albums WHERE artist = ? ORDER BY name",
                (artist_id,)
            )
            return cursor.fetchall()

    # ==================== SONGS ====================

    def get_songs_by_album(self, album_id: int) -> list[Row]:
        """Haal alle songs op van een specifiek album.

        Args:
            album_id: ID van het album

        Returns:
            Lijst met songs van dit album, gesorteerd op track nummer
        """
        with self._get_connection() as conn:
            cursor = conn.execute(
                "SELECT * FROM songs WHERE album = ? ORDER BY track",
                (album_id,)
            )
            return cursor.fetchall()

    def search_songs(self, search_term: str) -> list[Row]:
        """Zoek songs inclusief artiest en album informatie.

        Args:
            search_term: Zoekterm voor song titel

        Returns:
            Lijst met matchende songs met volledige informatie
        """
        with self._get_connection() as conn:
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
                ORDER BY ar.name, al.name, s.track
            """, (f"%{search_term}%",))
            return cursor.fetchall()

    # ==================== CATALOG ====================

    def get_artist_catalog(self, artist_id: int) -> dict:
        """Haal complete catalogus op voor een artiest.

        Args:
            artist_id: ID van de artiest

        Returns:
            Dictionary met artiest info, albums en songs
        """
        artist = self.get_artist_by_id(artist_id)
        if not artist:
            return {}

        albums = self.get_albums_by_artist(artist_id)

        # Haal songs op per album
        catalog = {
            "artist": artist["name"],
            "artist_id": artist_id,
            "albums": []
        }

        for album in albums:
            songs = self.get_songs_by_album(album["_id"])
            catalog["albums"].append({
                "album_name": album["name"],
                "album_id": album["_id"],
                "songs": [
                    {"track": song["track"], "title": song["title"]}
                    for song in songs
                ]
            })

        return catalog

    # ==================== STATISTICS ====================

    def get_statistics(self) -> dict:
        """Haal database statistieken op.

        Returns:
            Dictionary met statistieken
        """
        with self._get_connection() as conn:
            stats = {}

            # Tel artiesten
            cursor = conn.execute("SELECT COUNT(*) as count FROM artists")
            stats["total_artists"] = cursor.fetchone()["count"]

            # Tel albums
            cursor = conn.execute("SELECT COUNT(*) as count FROM albums")
            stats["total_albums"] = cursor.fetchone()["count"]

            # Tel songs
            cursor = conn.execute("SELECT COUNT(*) as count FROM songs")
            stats["total_songs"] = cursor.fetchone()["count"]

            return stats


# ==================== GEBRUIK ====================

if __name__ == "__main__":
    db = MusicDatabase()

    # Toon statistieken
    stats = db.get_statistics()
    print("=== Music Database Statistics ===")
    print(f"Artiesten: {stats['total_artists']}")
    print(f"Albums: {stats['total_albums']}")
    print(f"Songs: {stats['total_songs']}\n")

    # Zoek artiesten
    print("=== Artiesten met 'black' in de naam ===")
    artists = db.search_artists("black")
    for artist in artists:
        print(f"- {artist['name']}")

    print()

    # Haal complete catalogus op
    print("=== Catalogus van AC/DC (artist_id=3) ===")
    catalog = db.get_artist_catalog(3)
    if catalog:
        print(f"Artiest: {catalog['artist']}\n")
        for album in catalog["albums"]:
            print(f"Album: {album['album_name']}")
            for song in album["songs"]:
                print(f"  {song['track']:2d}. {song['title']}")
            print()

    # Zoek songs
    print("=== Songs met 'love' in de titel ===")
    songs = db.search_songs("love")
    for song in songs[:5]:  # Toon eerste 5
        print(f"{song['artist']}: {song['title']} (op {song['album']})")
```

## Gebruik van de class

### Basis gebruik

```python
# Maak een database instance
db = MusicDatabase()

# Haal alle artiesten op
artists = db.get_all_artists()
for artist in artists:
    print(f"{artist['_id']}: {artist['name']}")

# Zoek specifiek
beatles_songs = db.search_songs("revolution")
for song in beatles_songs:
    print(f"{song['title']} door {song['artist']}")
```

### Catalogus ophalen

```python
# Haal alle albums en songs op voor een artiest
catalog = db.get_artist_catalog(artist_id=42)

print(f"Artiest: {catalog['artist']}")
for album in catalog['albums']:
    print(f"\nAlbum: {album['album_name']}")
    for song in album['songs']:
        print(f"  Track {song['track']}: {song['title']}")
```

### Eigen database pad

```python
# Gebruik een andere database file
db = MusicDatabase("path/to/other/music.sqlite")
```

## Design patterns in de class

Deze class demonstreert verschillende belangrijke patterns:

### 1. Private helper method

```python
def _get_connection(self) -> sqlite3.Connection:
    """Helper method die niet bedoeld is voor extern gebruik."""
    # ...
```

De underscore `_` geeft aan dat dit een interne method is.

### 2. Type hints overal

```python
def get_artist_by_id(self, artist_id: int) -> Optional[Row]:
    #                           ↑ input type    ↑ return type
```

### 3. Docstrings met Args en Returns

```python
def search_artists(self, search_term: str) -> list[Row]:
    """Zoek artiesten op basis van naam.

    Args:
        search_term: Zoekterm voor artiest naam

    Returns:
        Lijst met matchende artiesten
    """
```

### 4. Context managers

```python
with self._get_connection() as conn:
    # Gebruik connection
    # Automatische cleanup
```

### 5. Placeholders tegen SQL injection

```python
cursor.execute(
    "SELECT * FROM artists WHERE name LIKE ?",
    (f"%{search_term}%",)  # Veilig!
)
```

## Uitbreidingen (optioneel)

Je kunt de class uitbreiden met extra functionaliteit:

### Data toevoegen

```python
def add_artist(self, name: str) -> int:
    """Voeg een nieuwe artiest toe."""
    with self._get_connection() as conn:
        cursor = conn.execute(
            "INSERT INTO artists (name) VALUES (?)",
            (name,)
        )
        conn.commit()
        return cursor.lastrowid
```

### Data wijzigen

```python
def update_song_title(self, song_id: int, new_title: str) -> bool:
    """Update de titel van een song."""
    with self._get_connection() as conn:
        cursor = conn.execute(
            "UPDATE songs SET title = ? WHERE _id = ?",
            (new_title, song_id)
        )
        conn.commit()
        return cursor.rowcount > 0
```

### Error handling

```python
def get_artist_by_id(self, artist_id: int) -> Optional[Row]:
    """Haal artiest op met error handling."""
    try:
        with self._get_connection() as conn:
            cursor = conn.execute(
                "SELECT * FROM artists WHERE _id = ?",
                (artist_id,)
            )
            return cursor.fetchone()
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return None
```

## Samenvatting

Je hebt geleerd:

- Een complete database class bouwen
- Methods organiseren per entiteit (artists, albums, songs)
- Private helper methods gebruiken (`_get_connection`)
- Complexe data structuren returnen (catalogus dictionary)
- Type hints en docstrings consequent toepassen
- Alle patterns combineren (context managers, placeholders, row_factory)

**Volgende stap:** [Deel 5](sql-deel5.md) - SQL injection preventie.

**Tip:** Gebruik deze MusicDatabase class als template voor je eigen database classes in Flask applicaties!
