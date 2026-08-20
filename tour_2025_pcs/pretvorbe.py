import re


def normaliziraj_besedilo(besedilo):
    if besedilo is None:
        return None
    return re.sub(r"\s+", " ", str(besedilo)).strip()


def v_int(vrednost):
    if not vrednost:
        return None
    zadetek = re.search(r"-?\d+", vrednost)
    return int(zadetek.group()) if zadetek else None


def v_float(vrednost):
    if not vrednost:
        return None
    zadetek = re.search(r"-?\d+(?:[.,]\d+)?", vrednost)
    return float(zadetek.group().replace(",", ".")) if zadetek else None


def cas_v_sekunde(cas):
    if not cas or cas in {"-", "--", ",,"}:
        return None

    deli = cas.replace("+", "").replace("*", "").strip().split(":")
    if not all(delcek.isdigit() for delcek in deli):
        return None

    deli = [int(delcek) for delcek in deli]
    if len(deli) == 3:
        ure, minute, sekunde = deli
        return 3600 * ure + 60 * minute + sekunde
    if len(deli) == 2:
        minute, sekunde = deli
        return 60 * minute + sekunde
    return None
