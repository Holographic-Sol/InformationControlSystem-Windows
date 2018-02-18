Information & Control Framework. written by Benjamin Jack Cullen

Demo:
https://youtu.be/U70NegSQTXY
Demo Indexing:
https://youtu.be/-_8aursdkQ4

Voice controlled information & control framework. Web crawlers
gather information, plugins add compatibility for control.
Indexing allows for formulaic access to files, directories, 
information and control.

Consider it a transparent open source Google Home.

Plugins - is for command files. (.py)
UserPrograms - is for program shortcuts/ scripts(.lnk, .bat)
IndexEngines - index targtet directories for index access via voice.

This progam:
	Defines any word.
	Provides any wiki on request.
	Answers questions.
	Runs command files for control of host and network devices.
	Algorithmic file access.
	Anything you want, its a framework!
	
My framework is over a year old but never had its own gui. Gui
still in dev, this version will remain basic. Framework is advancing.

More web crawlers = more information on request.
More command files = more control.
The framework does the rest.

Naturally, we select a form/app we wish to control before

arbitrarily typing on the keyboard. First say 'show #appname', then
once the application is selected, control the application. In the

case of browser control, no need to first attain control of browser.
Also, naturally we dont usually use two keyboards at once while
spamming applications with multiple inputs from multiple keyboards
at the same time, we use one or the other. If you use this program,
please let the voice commands run before overwriding/interupting
with from other input sources like mouse & keyboard.


With voice keyboard control, comes shortcuts. You can full screen youtube (f)

pause a video with space bar, etc.. know your favourite apps shortcuts.

With index & index access I have made efforts to ensure safety when index
access runs/plays/opens/ a file. These efforts include, minimal file
extension tuples in index engines & user specified directories in which
to look for those tuples. Executable/.bat files are not indexed from
the main host filesystem whatsoever, meaning that only exe/bat/py files
defined by the user in IC-System's 'UserPrograms' directory & 'Plugins'
directory will run on request. If i do implement a deep index access it 
will be prompted access while user specified index access will remain
unprompted, as its logic allows for fast unprompted, safe access to files.
Yes, you could increase the file extension tuple list and set to index from
root, but thats on you. The indexes are kept better up to date by only
indexing what you need.  Else it may take a while before changes in the
target indexed directories to be reflected in the indexes.
Currently Advanced Index Settings for directory indexing only.  While User
Index Settings indexes files & automatically indexes the directories
configured therein. 
Directory index access is by my logic, always unprompted.

WINDOWS 10 HOST CONTROL:
Command List:
key_word = ['stop transcription', 
            'search wikipedia', followed by query terms
            'transcriptions available for', followed by query terms
            'latest transcription for', followed by query terms
            'remove bookmark', followed by query terms
            'define', followed by query terms
            'ask google', followed by query terms
            'play audio', followed by query terms
            'directory', followed by query terms
            'open image', followed by query terms
            'open text', followed by query terms
            'open video', followed by query terms
            'run program', followed by query terms
            'transcription', followed by query terms (different from wiki search. will search all local transcripts made by any crawler)
            ]
'Computer' (followed by):
keyboard_item_key = ['left', 'right', 'down', 'up', 'enter', 'tab', 'back tab', 'next window',
                     'previous window', 'escape', 'page up', 'page down', 'plus', 'minus',
                     'recursively expand folders', 'exclamation', 'hash', 'operand', 'open curly brace',
                     'close curly brace', 'space', 'alternate', 'backspace', 'delete', 'end', 'insert',
                     'f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9', 'f10', 'f11', 'f12', 'prnt screen',
                     'windows key', 'right windows key', 'num lock', 'caps lock', 'scroll lock', 'break', 'pause',
                     'select all', 'copy', 'paste', 'undo', 'redo', 'save', 'display help', 'rename item',
                     'menu', 'cycle title bar', 'close and exit', 'cycle applications', 'display properties',
                     'go back', 'go forward',
                     ]
'google map' followed by query terms
'google earth map' followed by nothing. (use once location has been loaded)
'go to' followed by website name
'search google' followed by query terms
'search youtube' followed by query terms
'select title' followed by query terms (this is the equivelent of clicking hyper text titles (like a video link). for use in browser.)
'youtube video restart'

You can add programs to Plugins directory which adds 'compatibility' for host and network devices like smart tvs, tablets, phones,
anything.. Simply give the subprogram a suitable name and IC-System will run it if you call its name. Like, call the subprogram, 'googlemap.py'...
by saying 'google map hong kong'.