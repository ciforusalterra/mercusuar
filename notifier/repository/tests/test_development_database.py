import asyncio
from datetime import datetime
from unittest import TestCase, mock

import asyncpg

from notifier.model import Log
from notifier.repository.development import NotifierRepository


def _run(coro):
    """Run the given coroutine."""
    return asyncio.get_event_loop().run_until_complete(coro)


class AsyncMock(mock.MagicMock):
    async def __call__(self, *args, **kwargs):
        return super(AsyncMock, self).__call__(*args, **kwargs)


class TestDevelopmentDatabase(TestCase):

    def setUp(self):
        """
        Setup session
        :return: None
        """
        # self.session = mock.create_autospec(asyncpg.Connection)
        # self._patcher = mock.patch('asyncpg.Connection', new_callable=AsyncMock)
        self._patcher = mock.patch('asyncpg.Connection')
        self.session: asyncpg.Connection = self._patcher.start()
        self.notifier_repository = NotifierRepository(self.session)

    def tearDown(self):
        self._patcher.stop()

    def test_add_log(self):
        """
        Given log data to add_log, it should call database
        :return: None
        """
        log = Log()
        log.status = 'success'
        log.message = 'add xyz'
        log.created_date = datetime.now()
        # _run(self.notifier_repository.add_log(log))
        _run(self.notifier_repository.add_log(log))
        assert self.session.fetchval.method.assert_called_once_with('''
            INSERT INTO log(status, message, created_date)
            VALUES ($1, $2, $3)
        ''', log.status, log.message, log.created_date)
