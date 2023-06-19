from pathlib import Path
(Path(__file__).parent / 'database' / 'database.db').unlink(missing_ok=True)

import sqlite3
import xml.etree.ElementTree as ET
from zipfile import ZipFile
# from pathlib import Path

from .database import PATH_DB
from .database import fetch
from .utils import browser


url = 'https://download-a.akamaihd.net/files/media_publication/96/nwt_E.jwpub'
nwt = Path(url).name
contents = 'contents'
nwtdb = Path(url).stem + '.db'

def get_nwt_db(overwrite=False):
    if overwrite is False and Path(nwt).exists():
        print('Already exists nwt.db')
    else:
        print('Downloading nwt Bible')
        with open(nwt, 'wb') as f:
            print(f'Downloading {url}')
            f.write(browser.open(url).content)
    with ZipFile(nwt) as jwpub:
        with jwpub.open(contents, 'r') as c:
            with open(contents, 'wb') as f:
                f.write(c.read())

    with ZipFile(contents) as z:
        with z.open(nwtdb, 'r') as r:
            with open(nwtdb, 'wb') as f:
                f.write(r.read())
    Path(contents).unlink()


def parse_label_verse(html_tag):
    if not html_tag:
        return 0
    root = ET.fromstring(html_tag)
    if root.attrib['class'] == 'vl':
        return int(root.text)
    elif root.attrib['class'] == 'cl':
        return 1


def fetch_nwtdb():
    nwt_con = sqlite3.connect(nwtdb)
    con = sqlite3.connect(PATH_DB)
    nwt_cur = nwt_con.cursor()
    cur = con.cursor()
    chapters = nwt_cur.execute('SELECT BookNumber, ChapterNumber, FirstVerseId, LastVerseId '
                               'FROM BibleChapter').fetchall()
    cur.execute('INSERT INTO Bible (VerseId, BookNumber, ChapterNumber, VerseNumber, IsOmitted) '
                'VALUES (0, 0, 0, 0, 0) ON CONFLICT DO NOTHING')
    for data in chapters:
        booknum, chapternum, first_verse_id, last_verse_id = data
        labels = [label[0] for label in nwt_cur.execute(f'SELECT Label FROM BibleVerse '
                                 f'WHERE BibleVerseId BETWEEN {first_verse_id} AND {last_verse_id}')]
        for versenum in map(parse_label_verse, labels):
            cur.execute('INSERT INTO Bible(BookNumber, ChapterNumber, VerseNumber, IsOmitted) '
                        'VALUES (?, ?, ?, ?) ON CONFLICT DO NOTHING', (booknum, chapternum, versenum, False))
    # https://www.jw.org/finder?wtlocale=E&docid=1001070203&srcid=share&par=17-18
    omitted= [
        (40, 17, 21, 21), # Mat 17:21
        (40, 18, 11, 11), # Mat 18:11
        (40, 23, 14, 14), # Mat 23:14
        (41, 7, 16, 16),  # Mar 7:16
        (41, 9, 44, 44),  # Mar 9:44
        (41, 9, 46, 46),  # Mar 9:46
        (41, 11, 26, 26), # Mar 11:26
        (41, 15, 28, 28), # Mar 15:28
        (41, 16, 9, 20),  # Mar 16:9-20
        (42, 17, 36, 36), # Luc 17:36
        (42, 23, 17, 17), # Luc 23:17
        (43, 5, 4, 4),    # John 5:4
        (43, 7, 53, 53),  # John 7:53
        (43, 8, 1, 11),   # John 8:1-11
        (44, 8, 37, 37),  # Acts 8:37
        (44, 15, 34, 34), # Acts 15:34
        (44, 24, 7, 7),   # Acts 24:7
        (44, 28, 29, 29), # Acts 28:29
        (45, 16, 24, 24), # Rom 16:24
    ]
    for booknum, chapternum, first, last in omitted:
        for verse in range(first, last + 1):
            cur.execute('INSERT INTO Bible(BookNumber, ChapterNumber, VerseNumber, IsOmitted) '
                        'VALUES (?, ?, ?, ?) ON CONFLICT DO UPDATE SET IsOmitted=excluded.IsOmitted',
                        (booknum, chapternum, verse, True))
    con.commit()
    con.close()
    nwt_con.close()
    print('nwt bible ok')

def main():
    print('Starting configuration...')
    get_nwt_db(overwrite=False)
    fetch_nwtdb()
    fetch.languages()
    fetch.editions()
    for language_code in ['en', 'es', 'vi']:
        fetch.books(language_code=language_code)

if __name__ == '__main__':
    main()
