from __future__ import annotations
from importlib import import_module

import asyncpg

from config import config
from notifier.repository.caching import NotifierRepository as NotifierRepositoryCaching
from notifier.service.bridge import NotifierService


class NotifierFactory:

    def __init__(self, session: asyncpg.pool):
        self.session = session
        self.repository = None

    async def __aenter__(self) -> NotifierFactory:
        self.repository = FactoryRepository(await self.session.__aenter__())
        return self

    async def __aexit__(self) -> None:
        await self.session.__aexit__()

    def notifier(self) -> NotifierService:
        return NotifierService(self.repository)


class FactoryRepository:

    def __init__(self, session: asyncpg.Connection):
        self.session: asyncpg.Connection = session

    def notifier(self) -> NotifierRepositoryCaching:
        return NotifierRepositoryCaching(NotifierRepository(self.session))


# Import Repository dynamically to be same as environment setup
mode = config.get('runtime', 'mode')
NotifierRepository = None
try:
    NotifierRepository = import_module('notifier.repository.{}.NotifierRepository'.format(mode))
except ImportError:
    NotifierRepository = import_module('notifier.repository.development.NotifierRepository')
