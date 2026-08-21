import re

from bs4 import BeautifulSoup
from nastavitve import BASE_URL, TOUR_URL
from pretvorbe import cas_v_sekunde, normaliziraj_besedilo, v_float, v_int
from splet import absolutni_url, pridobi_html


def poisci_etape():
    html = pridobi_html(TOUR_URL)
    soup = BeautifulSoup(html, "html.parser")

    etape = {}
    for option in soup.select('option[value*="race/tour-de-france/2026/stage-"]'):
        value = option.get("value", "")
        zadetek = re.search(r"stage-(\d+)", value)
        if zadetek:
            stevilka = int(zadetek.group(1))
            etape[stevilka] = {
                "stage": stevilka,
                "oznaka": normaliziraj_besedilo(option.get_text(" ", strip=True)),
                "url": f"{BASE_URL}/race/tour-de-france/2026/stage-{stevilka}/result/result",
            }

    return [etape[stevilka] for stevilka in sorted(etape)]


def vrstice_besedila(soup):
    return [
        normaliziraj_besedilo(niz)
        for niz in soup.stripped_strings
        if normaliziraj_besedilo(niz)
    ]


def vrednost_za_oznako(vrstice, oznaka):
    for i, vrednost in enumerate(vrstice):
        if vrednost.rstrip(":").lower() == oznaka.lower():
            return vrstice[i + 1]
    return None


def razcleni_podatke_etape(soup, etapa):
    vrstice = vrstice_besedila(soup)
    oznaka = etapa["oznaka"] or ""

    return {
        "stage": etapa["stage"],
        "stage_type": "ITT" if "(ITT)" in oznaka else "RR",
        "date": vrednost_za_oznako(vrstice, "Date"),
        "departure": vrednost_za_oznako(vrstice, "Departure"),
        "arrival": vrednost_za_oznako(vrstice, "Arrival"),
        "distance_km": v_float(vrednost_za_oznako(vrstice, "Distance")),
        "vertical_meters": v_int(vrednost_za_oznako(vrstice, "Vertical meters")),
        "profile_score": v_int(vrednost_za_oznako(vrstice, "ProfileScore")),
        "avg_speed_winner_kmh": v_float(
            vrednost_za_oznako(vrstice, "Avg. speed winner")
        ),
        "won_how": vrednost_za_oznako(vrstice, "Won how"),
    }


def besedilo(element):
    if element is None:
        return None
    return normaliziraj_besedilo(element.get_text(" ", strip=True))


def podatki_casa(celica):
    if celica is None:
        return None, None

    vidni = celica.find("font")
    skriti = celica.select_one("span.hide")

    prikaz = besedilo(vidni) if vidni else besedilo(celica)
    za_racunanje = besedilo(skriti) if skriti else prikaz
    return prikaz, cas_v_sekunde(za_racunanje)


def razcleni_rezultate(soup, stevilka):
    tabela = soup.select_one("#resultsCont .resTab .general table.results")
    if tabela is None:
        raise ValueError(f"Tabela rezultatov za etapo {stevilka} ni bila najdena.")

    rezultati = []
    cas_zmagovalca = None

    for vrstica in tabela.select("tbody > tr"):
        rider_cell = vrstica.select_one("td.ridername")
        rider_link = rider_cell.select_one('a[href^="rider/"]') if rider_cell else None
        if rider_link is None:
            continue

        rider = besedilo(rider_link)
        rider_url = absolutni_url(rider_link["href"])

        celice = vrstica.find_all("td", recursive=False)
        rank_raw = besedilo(celice[0]) if celice else None
        rank = int(rank_raw) if rank_raw and rank_raw.isdigit() else None
        status = "finished" if rank is not None else rank_raw

        time_raw, cas = podatki_casa(vrstica.select_one("td.time"))
        if rank == 1:
            cas_zmagovalca = cas
            stage_gap_seconds = 0
            elapsed_seconds = cas
        elif rank is not None:
            stage_gap_seconds = cas
            elapsed_seconds = (
                cas_zmagovalca + cas
                if cas_zmagovalca is not None and cas is not None
                else None
            )
        else:
            stage_gap_seconds = None
            elapsed_seconds = None

        zastavica = rider_cell.select_one("span.flag")
        nationality_code = None
        if zastavica:
            for razred in zastavica.get("class", []):
                if re.fullmatch(r"[a-z]{2}", razred):
                    nationality_code = razred.upper()
                    break

        gc_position = v_int(besedilo(celice[1])) if len(celice) > 1 else None
        gc_timelag_raw = besedilo(celice[2]) if len(celice) > 2 else None

        rezultati.append(
            {
                "stage": stevilka,
                "rank": rank,
                "status": status,
                "gc_position": gc_position,
                "gc_timelag_seconds": cas_v_sekunde(gc_timelag_raw),
                "bib": v_int(besedilo(vrstica.select_one("td.bibs"))),
                "specialty": besedilo(vrstica.select_one("td.specialty")),
                "age": v_int(besedilo(vrstica.select_one("td.age"))),
                "nationality_code": nationality_code,
                "rider": rider,
                "rider_url": rider_url,
                "team": besedilo(vrstica.select_one('a[href^="team/"]')),
                "uci_points": v_float(besedilo(vrstica.select_one("td.uci_pnt"))),
                "pcs_points": v_float(besedilo(vrstica.select_one("td.pnt"))),
                "time_raw": time_raw,
                "stage_gap_seconds": stage_gap_seconds,
                "elapsed_seconds": elapsed_seconds,
            }
        )

    return rezultati


def pridobi_etapo(etapa):
    html = pridobi_html(etapa["url"])
    soup = BeautifulSoup(html, "html.parser")
    return razcleni_podatke_etape(soup, etapa), razcleni_rezultate(
        soup, etapa["stage"]
    )


def pridobi_breakaway(stevilka):
    url = f"{TOUR_URL}/stage-{stevilka}/statistics/kms-in-the-break"

    html = pridobi_html(url)
    soup = BeautifulSoup(html, "html.parser")

    for tabela in soup.find_all("table"):
        glava = tabela.find("tr")

        if glava is None:
            continue

        naslovi = [
            normaliziraj_besedilo(c.get_text(" ", strip=True))
            for c in glava.find_all(["th", "td"])
        ]

        if "KM in first group" not in naslovi:
            continue

        if "Stages" in naslovi:
            continue

        breakaway = []

        for vrstica in tabela.find_all("tr")[1:]:
            celice = vrstica.find_all("td")

            if len(celice) < 4:
                continue

            rider_link = celice[1].select_one('a[href^="rider/"]')

            if rider_link is None:
                continue

            breakaway.append({
                "stage": stevilka,
                "rider": normaliziraj_besedilo(
                    rider_link.get_text(" ", strip=True)
                ),
                "rider_url": absolutni_url(rider_link["href"]),
                "km_first_group": v_float(
                    celice[2].get_text(" ", strip=True)
                ),
                "km_before_peloton": v_float(
                    celice[3].get_text(" ", strip=True)
                ),
            })

        return breakaway

    return []