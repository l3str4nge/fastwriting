from abc import ABCMeta, abstractmethod

from src.database.base import SessionLocal


class BaseWordImporter(metaclass=ABCMeta):
    destination = SessionLocal()
    file = ""
    words = []

    @abstractmethod
    def from_file(self, filename: str) -> list:
        pass