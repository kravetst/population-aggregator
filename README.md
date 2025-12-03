# Population Aggregator

The **Population Aggregator** project allows you to collect information about countries and their populations from various sources (Wikipedia) and store it in a PostgreSQL database. In the future, it will be possible to expand the services and add other parsers for other sites.

---

## ⚠️ Don't Forget
Before running service, you should create **_.env_** file with valid access data for db

## 🚀 Features

- Parsing country and population data:
- [Wikipedia](https://en.wikipedia.org/wiki/List_of_countries_and_dependencies_by_population)
- Asynchronous parsing using `httpx` and `selectolax`
- Playwright support for dynamic content sites
- Data storage in PostgreSQL
- Launch via Docker and Docker Compose

---

## 📦 Technologies

- Python 3.11
- HTTP client: `httpx`
- HTML parser: `selectolax`
- PostgreSQL
- Docker + Docker Compose

---

## ⚡ Installation and launch

1. **Cloning the repository**

```bash
git clone https://github.com/kravetst/population-aggregator.git
cd population-aggregator
```

2. **Running Command**

```bash
docker-compose build
docker-compose up get_data
docker-compose up print_data
```
