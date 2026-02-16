# SQL Injection: Beveiliging

SQL injection is één van de meest voorkomende en gevaarlijkste beveiligingslekken in webapplicaties. In dit deel leer je wat SQL injection is, waarom het gevaarlijk is, en vooral: **hoe je het voorkomt** met de patterns die je al hebt geleerd.

!!! warning "OWASP Top 10"
    SQL injection staat al jaren in de [OWASP Top 10](https://owasp.org/www-project-top-ten/) van meest kritieke webapplicatie beveiligingsrisico's. Dit is essentiële kennis voor elke webdeveloper.

## Wat is SQL injection?

SQL injection is een aanval waarbij een kwaadwillende gebruiker SQL code injecteert via user input. Dit kan leiden tot:

- **Data diefstal**: Toegang tot alle data in de database
- **Data verlies**: Verwijderen van tabellen of records
- **Ongeautoriseerde toegang**: Inloggen als andere gebruikers
- **Complete compromise**: Overame van de database server

### Voorbeeld: onveilige code

Stel je hebt een login functie die user input direct in SQL zet:

```python
import sqlite3

def login_unsafe(username: str, password: str) -> bool:
    """GEVAARLIJK - gebruik dit NOOIT!"""
    conn = sqlite3.connect("users.db")

    # FOUT: f-string met user input in SQL!
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"

    cursor = conn.execute(query)
    user = cursor.fetchone()
    conn.close()

    return user is not None

# Normale login
result = login_unsafe("jan", "geheim123")  # Werkt normaal

# SQL injection attack!
result = login_unsafe("admin' --", "whatever")
# Query wordt: SELECT * FROM users WHERE username = 'admin' --' AND password = 'whatever'
# De -- maakt de rest commentaar, dus password check wordt overgeslagen!
```

De aanvaller kan nu inloggen als admin **zonder het wachtwoord te weten**!

### Andere aanvallen

SQL injection kan ook gebruikt worden voor:

**Data diefstal:**
```python
# User input: ' OR '1'='1
query = f"SELECT * FROM users WHERE username = '{user_input}'"
# Wordt: SELECT * FROM users WHERE username = '' OR '1'='1'
# Dit returnt ALLE gebruikers!
```

**Data vernietiging:**
```python
# User input: '; DROP TABLE users; --
query = f"DELETE FROM messages WHERE id = {message_id}"
# Zou kunnen worden: DELETE FROM messages WHERE id = 1; DROP TABLE users; --
# (Dit werkt gelukkig niet altijd, maar het risico bestaat)
```

## De oplossing: placeholders

Je hebt de oplossing al gezien in eerdere delen: **placeholders** (`?`). Dit is de **enige veilige manier** om user input in SQL te gebruiken.

### Veilige login functie

```python
import sqlite3
from sqlite3 import Row

def login_safe(username: str, password: str) -> bool:
    """Veilige login met placeholders."""
    with sqlite3.connect("users.db") as conn:
        conn.row_factory = Row

        # VEILIG: gebruik placeholders!
        cursor = conn.execute(
            "SELECT * FROM users WHERE username = ? AND password = ?",
            (username, password)
        )

        user = cursor.fetchone()
        return user is not None

# Normale login werkt
result = login_safe("jan", "geheim123")

# SQL injection attack wordt onschadelijk gemaakt
result = login_safe("admin' --", "whatever")
# De ' wordt geëscaped, wordt gezocht naar username "admin' --"
# Geen gevaar!
```

### Waarom placeholders veilig zijn

Placeholders zorgen voor **automatische escaping** van speciale karakters:

```python
def search_users_safe(search_term: str) -> list[Row]:
    """Zoek gebruikers veilig."""
    with sqlite3.connect("users.db") as conn:
        conn.row_factory = Row

        # Gevaarlijke input wordt automatisch geëscaped
        cursor = conn.execute(
            "SELECT * FROM users WHERE username LIKE ?",
            (f"%{search_term}%",)
        )

        return cursor.fetchall()

# SQL injection poging
users = search_users_safe("'; DROP TABLE users; --")
# Zoekt letterlijk naar de string "'; DROP TABLE users; --"
# Geen SQL code executie!
```

De database driver escapet automatisch:
- Enkele quotes (`'`) → `\'`
- Dubbele quotes (`"`) → `\"`
- Puntkomma's (`;`)
- Backslashes (`\`)

## Common mistakes (zelfs met placeholders!)

Er zijn een paar situaties waar placeholders **niet werken**. Pas hier extra op:

### 1. Table/column names

Placeholders werken NIET voor tabel- of kolomnamen:

```python
# FOUT - dit werkt niet!
table_name = "users"
cursor.execute("SELECT * FROM ?", (table_name,))  # ERROR

# Oplossing: whitelist validatie
ALLOWED_TABLES = ["users", "products", "orders"]

def get_all_from_table(table_name: str) -> list[Row]:
    """Haal data op met veilige tabel selectie."""
    if table_name not in ALLOWED_TABLES:
        raise ValueError(f"Invalid table: {table_name}")

    with sqlite3.connect("shop.db") as conn:
        conn.row_factory = Row
        # Nu is f-string veilig omdat we gevalideerd hebben
        cursor = conn.execute(f"SELECT * FROM {table_name}")
        return cursor.fetchall()
```

### 2. ORDER BY direction

```python
# FOUT - ORDER BY richting kan niet als placeholder
cursor.execute("SELECT * FROM users ORDER BY name ?", ("DESC",))  # ERROR

# Oplossing: valideer input
def get_users_sorted(desc: bool = False) -> list[Row]:
    """Haal gebruikers gesorteerd op."""
    # Controleer zelf welke waarde er komt
    order = "DESC" if desc else "ASC"

    with sqlite3.connect("users.db") as conn:
        conn.row_factory = Row
        # Nu is f-string veilig
        cursor = conn.execute(f"SELECT * FROM users ORDER BY name {order}")
        return cursor.fetchall()
```

### 3. LIMIT en OFFSET

Deze werken meestal WEL als placeholders, maar niet in alle SQL databases:

```python
# SQLite: dit werkt
def get_users_paginated(limit: int, offset: int) -> list[Row]:
    """Paginatie met placeholders (veilig in SQLite)."""
    with sqlite3.connect("users.db") as conn:
        conn.row_factory = Row
        cursor = conn.execute(
            "SELECT * FROM users LIMIT ? OFFSET ?",
            (limit, offset)
        )
        return cursor.fetchall()
```

## Volledige veilige database class

Hier is een complete voorbeeld met alle veilige patterns:

```python
import sqlite3
from sqlite3 import Row

class UserDatabase:
    """Veilige user database met SQL injection bescherming."""

    def __init__(self, db_path: str = "users.db"):
        self.db_path = db_path
        self._create_table()

    def _create_table(self) -> None:
        """Maak users tabel aan."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL UNIQUE,
                    email TEXT NOT NULL,
                    password TEXT NOT NULL
                )
            """)
            conn.commit()

    def add_user(self, username: str, email: str, password: str) -> int:
        """Voeg user toe (altijd veilig met placeholders)."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                "INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
                (username, email, password)
            )
            conn.commit()
            return cursor.lastrowid

    def login(self, username: str, password: str) -> Row | None:
        """Login user (veilig tegen SQL injection)."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = Row
            cursor = conn.execute(
                "SELECT * FROM users WHERE username = ? AND password = ?",
                (username, password)
            )
            return cursor.fetchone()

    def search_users(self, search_term: str) -> list[Row]:
        """Zoek users (veilig met placeholder in LIKE)."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = Row
            cursor = conn.execute(
                "SELECT id, username, email FROM users WHERE username LIKE ?",
                (f"%{search_term}%",)
            )
            return cursor.fetchall()

    def update_email(self, user_id: int, new_email: str) -> bool:
        """Update email (veilig met placeholders)."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                "UPDATE users SET email = ? WHERE id = ?",
                (new_email, user_id)
            )
            conn.commit()
            return cursor.rowcount > 0

    def delete_user(self, user_id: int) -> bool:
        """Verwijder user (veilig met placeholder)."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                "DELETE FROM users WHERE id = ?",
                (user_id,)
            )
            conn.commit()
            return cursor.rowcount > 0


# Gebruik (veilig tegen alle SQL injection pogingen)
db = UserDatabase()

# Normale gebruik
db.add_user("jan", "jan@email.nl", "geheim123")

# SQL injection pogingen worden onschadelijk gemaakt
db.add_user("'; DROP TABLE users; --", "evil@hacker.com", "whatever")
# Dit maakt gewoon een user met username "'; DROP TABLE users; --"
# Geen gevaar!

# Veilig inloggen
user = db.login("jan", "geheim123")
if user:
    print(f"Ingelogd als {user['username']}")

# Veilig zoeken
users = db.search_users("'; DELETE FROM users; --")
# Zoekt letterlijk naar die string, geen SQL executie
```

## Flask en SQL injection

In Flask applicaties is SQL injection een groot risico omdat je direct met user input werkt:

```python
from flask import Flask, request

app = Flask(__name__)

@app.route('/search')
def search():
    # User input komt uit URL parameters
    query = request.args.get('q', '')

    # GEVAARLIJK - NOOIT DOEN!
    # results = conn.execute(f"SELECT * FROM products WHERE name LIKE '%{query}%'")

    # VEILIG - altijd placeholders gebruiken
    with sqlite3.connect("shop.db") as conn:
        conn.row_factory = Row
        cursor = conn.execute(
            "SELECT * FROM products WHERE name LIKE ?",
            (f"%{query}%",)
        )
        results = cursor.fetchall()

    return render_template('search.html', results=results)
```

## Best practices samenvatting

✅ **DOE WEL:**
- Gebruik **altijd** placeholders (`?`) voor values
- Gebruik context managers (`with`)
- Valideer input bij table/column names (whitelist)
- Gebruik type hints
- Test met bekende SQL injection strings

❌ **DOE NIET:**
- F-strings of string concatenatie met user input in SQL
- User input direct in SQL queries
- `executescript()` met user input
- Vertrouwen op client-side validatie alleen

## Samenvatting

Je hebt geleerd:

- **Wat SQL injection is** en waarom het gevaarlijk is
- **Placeholders gebruiken** als enige veilige methode
- **Common mistakes** (table names, ORDER BY, etc.)
- **Veilige patterns** voor alle CRUD operaties
- **Flask specifieke risico's** en oplossingen
- **Best practices** voor veilige database code

**Volgende stap:** In [Deel 6](sql-deel6.md) leer je over exception handling bij database operaties.

**Oefening:** Maak nu [oefening 2](oefeningen/sql-oefening2.md) over SQL injection.

!!! tip "Test je beveiliging"
    Test je applicaties altijd met deze input strings:
    ```
    ' OR '1'='1
    ' OR '1'='1' --
    '; DROP TABLE users; --
    1' AND '1'='2
    ```
    Als deze niet gewoon als letterlijke strings behandeld worden, heb je een probleem!
