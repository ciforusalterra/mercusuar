from typing import Union

from asyncpg import Connection

from notifier.model import Log


class NotifierRepository:

    def __init__(self, session: Connection):
        self.session: Connection = session

    async def add_log(self, log: Log) -> Union[Log, bool]:
        conn = await self.session.fetchval('''
            INSERT INTO log(status, message, created_date)
            VALUES ($1, $2, $3)
        ''', log.status, log.message, log.created_date)
        print(conn)
        return conn or False
