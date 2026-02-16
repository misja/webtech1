# OOP Python – Objecten & Relaties

**Leestijd: ~20 minuten**

In dit deel leer je hoe objecten andere objecten kunnen bevatten (**compositie**). Dit is essentieel voor het werken met databases, waar tabellen aan elkaar gereleerd zijn via foreign keys.

## Wat is compositie?

Compositie betekent dat een object andere objecten bevat. Dit is een **"heeft een"** relatie:

```python
from dataclasses import dataclass

@dataclass
class Klant:
    naam: str
    email: str

@dataclass
class Product:
    naam: str
    prijs: float

@dataclass
class Bestelling:
    klant: Klant  # Bestelling HEEFT EEN klant
    product: Product  # Bestelling HEEFT EEN product

# Gebruik
jan = Klant("Jan Jansen", "jan@email.nl")
laptop = Product("Laptop", 799.99)
bestelling = Bestelling(jan, laptop)

print(f"{bestelling.klant.naam} bestelde {bestelling.product.naam}")
# Jan Jansen bestelde Laptop
```

!!! note "Compositie vs Inheritance"
    **Inheritance (is-een):** Een laptop **is een** product

    **Compositie (heeft-een):** Een bestelling **heeft een** klant

    In databases: compositie = foreign keys!

## Waarom compositie?

In webapplicaties heb je vaak objecten die aan elkaar gerelateerd zijn:

- Een **bestelling** heeft een **klant**
- Een **bestelling** heeft **producten**
- Een **blogpost** heeft een **auteur**
- Een **comment** heeft een **user** en een **post**

Dit modelleer je met compositie in je code, en met foreign keys in je database.

## Objects in lists

Een object kan een lijst met andere objecten bevatten:

```python
from dataclasses import dataclass, field

@dataclass
class Product:
    naam: str
    prijs: float

@dataclass
class Winkelwagen:
    klant_naam: str
    items: list[Product] = field(default_factory=list)

    def voeg_toe(self, product: Product) -> None:
        """Voeg product toe aan winkelwagen."""
        self.items.append(product)

    def bereken_totaal(self) -> float:
        """Bereken totaalprijs van alle producten."""
        return sum(product.prijs for product in self.items)

# Gebruik
wagen = Winkelwagen("Jan Jansen")
wagen.voeg_toe(Product("Laptop", 799.99))
wagen.voeg_toe(Product("Muis", 25.50))

print(f"Totaal: €{wagen.bereken_totaal():.2f}")
# Totaal: €825.49
```

!!! warning "field(default_factory=list)"
    Voor een lijst als attribuut moet je altijd `field(default_factory=list)` gebruiken, anders delen alle instanties dezelfde lijst!

## Return dicts voor gestructureerde data

In webapplicaties wil je vaak gestructureerde data teruggeven (voor JSON responses):

```python
from dataclasses import dataclass
from typing import Optional

@dataclass
class Klant:
    naam: str
    email: str
    korting_percentage: float = 0.0

    def bereken_korting(self, bedrag: float) -> float:
        """Bereken kortingsbedrag."""
        return bedrag * (self.korting_percentage / 100)

@dataclass
class Bestelling:
    klant: Klant
    subtotaal: float
    verzendkosten: float = 5.95

    def bereken_totaal(self) -> dict:
        """
        Bereken totaal en geef gestructureerde data terug.

        Returns:
            dict met keys: subtotaal, korting, verzendkosten, totaal
        """
        korting = self.klant.bereken_korting(self.subtotaal)

        # Gratis verzending boven €50 (na korting)
        verzendkosten = self.verzendkosten
        if (self.subtotaal - korting) >= 50:
            verzendkosten = 0.0

        totaal = self.subtotaal - korting + verzendkosten

        return {
            "subtotaal": self.subtotaal,
            "korting": korting,
            "verzendkosten": verzendkosten,
            "totaal": totaal
        }

# Gebruik
jan = Klant("Jan Jansen", "jan@email.nl", korting_percentage=10.0)
bestelling = Bestelling(jan, subtotaal=125.50)

totaal_info = bestelling.bereken_totaal()
print(f"Subtotaal: €{totaal_info['subtotaal']:.2f}")
print(f"Korting: -€{totaal_info['korting']:.2f}")
print(f"Verzendkosten: €{totaal_info['verzendkosten']:.2f}")
print(f"Totaal: €{totaal_info['totaal']:.2f}")
```

!!! info "Waarom dicts teruggeven?"
    Dicts zijn **JSON-ready**. In Flask kun je ze direct teruggeven:

    ```python
    @app.route('/api/bestelling/<int:id>')
    def get_bestelling(id):
        bestelling = Bestelling.query.get(id)
        return jsonify(bestelling.bereken_totaal())
    ```

## Complexe compositie: Complete bestelling

Hier een realistisch voorbeeld met meerdere gecomponeerde objecten:

