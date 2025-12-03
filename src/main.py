import asyncio
import sys

from sqlalchemy import text

from src.db.db_service import DBService  # шлях підлаштуй під себе якщо інший

db = DBService()


async def test_connection():
    await db.create_tables()

    async with db.get_session() as session:
        result = await session.execute(text("SELECT 1;"))
        print("DB working! Result =", result.scalar_one())


async def main():
    """
    Буде дві команди:
    - get_data      -> потім реалізуєш парсинг та збереження даних
    - print_data    -> потім додаси агрегацію та вивід
    Поки лише тестово перевіряємо підключення.
    """

    if len(sys.argv) > 1:
        cmd = sys.argv[1]

        if cmd == "get_data":
            await test_connection()
        elif cmd == "print_data":
            await test_connection()
        else:
            print("Unknown command")
    else:
        print("Usage: python src/main.py <get_data|print_data>")


if __name__ == "__main__":
    asyncio.run(main())
