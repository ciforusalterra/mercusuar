import asyncio
from datetime import datetime
from unittest import TestCase, mock

from notifier.model import Log
from notifier.repository.development import NotifierRepository


def _run(coro):
    """Run the given coroutine."""
    return asyncio.get_event_loop().run_until_complete(coro)


def async_mock(*args, **kwargs):
    """Mock as async"""
    m = mock.MagicMock(*args, **kwargs)

    async def mock_coro(*args, **kwargs):
        return m(*args, **kwargs)

    mock_coro.mock = m
    return mock_coro


class TestDevelopmentDatabase(TestCase):

    def setUp(self):
        """
        Setup session
        :return: None
        """
        self._patcher = mock.patch('asyncpg.Connection', new=async_mock())
        self.session = self._patcher.start()
        self.session.fetchval = async_mock(return_value=False)
        self.notifier_repository = NotifierRepository(self.session)

    def tearDown(self):
        """
        Stop patch
        :return: None
        """
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
        _run(self.notifier_repository.add_log(log))
        self.session.fetchval.mock.assert_called_once_with('''
            INSERT INTO log(status, message, created_date)
            VALUES ($1, $2, $3)
        ''', log.status, log.message, log.created_date)
