from typing import Union

from notifier.model import Log
from notifier.repository.development import NotifierRepository as PhysicalNotifierRepository


class NotifierRepository:

    def __init__(self, inner: PhysicalNotifierRepository):
        self.inner: PhysicalNotifierRepository = inner

    def add_log(self, log: Log) -> Union[Log, bool]:
        return self.inner.add_log(log)
