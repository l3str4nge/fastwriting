import csv

from src.database.models import Dictionary
from src.languages.base import BaseWordImporter


class CSVWordsImporter(BaseWordImporter):

    def from_file(self, filename: str) -> list:
        with open(filename, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
            self.words = [self.extract_word(row) for row in list(reader)[1:]]
            return self.words

    def extract_word(self, element: list):
        try:
            return element[0].split(',')[1]
        except Exception as e:
            print("TODO: LOGGGER")
            return "unknown"

    def to_db(self):
        try:
            for word in self.words:
                self.destination.add(Dictionary(word=str(word)))

            self.destination.commit()
        except Exception as e:
            self.destination.rollback()
