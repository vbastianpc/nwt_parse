from sqlalchemy import select

from ..utils import browser
from . import session
from . import get
from .schema import Edition
from .schema import Book
from .schema import Language


def languages():
    data = browser.open('https://www.jw.org/en/languages/').json()
    wol = browser.open('https://wol.jw.org/en/wol/li/r1/lp-e').soup
    aa = wol.find('ul', class_='librarySelection').find_all('a')

    def map_language(insert=None, update=None):
        for lang in data['languages']:
            if any((e := a) for a in aa if a.get('data-meps-symbol') == lang['langcode']):
                # 40x faster than a = wol.find('a', attrs={'data-meps-symbol': lang['langcode']})
                a = e
            else:
                a = {}
            exists = session.query(select(Language).where(Language.code == lang['symbol']).exists()).scalar()
            if (insert is True and not exists) or (update is True and exists):
                yield dict(
                    code=lang['symbol'], # other names: symbol, locale
                    meps_symbol=lang['langcode'], # other names: code, langcode, wtlocale, data-meps-symbol
                    name=lang['name'],
                    vernacular=lang['vernacularName'],
                    script=lang['script'],
                    is_rtl=lang['direction'] == 'rtl',
                    rsconf=a.get('data-rsconf'),
                    lib=a.get('data-lib'),
                    is_sign_language=lang['isSignLanguage'],
                    is_counted=lang['isCounted'],
                    has_web_content=lang['hasWebContent']
                )
    session.bulk_insert_mappings(Language, map_language(insert=True))
    session.bulk_update_mappings(Language, map_language(update=True))
    session.commit()



def editions(language_code: str = None):
    if language_code is not None and get.edition(language_code):
        return
    data = browser.open("https://www.jw.org/en/library/bible/json/").json()
    edts = []
    for d in data['langs'].values():
        language_meps_symbol = d['lang']['langcode']
        language = get.language(meps_symbol=language_meps_symbol)
        if not language:
            continue
        for e in d['editions']:
            if not get.edition(language_code=language.code):
                edts.append(Edition(
                    language_code=language.code,
                    name=e['title'],
                    symbol=e['symbol'],
                    url=e.get('contentAPI')
                ))
    session.add_all(edts)
    session.commit()


def books(language_code: str, lazy=True):
    if lazy and get.books(language_code):
        return
    edition = get.edition(language_code)
    if not edition:
        edition = Edition(language_code=language_code, symbol='nwt')
        session.add(edition)
        session.commit()
    if edition.url:
        _fetch_books_json(edition)
    else:
        _fetch_books_wol(edition)


def _fetch_books_json(edition: Edition) -> None:
    data = browser.open(edition.url).json()
    bks = []
    for booknum, bookdata in data['editionData']['books'].items():
        book = get.book(language_code=edition.language.code, booknum=booknum, edition_id=edition.id)
        if book:
            continue
        bks.append(Book(
            edition_id=edition.id,
            number=int(booknum),
            name=bookdata.get('standardName'),
            standard_abbreviation=bookdata.get('standardAbbreviation'),
            official_abbreviation=bookdata.get('officialAbbreviation'),
            standard_singular_bookname=bookdata.get('standardSingularBookName'),
            standard_singular_abbreviation=bookdata.get('standardSingularAbbreviation'),
            official_singular_abbreviation=bookdata.get('officialSingularAbbreviation'),
            standard_plural_bookname=bookdata.get('standardPluralBookName'),
            standard_plural_abbreviation=bookdata.get('standardPluralAbbreviation'),
            official_plural_abbreviation=bookdata.get('officialPluralAbbreviation'),
            book_display_title=bookdata.get('bookDisplayTitle'),
            chapter_display_title=bookdata.get('chapterDisplayTitle')
        ))
    session.add_all(bks)
    session.commit()


def _fetch_books_wol(edition: Edition) -> None:
    "https://wol.jw.org/wol/finder?wtlocale=BRS&pub=nwt"
    browser.open(f'https://wol.jw.org/wol/finder?wtlocale={edition.language.meps_symbol}&pub=nwt')
    books = browser.page.find('ul', class_='books hebrew clearfix').findChildren('li', recursive=False) + \
            browser.page.find('ul', class_='books greek clearfix').findChildren('li', recursive=False)
    bks = []
    for bk in books:
        book = get.book(language_code=edition.language.code, booknum=int(bk.a['data-bookid']), edition_id=edition.id)
        if book:
            continue
        bks.append(Book(
            edition_id=edition.id,
            number=int(bk.a['data-bookid']),
            name=bk.a.find('span', class_="title ellipsized name").text,
            standard_abbreviation=bk.a.find('span', class_="title ellipsized abbreviation").text,
            official_abbreviation=bk.a.find('span', class_="title ellipsized official").text,
            standard_singular_bookname=bk.a.find('span', class_="title ellipsized name").text,
            standard_singular_abbreviation=bk.a.find('span', class_="title ellipsized abbreviation").text,
            official_singular_abbreviation=bk.a.find('span', class_="title ellipsized official").text,
            standard_plural_bookname=bk.a.find('span', class_="title ellipsized name").text,
            standard_plural_abbreviation=bk.a.find('span', class_="title ellipsized abbreviation").text,
            official_plural_abbreviation=bk.a.find('span', class_="title ellipsized official").text,
            book_display_title=bk.a.find('span', class_="title ellipsized name").text,
            chapter_display_title=bk.a.find('span', class_="title ellipsized name").text
        ))
    session.add_all(bks)
    session.commit()
