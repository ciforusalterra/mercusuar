from datetime import datetime


class Log:

    def __init__(self):
        self.id: int = -1
        self.status: str = ''
        self.message: str = ''
        self.created_date: datetime = datetime.now()
