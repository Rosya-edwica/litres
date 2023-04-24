from config import PostgresConfig
import asyncpg


async def connect():
    connection = await asyncpg.connect(
        database=PostgresConfig.Database,
        user=PostgresConfig.User,
        password=PostgresConfig.Pass,
        host=PostgresConfig.Host,
        port=PostgresConfig.Port
    )
    return connection