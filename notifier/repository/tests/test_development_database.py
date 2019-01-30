from datetime import datetime
from unittest import TestCase, mock

from lib.cpyasynctest.cpyasynctest import async_mock, run_async

from notifier.model import Log
from notifier.repository.development import NotifierRepository


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
        run_async(self.notifier_repository.add_log(log))
        self.session.fetchval.mock.assert_called_once_with('''
            INSERT INTO log(status, message, created_date)
            VALUES ($1, $2, $3)
        ''', log.status, log.message, log.created_date)
