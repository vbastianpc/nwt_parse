from sqlalchemy import select

from database import session
from database.schema import Language
from database.schema import Edition
from database.schema import Book


def sign_languages() -> list[Language]:
    return session.query(Language).filter(Language.is_sign_language == True).order_by(Language.meps_symbol.asc()).all()

def languages() -> list[Language]:
    return session.query(Language).order_by(Language.meps_symbol.asc()).all()

def language(code: str | None = None, meps_symbol: str | None = None) -> Language | None:
    q = session.query(Language)
    if code is not None:
        q = q.filter(Language.code == code)
    elif meps_symbol is not None:
        q = q.filter(Language.meps_symbol == meps_symbol)
    else:
        raise TypeError('get_language expected one argument')
    return q.one_or_none()


def parse_language(code_or_meps: str) -> Language | None:
    return language(code=code_or_meps.lower()) or language(meps_symbol=code_or_meps.upper())


def sign_languages_meps_symbol() -> list[str]:
    return session.scalars(select(Language.meps_symbol).filter(Language.is_sign_language == True)).all()

def edition(language_code: str) -> Edition | None:
    return (session
            .query(Edition)
            .join(Language)
            .filter(Language.code == language_code)
            .order_by(Edition.id.asc())
            .limit(1)
            .one_or_none()
    )

def books(language_code: str = None, booknum: int = None) -> list[Book]:
    q = session.query(Book)
    if isinstance(language_code, str):
        q = (q
             .join(Edition, Edition.id == Book.edition_id)
             .join(Language, Language.code == Edition.language_code)
             .filter(Language.code == language_code)
        )
    if isinstance(booknum, int):
        q = q.filter(Book.number == booknum)
    return q.order_by(Book.number.asc()).all()


def book(language_code: str, booknum: int | str, edition_id: int | None = None) -> Book | None:
    q = (
        session.query(Book)
        .join(Edition, Edition.id == Book.edition_id)
        .join(Language, Language.code == Edition.language_code)
        .filter(
            Book.number == int(booknum),
            Language.code == language_code,
        )
    )
    if isinstance(edition_id, int):
        q = q.filter(Edition.id == edition_id)
    return q.one_or_none()
