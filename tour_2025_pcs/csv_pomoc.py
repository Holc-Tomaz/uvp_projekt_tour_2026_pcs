import csv


def shrani_csv(pot, podatki):
    if not podatki:
        return

    with pot.open("w", encoding="utf-8-sig", newline="") as datoteka:
        pisec = csv.DictWriter(datoteka, fieldnames=podatki[0].keys())
        pisec.writeheader()
        pisec.writerows(podatki)
