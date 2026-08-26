# Projektna naloga: Tour de France 2026 – zajem in analiza podatkov

Projekt avtomatsko pridobi podatke o dirki **Tour de France 2026** s spletne strani [ProCyclingStats](https://www.procyclingstats.com/).  
Zajemajo se podatki o etapah, rezultatih posameznih etap, kolesarjih in pobegih. Podatki se shranijo v več CSV datotek, ki jih nato uporabimo za analizo v Jupyter Notebooku.

## Struktura projekta

```text
uvp_projekt_tour_2026_pcs/
│
├── README.md
│
└── tour_2026_pcs/
    │
    ├── main.py
    ├── nastavitve.py
    ├── splet.py
    ├── scrapanje_etap.py
    ├── scrapanje_kolesarjev.py
    ├── pretvorbe.py
    ├── csv_pomoc.py
    ├── knjiznice.txt
    ├── analiza_podatkov_2026.ipynb
    │
    └── data/
        ├── tour_2026_etape.csv
        ├── tour_2026_rezultati.csv
        ├── tour_2026_kolesarji.csv
        ├── tour_2026_breakaway.csv
        └── tour_2026_razsirjeno.csv
```

## Opis delovanja

V datoteki `scrapanje_etap.py` so funkcije za pridobivanje seznama etap Toura 2026 ter podatkov o posameznih etapah. Za vsako etapo se pridobijo osnovni podatki, kot so start in cilj, dolžina, višinski metri, tip etape in povprečna hitrost zmagovalca. Iz iste strani se pridobijo tudi rezultati kolesarjev in podatki o pobegih.

V datoteki `scrapanje_kolesarjev.py` se iz profilov posameznih kolesarjev pridobijo dodatni podatki, kot so datum rojstva, narodnost, višina, teža in kraj rojstva.

Datoteka `splet.py` skrbi za pridobivanje spletnih strani, `pretvorbe.py` vsebuje pomožne funkcije za pretvarjanje besedila, števil in časov, `csv_pomoc.py` pa za shranjevanje podatkov v CSV datoteke. V `nastavitve.py` so določeni spletni naslovi in poti do datotek.

Osrednja datoteka `main.py` poveže vse dele projekta. Najprej pridobi podatke in rezultate vseh etap ter podatke o pobegih, nato pridobi še podatke o vseh kolesarjih. Na koncu podatke shrani v pet CSV datotek. Poleg ločenih tabel ustvari tudi `tour_2026_razsirjeno.csv`, v kateri so podatki o etapah, kolesarjih in rezultatih združeni.

Zbrane podatke nato uvozimo v zvezek `analiza_podatkov_2026.ipynb`, kjer jih analiziramo s knjižnicama `pandas` in `matplotlib`. Analiza med drugim prikazuje razvoj skupnega vrstnega reda skozi Tour, časovne zaostanke najboljših kolesarjev, zahtevnost etap, hitrost zmagovalcev, odstopanje kolesarjev ter podatke o pobegih.

## Viri podatkov

Podatki so pridobljeni s spletne strani:

1. [ProCyclingStats – Tour de France 2026](https://www.procyclingstats.com/race/tour-de-france/2026)
2. strani posameznih etap Tour de France 2026 na ProCyclingStats,
3. profili posameznih kolesarjev na ProCyclingStats.

## Navodila za zagon

Za delovanje projekta je potreben Python. Potrebne knjižnice so zapisane v datoteki `knjiznice.txt` in jih lahko namestimo z ukazom:

```bash
pip install -r knjiznice.txt
```

Nato se v mapi `tour_2026_pcs` zažene:

```bash
python main.py
```

Program pridobi podatke s spletne strani ProCyclingStats in jih shrani v mapo `data`.

Za analizo nato odpremo datoteko `analiza_podatkov_2026.ipynb` in po vrsti izvedemo celice v Jupyter Notebooku.
