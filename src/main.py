from jw import BibleEpub


epub = BibleEpub.from_human('mat 24:14', 'en')

print(epub.get_text())
print(BibleEpub.from_human('mat 24:14', 'es').get_text())
print(BibleEpub.from_human('mat 24:13', 'es').get_text())