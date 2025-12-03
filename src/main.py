import asyncio
import sys

from src.config import get_settings
from src.db.db_service import DBService
from src.services.country_service import CountryService
from src.parsers.countrie_parsers import WikipediaCountryParser

urls = {
    "un": "https://en.wikipedia.org/w/index."
          "php?title=List_of_countries_by_population_(United_Nations)&oldid=1215058959",
}


async def main():
    settings = get_settings()
    db = DBService()
    await db.create_tables()
    country_service = CountryService(db)
    if settings.DATA_SOURCE == "un":
        parser = WikipediaCountryParser(urls[settings.DATA_SOURCE])

    else:
        parser = None

    if parser is None:
        print("No data source")
        return

    if len(sys.argv) < 2:
        print("Usage: python src/main.py <get_data|print_data>")
        return

    cmd = sys.argv[1]
    if cmd == "get_data":
        countries = await parser.fetch_countries()
        await country_service.save_countries(countries)
        print(f"Saved {len(countries)} countries")
    elif cmd == "print_data":
        summary = await country_service.get_region_summary()
        for row in summary:
            print(f"{row.region}\n"
                  f"Total population: {row.total_population}\n"
                  f"Largest country: {row.largest_country} ({row.largest_population})\n"
                  f"Smallest country: {row.smallest_country} ({row.smallest_population})\n")
    else:
        print("Unknown command")

if __name__ == "__main__":
    asyncio.run(main())
