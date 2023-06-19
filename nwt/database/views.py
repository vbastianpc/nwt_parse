# https://github.com/sqlalchemy/sqlalchemy/wiki/Views
# I don't have idea how implement create views by sqlalchemy orm. So...

views = '''
CREATE VIEW IF NOT EXISTS ViewBooks AS
SELECT
    Book.BookId,
    Language.LanguageCode,
    Language.LanguageMepsSymbol,
    Book.BookNumber,
    Book.StandardName
FROM
    Book
INNER JOIN Language ON Language.LanguageCode = Edition.LanguageCode
INNER JOIN Edition ON Edition.EditionId = Book.EditionId
;

CREATE VIEW IF NOT EXISTS ViewEdition AS
SELECT
	Language.LanguageCode,
	Edition.EditionId,
	Language.LanguageMepsSymbol AS MepsSymbol,
	Language.LanguageName,
	Edition.SymbolEdition AS Pub,
	Edition.Name,
	Edition.URL
FROM Language
LEFT JOIN Edition ON Language.LanguageCode = Edition.LanguageCode
;'''.split(';')
