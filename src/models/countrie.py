from sqlalchemy import Column, Integer, String

from src.db.base import Base


class Country(Base):
    __tablename__ = "countries"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    region = Column(String, nullable=False)
    population = Column(Integer, nullable=False)

    def __repr__(self):
        return f"<Country(name={self.name}, region={self.region}, population={self.population})>"
