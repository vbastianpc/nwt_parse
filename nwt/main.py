from nwt.jw import BibleEpub


epub = BibleEpub.from_citation('mat 24:13, 14', 'en')

print(epub.get_text(fmt=None), '\n\n')
print(epub.get_text(fmt='HTML'), '\n\n')
print(epub.get_text(fmt='Markdown'), '\n\n')
print(epub.get_text(fmt='Obsidian'), '\n\n')
