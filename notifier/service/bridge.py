from typing import Union

from notifier.model import Log
from notifier.repository.caching import NotifierRepository


class NotifierService:

    def __init__(self, repository: NotifierRepository):
        self.repository = repository

    def add_log(self, log: Log) -> Union[Log, bool]:
        return self.repository.add_log(log)
