from unittest import TestCase, mock

from lib.cpyasynctest.cpyasynctest import async_mock, run_async

from rule_output.model import GetLastActiveInvoice
from rule_output.gateway.development import RuleOutputGateway


class TestDevelopmentDatabase(TestCase):

    def setUp(self):
        # TODO: Fix mock aiohttp client
        """
        Setup session
        :return: None
        """
        # Setup aiohttp session
        self._patcher = mock.patch('aiohttp.ClientSession', new=async_mock())
        self.session = self._patcher.start()
        self.session.get = async_mock()
        # self.session.get.__aenter__ = async_mock(return_value={'department_id': '1234'})
        # self.session.get.__aexit__ = async_mock()
        # self.session.get.return_value.__aenter__.return_value = {'department_id': '1234'}
        self.session.get.__aenter__ = async_mock()
        self.session.get.status = 200
        self.session.get.json = async_mock(return_value={'department_id': '1234'})
        self.session.get.__aexit__ = async_mock(return_value=True)

        # Setup url and port configuration
        self._config_patcher = mock.patch('config.config')
        self.config = self._config_patcher.start()
        self.config.url = 'localhost'
        self.config.port = '8080'

        # Setup RuleOutputGateway instance
        self.rule_output_gateway = RuleOutputGateway(self.session)

    def tearDown(self):
        """
        Stop patch
        :return: None
        """
        self._patcher.stop()
        self._config_patcher.stop()

    def test_get_last_active_invoice(self):
        """
        Given no param to get_last_active_invoice, it should call rule_out API
        :return: None
        """
        last_active_invoice = GetLastActiveInvoice()
        last_active_invoice.department_id = '1234'
        run_async(self.rule_output_gateway.get_last_active_invoice(last_active_invoice))
        self.session.get.mock.assert_called_once_with(
            self.config.url, port=self.config.port, params=last_active_invoice.__dict__)
