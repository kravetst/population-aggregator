import re
import httpx
from abc import ABC, abstractmethod
from typing import List, Dict
from selectolax.parser import HTMLParser


def clean_text(text: str) -> str:
    text = re.sub(r"\[.*?\]", "", text)
    return text.strip()


class BaseCountryParser(ABC):

    def __init__(self, url):
        self.url = url

    @abstractmethod
    async def fetch_countries(self) -> List[Dict]:
        pass


class WikipediaCountryParser(BaseCountryParser):

    async def fetch_countries(self) -> List[Dict]:
        async with httpx.AsyncClient(timeout=30, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/142.0.0.0 Safari/537.36"
        }) as client:
            resp = await client.get(self.url)
            resp.raise_for_status()
            html = HTMLParser(resp.text)

        countries = []
        table = html.css_first("table.wikitable")
        if not table:
            return countries

        for row in table.css("tr")[1:]:
            cols = row.css("td")
            if len(cols) < 3:
                continue
            name = clean_text(cols[0].text())
            region_text = clean_text(cols[5].text())
            region = region_text if region_text else "Unknown"
            population_text = clean_text(cols[2].text()).replace(",", "")
            try:
                population = int(population_text)
            except ValueError:
                population = 0

            countries.append({
                "name": name,
                "region": region,
                "population": population
            })

        return countries
