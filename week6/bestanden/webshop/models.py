"""
SQLAlchemy models voor de webshop applicatie.

Dit bestand bevat alle database models (ORM) voor de webshop.
We gebruiken SQLAlchemy in plaats van raw SQL queries.

Models:
- Category: Productcategorieën
- Product: Producten (met foreign key naar Category)
- Customer: Klanten
- Order: Bestellingen (met foreign key naar Customer)
- OrderItem: Bestelregels (many-to-many tussen Order en Product)
"""
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Category(db.Model):
    """Model voor productcategorieën.

    Relationships:
        products: One-to-Many naar Product
    """
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)

    # Relationship
    products = db.relationship('Product', backref='category', lazy=True)

    def __init__(self, name: str, description: str | None = None):
        """Maak nieuwe categorie aan.

        Args:
            name: Categorienaam
            description: Optionele beschrijving
        """
        self.name = name
        self.description = description

    def __repr__(self) -> str:
        """String representatie voor debugging."""
        return f'<Category {self.name}>'

    @property
    def product_count(self) -> int:
        """Tel aantal producten in deze categorie.

        Returns:
            Aantal producten
        """
        return len(self.products)


class Product(db.Model):
    """Model voor producten.

    Attributes:
        id: Primary key
        name: Productnaam
        price: Prijs in euro's
        stock: Voorraad aantal
        description: Product beschrijving
        category_id: Foreign key naar Category

    Relationships:
        category: Many-to-One naar Category (via backref)
        order_items: One-to-Many naar OrderItem
    """
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False, default=0)
    description = db.Column(db.Text)

    # Foreign Key
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)

    # Relationship
    order_items = db.relationship('OrderItem', backref='product', lazy=True)

    def __init__(
        self,
        name: str,
        price: float,
        stock: int,
        category_id: int,
        description: str | None = None
    ):
        """Maak nieuw product aan.

        Args:
            name: Productnaam
            price: Prijs in euro's
            stock: Voorraad aantal
            category_id: ID van de categorie
            description: Optionele beschrijving
        """
        self.name = name
        self.price = price
        self.stock = stock
        self.category_id = category_id
        self.description = description

    def __repr__(self) -> str:
        """String representatie voor debugging."""
        return f'<Product {self.name}>'

    @property
    def in_stock(self) -> bool:
        """Check of product op voorraad is.

        Returns:
            True als voorraad > 0
        """
        return self.stock > 0


class Customer(db.Model):
    """Model voor klanten.

    Attributes:
        id: Primary key
        name: Klantnaam
        email: Email adres (uniek)
        password_hash: Gehashed wachtwoord (Week 7)
        created_at: Registratie datum

    Relationships:
        orders: One-to-Many naar Order
    """
    __tablename__ = 'customers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200))  # Week 7: Authentication
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationship
    orders = db.relationship('Order', backref='customer', lazy=True)

    def __init__(self, name: str, email: str):
        """Maak nieuwe klant aan.

        Args:
            name: Klantnaam
            email: Email adres
        """
        self.name = name
        self.email = email

    def __repr__(self) -> str:
        """String representatie voor debugging."""
        return f'<Customer {self.name}>'

    @property
    def order_count(self) -> int:
        """Tel aantal bestellingen van deze klant.

        Returns:
            Aantal bestellingen
        """
        return len(self.orders)


class Order(db.Model):
    """Model voor bestellingen.

    Attributes:
        id: Primary key
        customer_id: Foreign key naar Customer
        order_date: Bestellingsdatum
        status: Bestellingstatus
        total_amount: Totaalbedrag

    Relationships:
        customer: Many-to-One naar Customer (via backref)
        order_items: One-to-Many naar OrderItem
    """
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    order_date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(50), default='Pending')  # Pending, Confirmed, Shipped, Delivered
    total_amount = db.Column(db.Float, default=0.0)

    # Relationship
    order_items = db.relationship('OrderItem', backref='order', lazy=True, cascade='all, delete-orphan')

    def __init__(self, customer_id: int):
        """Maak nieuwe bestelling aan.

        Args:
            customer_id: ID van de klant
        """
        self.customer_id = customer_id

    def __repr__(self) -> str:
        """String representatie voor debugging."""
        return f'<Order {self.id} - {self.status}>'

    def calculate_total(self) -> float:
        """Bereken totaalbedrag van bestelling.

        Returns:
            Totaalbedrag in euro's
        """
        total = sum(item.subtotal for item in self.order_items)
        self.total_amount = total
        return total

    @property
    def item_count(self) -> int:
        """Tel aantal items in bestelling.

        Returns:
            Aantal order items
        """
        return sum(item.quantity for item in self.order_items)


class OrderItem(db.Model):
    """Model voor bestelregels (many-to-many tussen Order en Product).

    Attributes:
        id: Primary key
        order_id: Foreign key naar Order
        product_id: Foreign key naar Product
        quantity: Aantal
        price: Prijs op moment van bestellen

    Relationships:
        order: Many-to-One naar Order (via backref)
        product: Many-to-One naar Product (via backref)
    """
    __tablename__ = 'order_items'

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    price = db.Column(db.Float, nullable=False)  # Prijs op moment van bestellen

    def __init__(self, order_id: int, product_id: int, quantity: int, price: float):
        """Maak nieuwe bestelregel aan.

        Args:
            order_id: ID van de bestelling
            product_id: ID van het product
            quantity: Aantal
            price: Prijs per stuk
        """
        self.order_id = order_id
        self.product_id = product_id
        self.quantity = quantity
        self.price = price

    def __repr__(self) -> str:
        """String representatie voor debugging."""
        return f'<OrderItem {self.quantity}x Product #{self.product_id}>'

    @property
    def subtotal(self) -> float:
        """Bereken subtotaal van deze order regel.

        Returns:
            Quantity * price
        """
        return self.quantity * self.price
