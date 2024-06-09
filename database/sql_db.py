import aiosqlite

from aiosqlite import Connection

class SQLDatabase():
    def __init__(self, path, pool_size=5):
        self.path = path
        self._pool = []
        self._pool_size = pool_size

    async def acquire_connection(self) -> Connection:
        if len(self._pool) < self._pool_size:
            connection = await aiosqlite.connect(self.path)
            self._pool.append(connection)
        return self._pool.pop()

    async def release_connection(self, connection: Connection):
        self._pool.append(connection)

    async def execute(self, query, *args):
        connection = await self.acquire_connection()
        try:
            async with connection.execute(query, args) as cursor:
                await connection.commit()
                return await cursor.fetchall()
        finally:
            await self.release_connection(connection)
    
    async def executemany(self, query, *args):
        connection = await self.acquire_connection()
        try:
            async with connection.executemany(query, args) as cursor:
                await connection.commit()
                return await cursor.fetchall()
        finally:
            await self.release_connection(connection)

    async def fetch_one(self, query, *args):
        connection = await self.acquire_connection()
        try:
            async with connection.execute(query, args) as cursor:
                return await cursor.fetchone()
        finally:
            await self.release_connection(connection)