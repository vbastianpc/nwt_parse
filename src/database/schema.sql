
CREATE TABLE "Bible" (
	"VerseId" INTEGER NOT NULL, 
	"BookNumber" INTEGER, 
	"ChapterNumber" INTEGER, 
	"VerseNumber" INTEGER, 
	"IsOmitted" BOOLEAN, 
	PRIMARY KEY ("VerseId"), 
	UNIQUE ("BookNumber", "ChapterNumber", "VerseNumber")
)

;
CREATE TABLE "Language" (
	"LanguageCode" VARCHAR NOT NULL, 
	"LanguageMepsSymbol" VARCHAR NOT NULL, 
	"LanguageName" VARCHAR, 
	"LanguageVernacular" VARCHAR, 
	"RsConfigSymbol" VARCHAR, 
	"LibrarySymbol" VARCHAR, 
	"IsSignLanguage" BOOLEAN, 
	"LanguageScript" VARCHAR, 
	"IsRTL" BOOLEAN, 
	"HasWebContent" BOOLEAN, 
	"IsCounted" BOOLEAN, 
	PRIMARY KEY ("LanguageCode"), 
	UNIQUE ("LanguageMepsSymbol")
)

;
CREATE TABLE "Edition" (
	"EditionId" INTEGER NOT NULL, 
	"LanguageCode" INTEGER NOT NULL, 
	"Name" VARCHAR, 
	"SymbolEdition" VARCHAR, 
	"URL" VARCHAR, 
	PRIMARY KEY ("EditionId"), 
	FOREIGN KEY("LanguageCode") REFERENCES "Language" ("LanguageCode"), 
	UNIQUE ("LanguageCode", "SymbolEdition")
)

;
CREATE TABLE "Book" (
	"BookId" INTEGER NOT NULL, 
	"EditionId" INTEGER NOT NULL, 
	"BookNumber" INTEGER, 
	"StandardName" VARCHAR, 
	"StandardAbbreviation" VARCHAR, 
	"OfficialAbbreviation" VARCHAR, 
	"StandardSingularBookName" VARCHAR, 
	"StandardSingularAbbreviation" VARCHAR, 
	"OfficialSingularAbbreviation" VARCHAR, 
	"StandardPluralBookName" VARCHAR, 
	"StandardPluralAbbreviation" VARCHAR, 
	"OfficialPluralAbbreviation" VARCHAR, 
	"RefreshedOnDate" DATETIME, 
	"BookDisplayTitle" VARCHAR, 
	"ChapterDisplayTitle" VARCHAR, 
	PRIMARY KEY ("BookId"), 
	FOREIGN KEY("EditionId") REFERENCES "Edition" ("EditionId"), 
	UNIQUE ("BookNumber", "EditionId")
)

;