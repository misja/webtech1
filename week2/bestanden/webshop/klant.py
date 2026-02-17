class Klant:
    """Klasse voor klanten in de webshop met krediet en korting."""

    def __init__(self, naam: str, email: str):
        """Maak een nieuwe klant aan.

        Args:
            naam: Naam van de klant
            email: Email adres van de klant
        """
        self.naam = naam
        self.email = email
        self.__krediet = 1000.0  # Startkrediet voor nieuwe klanten
        self.__korting = 0.0  # Standaard geen korting

    @property
    def krediet(self) -> float:
        """Getter voor krediet.

        Returns:
            Huidig krediet in euro's
        """
        return self.__krediet

    @krediet.setter
    def krediet(self, waarde: float) -> None:
        """Setter voor krediet met validatie.

        Args:
            waarde: Nieuw krediet (moet >= 0 zijn)
        """
        if waarde >= 0:
            self.__krediet = waarde
        else:
            print("Krediet kan geen negatieve waarde krijgen")
            self.__krediet = 0

    @property
    def korting(self) -> float:
        """Getter voor korting.

        Returns:
            Korting als decimaal (0.15 = 15%)
        """
        return self.__korting

    @korting.setter
    def korting(self, waarde: float) -> None:
        """Setter voor korting met validatie.

        Args:
            waarde: Korting tussen 0 en 1.0 (0.15 = 15%)
        """
        if 0 <= waarde <= 1.0:
            self.__korting = waarde
        else:
            print("Korting moet tussen 0 en 1.0 liggen")

    @property
    def volledige_naam(self) -> str:
        """Read-only property die volledige naam returnt.

        Returns:
            Naam met email tussen haakjes
        """
        return f"{self.naam} ({self.email})"

    def __str__(self) -> str:
        """String representatie van de klant."""
        return f"Klant: {self.naam}, Email: {self.email}, Krediet: €{self.__krediet:.2f}"


if __name__ == '__main__':
    # Test de Klant klasse
    jan = Klant("Jan Jansen", "jan@email.nl")
    print(jan)

    # Test properties
    print(f"\nKrediet: €{jan.krediet:.2f}")

    jan.korting = 0.15
    print(f"Korting: {jan.korting * 100}%")

    # Test validatie
    jan.korting = 2.0  # Dit wordt afgewezen

    jan.krediet = jan.krediet - 300.0
    print(f"Nieuw krediet: €{jan.krediet:.2f}")

    # Test read-only property
    print(f"\nVolledige naam: {jan.volledige_naam}")
