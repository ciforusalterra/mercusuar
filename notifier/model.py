from datetime import datetime


class Log:
    id: int = -1
    status: str = ''
    message: str = ''
    created_date: datetime = datetime.now()
