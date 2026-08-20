import re
from time import sleep
from bs4 import BeautifulSoup

from pretvorbe import normaliziraj_besedilo, v_float
from splet import pridobi_html


MESECI = {
    "january": 1,
    "february": 2,
    "march": 3,
    "april": 4,
    "may": 5,
    "june": 6,
    "july": 7,
    "august": 8,
    "september": 9,
    "october": 10,
    "november": 11,
    "december": 12,
}


def besedilo_med_oznakami(besedilo, zacetek, konci):
    vzorec_koncev = "|".join(re.escape(konec) for konec in konci)
    zadetek = re.search(
        rf"{re.escape(zacetek)}\s*(.*?)\s*(?={vzorec_koncev}|$)",
        besedilo,
        re.IGNORECASE,
    )
    return normaliziraj_besedilo(zadetek.group(1)) if zadetek else None


def datum_rojstva_iso(datum):
    if not datum:
        return None

    zadetek = re.search(
        r"(\d{1,2})(?:st|nd|rd|th)?\s+([A-Za-z]+)\s+(\d{4})",
        datum,
        re.IGNORECASE,
    )
    if not zadetek:
        return None

    dan = int(zadetek.group(1))
    mesec = MESECI[zadetek.group(2).lower()]
    leto = int(zadetek.group(3))
    return f"{leto:04d}-{mesec:02d}-{dan:02d}"


def razcleni_profil(html, url, ime_iz_rezultatov):
    soup = BeautifulSoup(html, "html.parser")
    besedilo = normaliziraj_besedilo(soup.get_text(" ", strip=True))

    h1 = soup.find("h1")
    ime = normaliziraj_besedilo(h1.get_text(" ", strip=True)) if h1 else ime_iz_rezultatov

    datum_raw = besedilo_med_oznakami(besedilo, "Date of birth:", ["Nationality:"])
    nationality = besedilo_med_oznakami(
        besedilo,
        "Nationality:",
        ["Weight:", "Height:", "Place of birth:", "Specialties"],
    )
    place_of_birth = besedilo_med_oznakami(
        besedilo,
        "Place of birth:",
        ["Specialties", "All time", "PCS Ranking"],
    )

    teza_zadetek = re.search(r"Weight:\s*(\d+(?:[.,]\d+)?)\s*kg", besedilo)
    visina_zadetek = re.search(r"Height:\s*(\d+(?:[.,]\d+)?)\s*m", besedilo)

    weight = v_float(teza_zadetek.group(1)) if teza_zadetek else None
    height = v_float(visina_zadetek.group(1)) if visina_zadetek else None
    bmi = round(weight / height**2, 2) if weight and height else None

    date_of_birth = datum_rojstva_iso(datum_raw)

    return {
        "rider": ime,
        "rider_url": url,
        "date_of_birth": date_of_birth,
        "birth_year": int(date_of_birth[:4]) if date_of_birth else None,
        "nationality": nationality,
        "height_m": height,
        "weight_kg": weight,
        "bmi": bmi,
        "place_of_birth": place_of_birth,
    }


def pridobi_podatke_kolesarja(ime, url):
    html = pridobi_html(url)
    return razcleni_profil(html, url, ime)


def pridobi_vse_kolesarje(rezultati):
    kolesarji = {
        rezultat["rider_url"]: rezultat["rider"]
        for rezultat in rezultati
    }

    profili = []
    skupaj = len(kolesarji)

    for i, (url, ime) in enumerate(kolesarji.items(), start=1):
        print(f"Kolesar {i}/{skupaj}: {ime}")
        profili.append(pridobi_podatke_kolesarja(ime, url))
        sleep(1)

    return profili
