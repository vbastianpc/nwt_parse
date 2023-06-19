from nwt.jw import BibleEpub

epub = BibleEpub.from_citation('mat 24:14', 'es')

print(epub.get_text())
print(BibleEpub.from_citation('mat 24:14', 'es').get_text())
print(BibleEpub.from_citation('mat 24:13', 'es').get_text())
