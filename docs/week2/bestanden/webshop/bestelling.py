"""Order klasse voor de webshop - demonstratie van compositie."""

import datetime


class Order:
    """Klasse voor bestellingen in de webshop.

    Een bestelling is samengesteld uit:
    - Een klant (Customer)
    - Een winkelwagen (Cart) met producten
    - Een betaalmethode (PaymentMethod)
    - Verzendkosten
    """

    def __init__(
        self,
        klant: 'Customer',
        winkelwagen: 'Cart',
        betaalmethode: 'PaymentMethod',
        verzendkosten: float = 5.95
    ):
        """Maak een nieuwe bestelling aan.

        Args:
            klant: Customer object
            winkelwagen: Cart object met producten
            betaalmethode: PaymentMethod object
            verzendkosten: Verzendkosten in euro's (default: 5.95)
        """
        self.klant = klant
        self.winkelwagen = winkelwagen
        self.betaalmethode = betaalmethode
        self.verzendkosten = verzendkosten
        self.besteldatum = datetime.datetime.now()
        self.status = "In behandeling"

    def bereken_totaal(self) -> float:
        """Bereken totaalbedrag inclusief verzendkosten.

        Returns:
            Totaalbedrag in euro's (gratis verzending boven €50)
        """
        subtotaal = self.winkelwagen.bereken_totaal()

        # Gratis verzending boven €50
        if subtotaal >= 50:
            return subtotaal
        else:
            return subtotaal + self.verzendkosten

    def plaats_bestelling(self) -> bool:
        """Plaats de bestelling en verwerk de betaling.

        Returns:
            True als bestelling succesvol geplaatst, False bij lege winkelwagen
        """
        if not self.winkelwagen.items:
            print("Kan geen lege bestelling plaatsen!")
            return False

        print(f"\n{'='*50}")
        print(f"BESTELLING VOOR {self.klant.naam}")
        print(f"{'='*50}")

        # Toon producten
        print("\nProducten:")
        for product in self.winkelwagen.items:
            print(f"  - {product}")

        # Bereken kosten
        subtotaal = self.winkelwagen.bereken_totaal()
        print(f"\nSubtotaal: €{subtotaal:.2f}")

        if subtotaal >= 50:
            print("Verzendkosten: €0.00 (GRATIS verzending!)")
            verzending = 0.0
        else:
            print(f"Verzendkosten: €{self.verzendkosten:.2f}")
            verzending = self.verzendkosten

        totaal = subtotaal + verzending
        print(f"Totaal: €{totaal:.2f}")

        # Verwerk betaling
        print(f"\nBetaalmethode: {self.betaalmethode.type}")
        eindtotaal = self.betaalmethode.verwerk_betaling(totaal)

        # Bevestiging
        self.status = "Bevestigd"
        print(f"\nBestelling bevestigd!")
        print(f"Bevestiging verzonden naar {self.klant.email}")
        print(f"Verwachte levering: 2-3 werkdagen")
        print(f"{'='*50}\n")

        return True

    def toon_status(self) -> None:
        """Toon de status van de bestelling."""
        print(f"\nBestellingsnummer: #{id(self)}")
        print(f"Klant: {self.klant.naam}")
        print(f"Datum: {self.besteldatum.strftime('%d-%m-%Y %H:%M')}")
        print(f"Status: {self.status}")
        print(f"Aantal producten: {len(self.winkelwagen.items)}")
        print(f"Totaalbedrag: €{self.bereken_totaal():.2f}")
