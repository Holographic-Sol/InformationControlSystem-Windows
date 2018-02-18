import webbrowser
import codecs

with codecs.open('secondary-key.tmp', 'r', encoding='utf-8') as fo:
    for line in fo:
        value = line[15:]
        print(value)
        
webbrowser.open("https://www.youtube.com/results?search_query=" + value)
