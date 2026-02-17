"""CRUD operaties demonstratie met SQLAlchemy.

Dit script demonstreert alle CRUD (Create, Read, Update, Delete) operaties:
- CREATE: Nieuwe cursist toevoegen
- READ: Cursisten opvragen (all, get, filter)
- UPDATE: Leeftijd van cursist wijzigen
- DELETE: Cursist verwijderen

Voer eerst setup_database.py uit om de database aan te maken.
"""
from basic_model_app import db, Cursist

###########################
###### CREATE ############
###########################
print("=== CREATE: Nieuwe cursist toevoegen ===")
elsje = Cursist('Elsje', 19)
db.session.add(elsje)
db.session.commit()
print("Elsje toegevoegd\n")

###########################
###### READ ##############
###########################
print("=== READ: Alle cursisten ===")
alle_cursisten = Cursist.query.all()
print(*alle_cursisten, sep='\n')
print()

# Zoeken op ID
print("=== READ: Cursist met ID 2 ===")
cursist_twee = Cursist.query.get(2)
print(cursist_twee)
print(f"Leeftijd: {cursist_twee.leeftijd}")
print()

# Filteren op naam
print("=== READ: Filter op naam 'Elsje' ===")
cursist_elsje = Cursist.query.filter_by(naam='Elsje').first()
print(cursist_elsje)
print()

###########################
###### UPDATE ############
###########################
print("=== UPDATE: Leeftijd wijzigen ===")
cursist_joyce = Cursist.query.get(1)
print(f"Oude leeftijd Joyce: {cursist_joyce.leeftijd}")
cursist_joyce.leeftijd = 40
db.session.add(cursist_joyce)
db.session.commit()
print(f"Nieuwe leeftijd Joyce: {cursist_joyce.leeftijd}")
print()

###########################
###### DELETE ############
###########################
print("=== DELETE: Cursist verwijderen ===")
cursist_elsje = Cursist.query.get(3)
print(f"Te verwijderen: {cursist_elsje}")
db.session.delete(cursist_elsje)
db.session.commit()
print("Elsje verwijderd")
print()

# Overzicht na alle aanpassingen
print("=== FINAL: Overzicht na CRUD operaties ===")
alle_cursisten = Cursist.query.all()
print(*alle_cursisten, sep='\n')
