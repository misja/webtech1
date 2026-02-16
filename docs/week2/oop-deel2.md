# OOP Python – Dataclasses

In het vorige deel heb je gezien hoe je klassen maakt met `__init__`. Voor klassen die vooral data bevatten, heeft Python een modernere aanpak: **dataclasses**. Deze maken je code korter en leesbaarder.

## Het probleem met reguliere klassen

Kijk naar deze `Product` klasse:

```python
class Product:
    def __init__(self, naam: str, prijs: float, voorraad: int = 0):
        self.naam = naam
        self.prijs = prijs
        self.voorraad = voorraad
```

Dit werkt prima, maar er is veel **boilerplate**: je typt elke attribuutnaam drie keer. Voor klassen met veel attributen wordt dit vervelend.

## Dataclasses: minder code, zelfde resultaat

Python biedt een elegantere manier met de `@dataclass` decorator:

```python
from dataclasses import dataclass

@dataclass
class Product:
    naam: str
    prijs: float
    voorraad: int = 0
```

Dit genereert automatisch:
- Een `__init__` methode
- Een `__repr__` methode (voor debugging)
- Een `__eq__` methode (voor vergelijkingen)

Je gebruikt de klasse precies hetzelfde:

```python
laptop = Product("Laptop", 799.99, 5)
print(laptop.naam)        # "Laptop"
print(laptop.prijs)       # 799.99
print(laptop)             # Product(naam='Laptop', prijs=799.99, voorraad=5)
```

!!! info "Wat doet @dataclass?"
    De `@dataclass` decorator is een **class decorator** die tijdens het laden van je code automatisch methoden genereert. Je krijgt gratis:

    - `__init__()` - constructor
    - `__repr__()` - string representatie voor debugging
    - `__eq__()` - vergelijking tussen objecten

    Dit scheelt veel typwerk en voorkomt fouten.

## Methoden toevoegen aan dataclasses

Je kunt gewoon methoden toevoegen zoals bij normale klassen:

```python
from dataclasses import dataclass

@dataclass
class Product:
    naam: str
    prijs: float
    voorraad: int = 0

    def verkoop(self, aantal: int) -> bool:
        """Verkoop een aantal items."""
        if self.voorraad >= aantal:
            self.voorraad -= aantal
            return True
        return False

    def bereken_voorraadwaarde(self) -> float:
        """Bereken totale waarde van voorraad."""
        return self.prijs * self.voorraad


laptop = Product("Laptop", 799.99, 5)
laptop.verkoop(2)
print(f"Voorraadwaarde: €{laptop.bereken_voorraadwaarde():.2f}")
# Output: Voorraadwaarde: €2399.97
```

## Type hints verdieping

Nu je dataclasses gebruikt, is het tijd om meer type hints te leren kennen.

### Optional - waarden die None kunnen zijn

Soms mag een waarde `None` zijn:

```python
from dataclasses import dataclass
from typing import Optional

@dataclass
class Product:
    naam: str
    prijs: float
    voorraad: int = 0
    beschrijving: Optional[str] = None  # Mag None zijn

laptop = Product("Laptop", 799.99, 5, "Gaming laptop")
muis = Product("Muis", 25.50, 10)  # Geen beschrijving

if laptop.beschrijving:
    print(laptop.beschrijving)
```

!!! tip "Optional is een shortcut"
    `Optional[str]` is hetzelfde als `str | None` (Python 3.10+). Het betekent: "een string OF None".

### List - lijsten met types

Voor lijsten geef je aan welk type elementen erin zitten:

```python
from dataclasses import dataclass, field

@dataclass
class Winkelwagen:
    klant_naam: str
    producten: list[Product] = field(default_factory=list)

    def voeg_toe(self, product: Product) -> None:
        """Voeg een product toe aan de winkelwagen."""
        self.producten.append(product)

    def bereken_totaal(self) -> float:
        """Bereken totaalprijs van alle producten."""
        return sum(p.prijs for p in self.producten)


wagen = Winkelwagen("Jan Jansen")
wagen.voeg_toe(Product("Laptop", 799.99))
wagen.voeg_toe(Product("Muis", 25.50))
print(f"Totaal: €{wagen.bereken_totaal():.2f}")
# Output: Totaal: €825.49
```

!!! note "field(default_factory=list)"
    Voor **mutable** default waarden (lists, dicts) moet je `field(default_factory=list)` gebruiken in plaats van `= []`.

    **Waarom?** Een gewoon `= []` zou gedeeld worden tussen alle instanties (Python quirk). Met `default_factory` krijgt elke instantie zijn eigen lege lijst.

## Validatie met Pydantic

Dataclasses valideren je data niet automatisch. Voor validatie kun je **Pydantic** gebruiken:

