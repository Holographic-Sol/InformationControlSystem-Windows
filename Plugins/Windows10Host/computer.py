import os
import win32com.client
import codecs
import time
from pywinauto import application
from pywinauto.SendKeysCtypes import SendKeys
from pywinauto.SendKeysCtypes import SendInput

app = application.Application()
shell = win32com.client.Dispatch("WScript.Shell")

key = ''
value = ''
key_valid = False

with codecs.open('secondary-key.tmp', 'r', encoding='utf-8') as fo:
    for line in fo:
        line = line.strip()
        value = line
        value = value[9:]
        key = value
        spec_value = value[5:]
        print('computer control file:',value)

def left_():
    SendKeys("{LEFT}")
def right_():
    print('foo2')
    SendKeys("{RIGHT}")
def down_():
    SendKeys("{DOWN}")
def up_():
    SendKeys("{UP}")
def enter_():
    SendKeys("{ENTER}")
def tab_():
    SendKeys("{TAB}")
def back_tab_():
    SendKeys("+{TAB}")
def next_window_():
    SendKeys("^{TAB}")
def previous_window_():
    SendKeys("^+{TAB}")
def escape_():
    SendKeys("{ESC}")
def page_up_():
    SendKeys("{PGUP}")
def page_dn_():
    SendKeys("{PGDN}")
def plus_():
    SendKeys("{+}")
def minus_():
    SendKeys("{-}")
def recursively_expand_folders_():
    SendKeys("{NumPadMulti}")
def exclamation_():
    SendKeys("{!}")
def hash_():
    SendKeys("{#}")
def operand_():
    SendKeys("{^}")
def open_curly_brace_():
    SendKeys("{{}")
def close_curly_brace_():
    SendKeys("{}}")
def space_():
    SendKeys("{SPACE}")
def alter_():
    endKeys("{ALT}")
def backspace_():
    SendKeys("{BACKSPACE}")
def delete_():
    SendKeys("{DELETE}")
def end_():
    SendKeys("{END}")
def insert_():
    SendKeys("{INESRT}")
def f1_():
    SendKeys("{F1}")
def f2_():
    SendKeys("{F2}")
def f3_():
    SendKeys("{F3}")
def f4_():
    SendKeys("{F4}")
def f5_():
    SendKeys("{F5}")
def f6_():
    SendKeys("{F6}")
def f7_():
    SendKeys("{F7}")
def f8_():
    SendKeys("{F8}")
def f9_():
    SendKeys("{F9}")
def f10_():
    SendKeys("{F10}")
def f11_():
    SendKeys("{F11}")
def f12_():
    SendKeys("{F12}")
def prnt_screen_():
    SendKeys("{PRINTSCREEN}")
def windows_key_():
    SendKeys("{LWIN}")
def right_windows_key_():
    SendKeys("{RWIN}")
def num_lck_():
    SendKeys("{NUMLOCK}")
def caps_lock_():
    SendKeys("{CAPSLOCK}")
def scroll_lock_():
    SendKeys("{SCROLLLOCK}")
def break_():
    SendKeys("{BREAK}")
def pause_():
    SendKeys("{PAUSE}")
def select_all_():
    shell.SendKeys("^a")
def copy_():
    shell.SendKeys("^C")
def paste_():
    shell.SendKeys("^V")
def undo_():
    shell.SendKeys("^{Z}")
def redo_():
    shell.SendKeys("^+{Z}")
def save_():
    shell.SendKeys("^{S}")
def display_help_():
    shell.SendKeys("{F1}")
def rename_item_():
    shell.SendKeys("{F2}")
def menu_():
    shell.SendKeys("{F10}")
def cycle_title_bar_():
    shell.SendKeys("{F6}")
def close_and_exit_():
    shell.SendKeys("%{F4}")
def cycle_applications_():
    shell.SendKeys("%{ESC}")
def display_properties_():
    shell.SendKeys("%{ENTER}")
def go_back_():
    shell.SendKeys("%{LEFT}")
def go_forward_():
    shell.SendKeys("%{RIGHT}")
    
keyboard_item = {'left' : left_,
                 'right' : right_,
                 'down' : down_,
                 'up' : up_,
                 'enter' : enter_,
                 'tab' : tab_,
                 'back tab' : back_tab_,
                 'next window' : next_window_,
                 'previous window' : previous_window_,
                 'escape' : escape_,
                 'page up' : page_up_,
                 'page down' : page_dn_,
                 'plus' : plus_,
                 'minus' : minus_,
                 'recursively expand folders' : recursively_expand_folders_,
                 'exclamation' : exclamation_,
                 'hash' : hash_,
                 'operand' : operand_,
                 'open curly brace' : open_curly_brace_,
                 'close curly brace' : close_curly_brace_,
                 'space' : space_,
                 'alternate' : alter_,
                 'backspace' : backspace_,
                 'delete' : delete_,
                 'end' : end_,
                 'insert' : insert_,
                 'f1' : f1_,
                 'f2' : f2_,
                 'f3' : f3_,
                 'f4' : f4_,
                 'f5' : f5_,
                 'f6' : f6_,
                 'f7' : f7_,
                 'f8' : f8_,
                 'f9' : f9_,
                 'f10' : f10_,
                 'f11' : f11_,
                 'f12' : f12_,
                 'prnt screen' : prnt_screen_,
                 'windows key' : windows_key_,
                 'right windows key' : right_windows_key_,
                 'num lock' : num_lck_,
                 'caps lock' : caps_lock_,
                 'scroll lock' : scroll_lock_,
                 'break' : break_,
                 'pause' : pause_,
                 'select all' : select_all_,
                 'copy' : copy_,
                 'paste' : paste_,
                 'undo' : undo_,
                 'redo' : redo_,
                 'save' : save_,
                 'display help' : display_help_,
                 'rename item' : rename_item_,
                 'menu' : menu_,
                 'cycle title bar' : cycle_title_bar_,
                 'close and exit' : close_and_exit_,
                 'cycle applications' : cycle_applications_,
                 'display properties' : display_properties_,
                 'go back' : go_back_,
                 'go forward' : go_forward_,
                 }
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

if value.startswith('show'):
    shell.AppActivate(value[5:])
    quit()
    
elif value.startswith('type'):
    shell.SendKeys(value[5:])
    quit()
    
i = 0
for keyboard_item_key in keyboard_item_key:
    if key in keyboard_item:
        my_funk = keyboard_item[key]
        key_valid = True
        break
    i+=1
if key_valid == True:
    my_funk()
