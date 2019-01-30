from typing import Union
from urllib.parse import urlencode

from aiohttp import ClientSession

from config import config
from rule_output.model import GetLastActiveInvoice


class RuleOutputGateway:

    def __init__(self, session: ClientSession):
        self.session: ClientSession = session

    async def get_last_active_invoice(self, params: GetLastActiveInvoice) -> Union[GetLastActiveInvoice, bool]:
        url: str = config.get('rule_output', 'url')
        port: int = int(config.get('rule_output', 'port'))
        async with self.session.get(url, port=port, params=params.__dict__) as response:
            if response.status == 200:
                body: dict = await response.json()
                result: GetLastActiveInvoice = GetLastActiveInvoice()
                result.__dict__ = body
                return result
            else:
                return False