```python
from dataclasses import dataclass, field
from typing import Optional

@dataclass
class Klant:
    naam: str
    email: str
    korting_percentage: float = 0.0

    def bereken_korting(self, bedrag: float) -> float:
        return bedrag * (self.korting_percentage / 100)

@dataclass
class Product:
    naam: str
    prijs: float
    voorraad: int = 0

@dataclass
class Betaalmethode:
    type: str  # "iDEAL", "Creditcard", "PayPal"
    transactiekosten: float = 0.0

    def bereken_totaal_met_kosten(self, bedrag: float) -> float:
        return bedrag + self.transactiekosten

@dataclass
class Verzendmethode:
    type: str  # "Standaard", "Express", "Afhalen"
    kosten: float
    levertijd: str

@dataclass
class Kortingscode:
    code: str
    percentage: float

    def bereken_korting(self, bedrag: float) -> float:
        return bedrag * (self.percentage / 100)

@dataclass
class Bestelling:
    """Complete bestelling met alle relaties."""
    klant: Klant
    producten: list[Product] = field(default_factory=list)
    betaalmethode: Optional[Betaalmethode] = None
    verzendmethode: Optional[Verzendmethode] = None
    kortingscode: Optional[Kortingscode] = None

    def bereken_subtotaal(self) -> float:
        """Som van alle productprijzen."""
        return sum(p.prijs for p in self.producten)

    def bereken_totaal(self) -> dict:
        """
        Bereken complete totaal met alle kortingen en kosten.

        Returns:
            dict met alle bedragen (JSON-ready)
        """
        subtotaal = self.bereken_subtotaal()

        # Kortingscode
        korting = 0.0
        if self.kortingscode:
            korting = self.kortingscode.bereken_korting(subtotaal)

        # Verzendkosten (gratis boven €50 na korting)
        verzendkosten = 0.0
        if self.verzendmethode:
            verzendkosten = self.verzendmethode.kosten
            if (subtotaal - korting) >= 50:
                verzendkosten = 0.0

        # Transactiekosten
        tussentotaal = subtotaal - korting + verzendkosten
        transactiekosten = 0.0
        if self.betaalmethode:
            transactiekosten = self.betaalmethode.transactiekosten

        totaal = tussentotaal + transactiekosten

        return {
            "subtotaal": subtotaal,
            "korting": korting,
            "verzendkosten": verzendkosten,
            "transactiekosten": transactiekosten,
            "totaal": totaal
        }

# Test complete systeem
laptop = Product("Gaming Laptop", 799.99, 5)
muis = Product("Gaming Muis", 89.99, 20)

jan = Klant("Jan Jansen", "jan@email.nl", korting_percentage=5.0)

bestelling = Bestelling(
    klant=jan,
    producten=[laptop, muis],
    betaalmethode=Betaalmethode("iDEAL", transactiekosten=0.0),
    verzendmethode=Verzendmethode("Standaard", 5.95, "2-3 werkdagen"),
    kortingscode=Kortingscode("WELKOM10", 10.0)
)

totaal_info = bestelling.bereken_totaal()

print(f"Klant: {bestelling.klant.naam}")
print(f"Producten: {len(bestelling.producten)}x")
print(f"\nSubtotaal: €{totaal_info['subtotaal']:.2f}")
print(f"Korting: -€{totaal_info['korting']:.2f}")
print(f"Verzendkosten: €{totaal_info['verzendkosten']:.2f}")
print(f"Transactiekosten: €{totaal_info['transactiekosten']:.2f}")
print(f"TOTAAL: €{totaal_info['totaal']:.2f}")
```

## Preview: Database relaties (Foreign Keys)

Dit is waarom je compositie leert - in databases werk je zo met gerelateerde tabellen:

```python
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False)

class BlogPost(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)

    # Foreign key: elke post HEEFT EEN auteur
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # Relationship: geeft toegang tot het User object
    author = db.relationship('User', backref='posts')

# Gebruik (week 6!)
user = User.query.get(1)
post = BlogPost(title="Mijn blog", content="...", author=user)
db.session.add(post)
db.session.commit()

# Compositie in actie:
print(f"{post.title} door {post.author.username}")
```

!!! info "OOP → Database mapping"
    - **Compositie in Python** → **Foreign key in database**
    - `bestelling.klant` → `bestellingen.klant_id` (foreign key naar `klanten.id`)
    - Objecten bevatten objecten → Tabellen verwijzen naar tabellen

## JSON export voor API's

Voor webapplicaties wil je vaak je data als JSON exporteren:

