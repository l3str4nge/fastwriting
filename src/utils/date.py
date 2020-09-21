from datetime import datetime


def date_to_str(date: datetime, format="%Y_%m_%d_%H_%M") -> str:
    return date.strftime(format)


def now_to_str() -> str:
    return date_to_str(datetime.now())