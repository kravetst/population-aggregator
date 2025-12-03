from sqlalchemy import text
from src.db.db_service import DBService
from src.models.countrie import Country

class CountryService:
    def __init__(self, db: DBService):
        self.db = db

    async def save_countries(self, countries: list[dict]):
        async with self.db.get_session() as session:
            objs = [Country(**c) for c in countries]
            session.add_all(objs)
            await session.commit()

    async def get_region_summary(self):
        async with self.db.get_session() as session:
            query = """
            SELECT
                region,
                SUM(population) AS total_population,
                (SELECT name FROM countries c2 WHERE c2.region = c1.region ORDER BY population DESC LIMIT 1) AS largest_country,
                (SELECT population FROM countries c2 WHERE c2.region = c1.region ORDER BY population DESC LIMIT 1) AS largest_population,
                (SELECT name FROM countries c2 WHERE c2.region = c1.region ORDER BY population ASC LIMIT 1) AS smallest_country,
                (SELECT population FROM countries c2 WHERE c2.region = c1.region ORDER BY population ASC LIMIT 1) AS smallest_population
            FROM countries c1
            GROUP BY region;
            """
            result = await session.execute(text(query))
            return result.mappings().all()
