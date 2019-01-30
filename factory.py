from __future__ import annotations
from importlib import import_module

import asyncpg
from aiohttp import ClientSession

from config import config
from notifier.repository.caching import NotifierRepository as NotifierRepositoryCaching
from notifier.service.bridge import NotifierService
from rule_output.gateway.caching import RuleOutputGateway as RuleOutputGatewayCaching


class NotifierFactory:

    def __init__(self, session: asyncpg.pool):
        self.session = session
        self.repository = None

    async def __aenter__(self) -> NotifierFactory:
        self.repository = FactoryPostgreRepository(await self.session.__aenter__())
        return self

    async def __aexit__(self) -> None:
        await self.session.__aexit__()

    def notifier(self) -> NotifierService:
        return NotifierService(self.repository)


class RuleOutputFactory:

    def __init__(self, session: ClientSession):
        self.session = session
        self.gateway = FactoryAioClientGateway(session)


class FactoryPostgreRepository:

    def __init__(self, session: asyncpg.Connection):
        self.session: asyncpg.Connection = session

    def notifier(self) -> NotifierRepositoryCaching:
        return NotifierRepositoryCaching(NotifierRepository(self.session))


class FactoryAioClientGateway:

    def __init__(self, session: ClientSession):
        self.session: ClientSession = session

    def rule_output(self) -> RuleOutputGatewayCaching:
        return RuleOutputGatewayCaching(RuleOutputGateway(self.session))


# Import Repository dynamically to be same as environment setup
mode = config.get('runtime', 'mode')
NotifierRepository = None
RuleOutputGateway = None
try:
    NotifierRepository = import_module('notifier.repository.{}.NotifierRepository'.format(mode))
    RuleOutputGateway = import_module('notifier.repository.{}.RuleOutputGateway'.format(mode))
except ImportError:
    NotifierRepository = import_module('notifier.repository.development.NotifierRepository')
    RuleOutputGateway = import_module('notifier.repository.development.RuleOutputGateway')
