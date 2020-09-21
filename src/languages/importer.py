import csv

from src.database.models import Dictionary
from src.languages.base import BaseWordImporter


class WordsImporter(BaseWordImporter):

    def from_file(self, filename: str) -> list:
        with open(filename, newline='') as f:
            self.words = [row.replace('\n', '') for row in list(f.readlines())[1:]]
            return self.words

    def to_db(self):
        try:
            for i, word in enumerate(self.words):
                self.destination.add(Dictionary(id=i+1, word=str(word)))

            self.destination.commit()
        except Exception as e:
            self.destination.rollback()
