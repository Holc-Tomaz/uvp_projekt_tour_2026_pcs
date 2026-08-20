from time import sleep
from urllib.parse import urljoin
import requests

import cloudscraper

from nastavitve import BASE_URL


SEJA = cloudscraper.create_scraper(
    browser={"browser": "chrome", "platform": "windows", "desktop": True}
)
SEJA.headers["User-Agent"] = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/120.0.0.0 Safari/537.36"
)


def absolutni_url(href):
    return urljoin(BASE_URL + "/", href)


def pridobi_html(url):
    try:
        odgovor = SEJA.get(url, timeout=30)
        odgovor.raise_for_status()

    except (requests.exceptions.ConnectionError,
            requests.exceptions.HTTPError):
        print("Napaka pri povezavi. Ponovni poskus čez 5 sekund ...")
        sleep(5)

        odgovor = SEJA.get(url, timeout=30)
        odgovor.raise_for_status()

    return odgovor.text
