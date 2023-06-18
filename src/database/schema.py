"""
https://dbdiagram.io/d/61417a16825b5b0146029d49
"""

from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.sqltypes import Boolean
from sqlalchemy.sql.sqltypes import Integer
from sqlalchemy.sql.sqltypes import String
from sqlalchemy.dialects.sqlite import DATETIME


DateTime = DATETIME(storage_format="%(year)04d-%(month)02d-%(day)02d %(hour)02d:%(minute)02d:%(second)02d")


class Base:
    """https://stackoverflow.com/a/55749579
    https://stackoverflow.com/a/54034230"""
    def __repr__(self):
        params = [f'{k}={v!r}' for k, v in self.__dict__.items() if k not in ['_sa_instance_state', '_sa_adapter']]
        params = ',\n    '.join(params)
        return f'<{self.__class__.__name__}(\n    {params}\n)>'

Base = declarative_base(cls=Base)

class Bible(Base):
    __tablename__ = 'Bible'
    __table_args__ = (UniqueConstraint('BookNumber', 'ChapterNumber', 'VerseNumber'),)
    id = Column('VerseId', Integer, primary_key=True)
    book = Column('BookNumber', Integer)
    chapter = Column('ChapterNumber', Integer)
    verse = Column('VerseNumber', Integer)
    is_omitted = Column('IsOmitted', Boolean, default=False)


class Language(Base):
    __tablename__ = 'Language'
    code = Column('LanguageCode', String, primary_key=True)
    meps_symbol = Column('LanguageMepsSymbol', String, unique=True, nullable=False)
    name = Column('LanguageName', String)
    vernacular = Column('LanguageVernacular', String)
    rsconf = Column('RsConfigSymbol', String)
    lib = Column('LibrarySymbol', String)
    is_sign_language = Column('IsSignLanguage', Boolean)
    script = Column('LanguageScript', String)
    is_rtl = Column('IsRTL', Boolean)
    has_web_content = Column('HasWebContent', Boolean)
    is_counted = Column('IsCounted', Boolean)

    edition = relationship('Edition', back_populates='language', foreign_keys='[Edition.language_code]')


class Edition(Base):
    __tablename__ = 'Edition'
    __table_args__ = (UniqueConstraint('LanguageCode', 'SymbolEdition'), )

    id = Column('EditionId', Integer, primary_key=True)
    language_code = Column('LanguageCode', Integer, ForeignKey('Language.LanguageCode'), nullable=False)
    name = Column('Name', String)
    symbol = Column('SymbolEdition', String)
    url = Column('URL', String)

    language = relationship('Language', back_populates='edition', foreign_keys=[language_code])
    books = relationship('Book', back_populates='edition', foreign_keys='[Book.edition_id]')


class Book(Base):
    __tablename__ = 'Book'
    __table_args__ = (UniqueConstraint('BookNumber', 'EditionId'), )

    id = Column('BookId', Integer, primary_key=True)
    edition_id = Column('EditionId', Integer, ForeignKey('Edition.EditionId'), nullable=False)
    number = Column('BookNumber', Integer)

    name = Column('StandardName', String, default='')
    standard_abbreviation = Column('StandardAbbreviation', String, default='')
    official_abbreviation = Column('OfficialAbbreviation', String, default='')

    standard_singular_bookname = Column('StandardSingularBookName', String, default='')
    standard_singular_abbreviation = Column('StandardSingularAbbreviation', String, default='')
    official_singular_abbreviation = Column('OfficialSingularAbbreviation', String, default='')

    standard_plural_bookname = Column('StandardPluralBookName', String, default='')
    standard_plural_abbreviation = Column('StandardPluralAbbreviation', String, default='')
    official_plural_abbreviation = Column('OfficialPluralAbbreviation', String, default='')

    refreshed = Column('RefreshedOnDate', DateTime)

    book_display_title = Column('BookDisplayTitle', String, default='')
    chapter_display_title = Column('ChapterDisplayTitle', String, default='')

    edition = relationship('Edition', back_populates='books', foreign_keys=[edition_id])

    @property
    def language(self) -> Language:
        return self.edition.language

