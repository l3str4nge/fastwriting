from datetime import datetime


def date_to_str(date: datetime, format="%Y-%m-%d_%H:%M:%S") -> str:
    return date.strftime(format)


def now_to_str() -> str:
    return date_to_str(datetime.now())