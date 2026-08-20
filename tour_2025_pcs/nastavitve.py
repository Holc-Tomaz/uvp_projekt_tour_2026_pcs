from pathlib import Path

BASE_URL = "https://www.procyclingstats.com"
TOUR_URL = f"{BASE_URL}/race/tour-de-france/2025"

KOREN = Path(__file__).resolve().parent
DATA = KOREN / "data"

ETAPE_CSV = DATA / "tour_2025_etape.csv"
REZULTATI_CSV = DATA / "tour_2025_rezultati.csv"
KOLESARJI_CSV = DATA / "tour_2025_kolesarji.csv"
RAZSIRJENO_CSV = DATA / "tour_2025_razsirjeno.csv"


def pripravi_mape():
    DATA.mkdir(exist_ok=True)
