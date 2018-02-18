import webbrowser
import codecs

with codecs.open('secondary-key.tmp', 'r', encoding='utf-8') as fo:
    for line in fo:
        value = line[14:]
        
webbrowser.open("https://www.google.com/search?site=&source=hp&q=" + value)
