from time import sleep
from urllib.parse import urljoin

import requests
from nastavitve import BASE_URL

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}


def absolutni_url(href):
    return urljoin(BASE_URL + "/", href)


def pridobi_html(url):
    for poskus in range(2):
        try:
            odgovor = requests.get(url, headers=HEADERS, timeout=30)
            odgovor.raise_for_status()
            return odgovor.text
        except requests.exceptions.RequestException:
            if poskus == 1:
                raise

            print("Napaka, try čez 5s")
            sleep(5)
