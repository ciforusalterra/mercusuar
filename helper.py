import aiohttp
import asyncpg


class ConnectionSession():

    async def __aenter__(self) -> aiohttp.ClientSession:
        self.session = aiohttp.ClientSession()
        return self.session

    async def __aexit__(self) -> None:
        await self.session.close()


class DatabaseSession():

    def __init__(self, pool: asyncpg.create_pool):
        self.pool = pool

    async def __aenter__(self) -> asyncpg.Connection:
        self.conn = await self.pool.acquire()
        return self.conn

    async def __aexit__(self) -> None:
        await self.pool.release(self.conn)
