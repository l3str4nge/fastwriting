from datetime import timedelta
from freezegun.api import FrozenDateTimeFactory


def move_in_time_forward_by(freezer: FrozenDateTimeFactory, hours: int = 0, minutes: int = 0, seconds: int = 0):
    freezer.move_to(freezer.time_to_freeze + timedelta(hours=hours, minutes=minutes, seconds=seconds))
