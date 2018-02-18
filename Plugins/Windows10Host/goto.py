import webbrowser
import codecs

with codecs.open('secondary-key.tmp', 'r', encoding='utf-8') as fo:
    for line in fo:
        value = line[6:]
        print(value)

value = value.replace(" ", "")
webbrowser.open("www." + value)
