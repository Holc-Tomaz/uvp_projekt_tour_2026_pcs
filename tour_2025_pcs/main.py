from csv_pomoc import shrani_csv
from nastavitve import (
    ETAPE_CSV,
    KOLESARJI_CSV,
    RAZSIRJENO_CSV,
    REZULTATI_CSV,
    pripravi_mape,
)
from scrapanje_etap import poisci_etape, pridobi_etapo
from scrapanje_kolesarjev import pridobi_vse_kolesarje


def razsiri_rezultate(rezultati, etape, kolesarji):
    etape_po_stevilki = {etapa["stage"]: etapa for etapa in etape}
    kolesarji_po_url = {kolesar["rider_url"]: kolesar for kolesar in kolesarji}

    return [
        {
            **etape_po_stevilki[rezultat["stage"]],
            **kolesarji_po_url[rezultat["rider_url"]],
            **rezultat,
        }
        for rezultat in rezultati
    ]


def main():
    pripravi_mape()

    etape = []
    rezultati = []

    seznam_etap = poisci_etape()

    for i, etapa in enumerate(seznam_etap, start=1):
        print(f"Etapa {i}/{len(seznam_etap)}")
        podatki_etape, rezultati_etape = pridobi_etapo(etapa)
        etape.append(podatki_etape)
        rezultati.extend(rezultati_etape)

    kolesarji = pridobi_vse_kolesarje(rezultati)
    razsirjeno = razsiri_rezultate(rezultati, etape, kolesarji)

    shrani_csv(ETAPE_CSV, etape)
    shrani_csv(REZULTATI_CSV, rezultati)
    shrani_csv(KOLESARJI_CSV, kolesarji)
    shrani_csv(RAZSIRJENO_CSV, razsirjeno)


if __name__ == "__main__":
    main()
