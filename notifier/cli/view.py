from factory import NotifierFactory
from helper import DatabaseSession


class NotifierHandler:

    def __init__(self, database_session: DatabaseSession):
        self.database_session = database_session

    def repository(self) -> NotifierFactory:
        return NotifierFactory(self.database_session)
