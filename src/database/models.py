from sqlalchemy import Column, Integer, String, ForeignKey, Date

from .base import Base


class Language(Base):
    __tablename__ = 'language'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