```python
from pydantic import BaseModel, Field, field_validator

class Product(BaseModel):
    naam: str = Field(min_length=1)
    prijs: float = Field(gt=0)  # gt = greater than
    voorraad: int = Field(ge=0, default=0)  # ge = greater or equal

    @field_validator('prijs')
    @classmethod
    def prijs_positief(cls, v: float) -> float:
        if v <= 0:
            raise ValueError('Prijs moet positief zijn')
        return v


# Dit werkt:
laptop = Product(naam="Laptop", prijs=799.99, voorraad=5)

# Dit geeft een foutmelding:
try:
    kapot = Product(naam="", prijs=-10, voorraad=5)
except ValueError as e:
    print(f"Validatiefout: {e}")
# Output: Validatiefout: String should have at least 1 character
```

!!! info "Pydantic vs Dataclasses"
    **Dataclasses:** Eenvoudig, built-in Python, geen validatie

    **Pydantic:** Externe library, automatische validatie, type coercion, JSON serialization

    **Voor deze cursus:** Dataclasses is genoeg voor nu. Pydantic zie je later bij API's (FastAPI).

## Preview: Database modellen

Database modellen (die je later gaat maken) lijken erg op dataclasses:

```python
# Dit is hoe SQLAlchemy 2.0+ modellen eruitzien:
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass

class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    naam: Mapped[str] = mapped_column(String(100))
    prijs: Mapped[float]
    voorraad: Mapped[int] = mapped_column(default=0)
```

Zie je de overeenkomst? Type annotations + class attributes, net als dataclasses!

## Volledige voorbeeld: Webshop

Een compleet voorbeeld met dataclasses:

```python
from dataclasses import dataclass, field
from typing import Optional

@dataclass
class Product:
    naam: str
    prijs: float
    voorraad: int = 0

    def verkoop(self, aantal: int) -> bool:
        if self.voorraad >= aantal:
            self.voorraad -= aantal
            return True
        return False


@dataclass
class Klant:
    naam: str
    email: str
    korting_percentage: float = 0.0

    def bereken_korting(self, bedrag: float) -> float:
        """Bereken korting op een bedrag."""
        return bedrag * (self.korting_percentage / 100)


@dataclass
class Bestelling:
    klant: Klant
    producten: list[Product] = field(default_factory=list)
    betaald: bool = False

    def voeg_product_toe(self, product: Product) -> None:
        """Voeg een product toe aan de bestelling."""
        self.producten.append(product)

    def bereken_subtotaal(self) -> float:
        """Bereken subtotaal (zonder korting)."""
        return sum(p.prijs for p in self.producten)

    def bereken_totaal(self) -> float:
        """Bereken totaal (met korting)."""
        subtotaal = self.bereken_subtotaal()
        korting = self.klant.bereken_korting(subtotaal)
        return subtotaal - korting


# Gebruik
jan = Klant("Jan Jansen", "jan@email.nl", korting_percentage=10.0)
bestelling = Bestelling(klant=jan)

laptop = Product("Laptop", 799.99, 5)
muis = Product("Muis", 25.50, 20)

bestelling.voeg_product_toe(laptop)
bestelling.voeg_product_toe(muis)

print(f"Subtotaal: €{bestelling.bereken_subtotaal():.2f}")
print(f"Korting: €{jan.bereken_korting(bestelling.bereken_subtotaal()):.2f}")
print(f"Totaal: €{bestelling.bereken_totaal():.2f}")

# Output:
# Subtotaal: €825.49
# Korting: €82.55
# Totaal: €742.94
```

## Wanneer dataclasses gebruiken?

**Gebruik dataclasses:**
- Voor klassen die vooral data bevatten
- Veel attributen, weinig logica
- Je wilt clean, leesbare code

**Gebruik reguliere klassen:**
- Complexe initialization logic nodig
- Veel custom dunder methods (`__len__`, `__iter__`, etc.)
- Geen data container maar echt gedrag

!!! tip "Database modellen zijn dataclass-achtig"
    SQLAlchemy modellen die je later maakt, gebruiken hetzelfde patroon: type annotaties met class attributen. Als je dataclasses begrijpt, begrijp je ook de moderne SQLAlchemy syntax.

## Samenvatting

Je hebt nu gezien:

- **Dataclasses**: Minder boilerplate voor data containers met `@dataclass`
- **Type hints**: `Optional[str]`, `list[Product]` voor complexere types
- **field()**: Voor mutable defaults met `default_factory`
- **Pydantic**: Optionele validatie library
- **Preview**: Database modellen volgen hetzelfde patroon

### Belangrijkste voordelen dataclasses

1. **Minder code** - geen repetitieve `__init__`
2. **Automatische methoden** - `__repr__`, `__eq__` gratis
3. **Type safety** - duidelijk welke attributen een klasse heeft
4. **Voorbereidend** - SQLAlchemy modellen werken vergelijkbaar

### Volgende stap

In het volgende deel: **inheritance** - hoe klassen van elkaar kunnen erven. Dit is essentieel voor database modellen.

---

**Maak nu [oefening 2](oefeningen/oop-oefening2.md).**
