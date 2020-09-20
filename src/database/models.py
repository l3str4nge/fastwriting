from sqlalchemy import Column, Integer, String, ForeignKey, Date

from .base import Base


class Language(Base):
    __tablename__ = 'language'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)


class Dictionary(Base):
    __tablename__ = 'dictionary'

    id = Column(Integer, primary_key=True, index=True)
    word = Column(String(100))
    lang = Column(Integer, ForeignKey("language.id"), index=True)