```python
import json
from dataclasses import dataclass, asdict

@dataclass
class Klant:
    naam: str
    email: str

@dataclass
class Product:
    naam: str
    prijs: float

@dataclass
class Bestelling:
    klant: Klant
    producten: list[Product]

    def export_json(self) -> str:
        """Export als JSON string."""
        data = {
            "klant": {
                "naam": self.klant.naam,
                "email": self.klant.email
            },
            "producten": [
                {"naam": p.naam, "prijs": p.prijs}
                for p in self.producten
            ],
            "aantal_producten": len(self.producten)
        }
        return json.dumps(data, indent=2)

# Test
jan = Klant("Jan Jansen", "jan@email.nl")
bestelling = Bestelling(
    klant=jan,
    producten=[
        Product("Laptop", 799.99),
        Product("Muis", 25.50)
    ]
)

print(bestelling.export_json())
```

Output:
```json
{
  "klant": {
    "naam": "Jan Jansen",
    "email": "jan@email.nl"
  },
  "producten": [
    {"naam": "Laptop", "prijs": 799.99},
    {"naam": "Muis", "prijs": 25.5}
  ],
  "aantal_producten": 2
}
```

!!! tip "Dataclass → dict"
    Je kunt ook `asdict()` gebruiken om een dataclass automatisch naar een dict te converteren:

    ```python
    from dataclasses import asdict

    klant_dict = asdict(jan)
    # {'naam': 'Jan Jansen', 'email': 'jan@email.nl'}
    ```

## Praktijk: Flask API endpoint

Hier zie je hoe dit in een echte Flask applicatie werkt:

```python
from flask import Flask, jsonify
from dataclasses import dataclass

app = Flask(__name__)

@dataclass
class Product:
    id: int
    naam: str
    prijs: float

# In-memory "database" (week 6: echte database!)
producten = [
    Product(1, "Laptop", 799.99),
    Product(2, "Muis", 25.50),
    Product(3, "Toetsenbord", 89.99)
]

@app.route('/api/producten')
def get_producten():
    """Geef alle producten terug als JSON."""
    return jsonify([
        {"id": p.id, "naam": p.naam, "prijs": p.prijs}
        for p in producten
    ])

@app.route('/api/producten/<int:product_id>')
def get_product(product_id):
    """Geef één product terug."""
    product = next((p for p in producten if p.id == product_id), None)

    if product:
        return jsonify({
            "id": product.id,
            "naam": product.naam,
            "prijs": product.prijs
        })
    else:
        return jsonify({"error": "Product niet gevonden"}), 404
```

!!! note "Return values → JSON"
    Zie je waarom we altijd **return values** gebruiken en niet **print**? In een API moet je data teruggeven aan de client, niet naar de console printen.

## Separation of concerns

Goede code scheidt verantwoordelijkheden:

**Business logic (modellen):**
```python
@dataclass
class Bestelling:
    """Bevat business logic en data."""
    klant: Klant
    producten: list[Product]

    def bereken_totaal(self) -> dict:
        """Bereken totaal - RETURN data."""
        return {"totaal": sum(p.prijs for p in self.producten)}
```

**Presentation layer (routes):**
```python
@app.route('/bestelling/<int:id>')
def toon_bestelling(id):
    """Haalt data op en presenteert het."""
    bestelling = get_bestelling(id)  # Haal op
    totaal_info = bestelling.bereken_totaal()  # Bereken

    # Presenteer als HTML of JSON
    return render_template('bestelling.html',
                         bestelling=bestelling,
                         totaal=totaal_info['totaal'])
```

!!! info "Waarom scheiden?"
    - Business logic is herbruikbaar (API, CLI, tests)
    - Makkelijker te testen (geen Flask nodig voor tests)
    - Duidelijke verantwoordelijkheden

## Checklist

Controleer of je het volgende beheerst:

- [ ] Compositie: objecten die andere objecten bevatten
- [ ] `list[Object]` met `field(default_factory=list)`
- [ ] `Optional[]` voor attributen die None kunnen zijn
- [ ] Methoden die dicts teruggeven (JSON-ready)
- [ ] Begrijpen: compositie in code = foreign keys in database
- [ ] JSON export met `json.dumps()` of `jsonify()`
- [ ] Separation of concerns: business logic vs presentation

## Samenvatting

In dit deel heb je geleerd:

- **Compositie**: Objecten die andere objecten bevatten (heeft-een relatie)
- **Type hints**: `list[Product]`, `Optional[Klant]`
- **Return dicts**: Gestructureerde data voor JSON responses
- **JSON export**: Data klaarmaken voor API's
- **Database preview**: Compositie = foreign keys
- **Separation of concerns**: Business logic apart van presentation

**Je kunt nu:**

- Complexe datastructuren modelleren met objecten
- Web-ready code schrijven die JSON kan teruggeven
- Begrijpen hoe SQLAlchemy relaties werkt (foreign keys)
- Code schrijven die geschikt is voor Flask API's

**Volgende stap:** In week 6 ga je dit toepassen met SQLAlchemy. Je modellen krijgen foreign keys en relationships om tabellen aan elkaar te koppelen.

**Oefening:** Maak [Oefening 4](oefeningen/oop-oefening4.md) om compositie te oefenen met een compleet bestellingssysteem.
