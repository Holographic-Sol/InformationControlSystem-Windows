# FILE-INDEXER/VALUE-GENERATOR, Written by Benjamin Jack Cullen

import os
import sys
import csv
import time
import codecs
import distutils.dir_util
import fileinput
import datetime

# Files & Paths
mainDir = 'Indexes'
encode = u'\u5E73\u621015\u200e,'
config = 'config.conf'
rawPath = (mainDir+'/Raw-Indexes')
csvPath = (mainDir+'/CSV-Indexes')
distutils.dir_util.mkpath(rawPath)
distutils.dir_util.mkpath(csvPath)
rawUserDirectory = (mainDir+'/Raw-Indexes/raw-user-directory-index.py')
csvUserDirectory = (mainDir+'/CSV-Indexes/csv-user-directory-index.py')

dir_target_aud = ''
dir_target_vid = ''
dir_target_img = ''
dir_target_txt = ''

dir_target_root_aud = ''
dir_target_root_vid = ''
dir_target_root_txt = ''
dir_target_root_img = ''

live_path = []
indexed_path = []
to_file_path = []

write_request = False

def write_index():
    global dir_target_aud
    global dir_target_vid
    global dir_target_img
    global dir_target_txt
    global dir_target_root_txt
    global dir_target_root_img
    global dir_target_root_vid
    global dir_target_root_aud
    
    global live_path
    global indexed_path
    
    global to_file_path

    global write_request
    
    print('index user directories: writing ...')
    refreshIndex = open(rawUserDirectory, "w").close()
    for dirname, dirnames, filenames in os.walk(dir_target_aud):
        for subdirname in dirnames:
            fullpath = os.path.join(dir_target_root_aud, dirname, subdirname)
            # print('writing path:',fullpath)
            to_file_path.append(fullpath)

    for dirname, dirnames, filenames in os.walk(dir_target_vid):
        for subdirname in dirnames:
            fullpath = os.path.join(dir_target_root_vid, dirname, subdirname)
            # print('writing path:',fullpath)
            to_file_path.append(fullpath)
            

    for dirname, dirnames, filenames in os.walk(dir_target_img):
        for subdirname in dirnames:
            fullpath = os.path.join(dir_target_root_img, dirname, subdirname)
            # print('writing path:',fullpath)
            to_file_path.append(fullpath)

    for dirname, dirnames, filenames in os.walk(dir_target_txt):
        for subdirname in dirnames:
            fullpath = os.path.join(dir_target_root_txt, dirname, subdirname)
            # print('writing path:',fullpath)
            to_file_path.append(fullpath)

    i = 0
    for to_file_paths in to_file_path:
        txtFile = codecs.open(rawUserDirectory, "a", encoding="utf-8")
        # print('writing path:', to_file_path[i])
        txtFile.writelines(to_file_path[i] + "\n")
        txtFile.close()
        i += 1
    time.sleep(2)
    open(csvUserDirectory, "w").close
    ifile  = codecs.open(rawUserDirectory, "r", encoding="utf-8")
    reader = csv.reader(ifile)
    ofile  = codecs.open(csvUserDirectory, "w", encoding="utf-8")
    writer = csv.writer(ofile, delimiter='	', quotechar='"', quoting=csv.QUOTE_ALL)
    for row in reader:
        writer.writerow(row)
    ifile.close()
    ofile.close()
    print('index user directories: wrote ...')
    write_request = False

def get_live_paths():
    global dir_target_aud
    global dir_target_vid
    global dir_target_img
    global dir_target_txt
    global dir_target_root_txt
    global dir_target_root_img
    global dir_target_root_vid
    global dir_target_root_aud
    global live_path
    for dirname, dirnames, filenames in os.walk(dir_target_aud):
        for subdirname in dirnames:
            fullpath = os.path.join(dir_target_root_aud, dirname, subdirname)
            if fullpath not in live_path:
                # print('live path:',fullpath)
                live_path.append(fullpath)

    for dirname, dirnames, filenames in os.walk(dir_target_vid):
        for subdirname in dirnames:
            fullpath = os.path.join(dir_target_root_vid, dirname, subdirname)
            if fullpath not in live_path:
                # print('live path:',fullpath)
                live_path.append(fullpath)
                
    for dirname, dirnames, filenames in os.walk(dir_target_img):
        for subdirname in dirnames:
            fullpath = os.path.join(dir_target_root_img, dirname, subdirname)
            if fullpath not in live_path:
                # print('live path:',fullpath)
                live_path.append(fullpath)
    for dirname, dirnames, filenames in os.walk(dir_target_txt):
        for subdirname in dirnames:
            fullpath = os.path.join(dir_target_root_txt, dirname, subdirname)
            if fullpath not in live_path:
                # print('live path:',fullpath)
                live_path.append(fullpath)

def get_indexed_paths():
    global indexed_path
    global csvUserDirectory
    with codecs.open(rawUserDirectory, 'r', encoding='utf-8') as fo:
        for line in fo:
            line = line.strip()
            line = line.replace('"','')
            if line not in indexed_path:
                # print('indexed path:', line)
                indexed_path.append(line)

def compare_index_to_live_path():
    global live_path
    global indexed_path
    global write_request
    # print('comparing indexed paths to live paths')
    i = 0
    for indexed_paths in indexed_path:
        if indexed_path[i] not in live_path:
            # print('not in fs:', indexed_path[i])
            write_request = True
        i += 1

def compare_live_path_to_index():
    global live_path
    global indexed_path
    global write_request
    # print('comparing live paths to indexed paths')
    i = 0
    for live_paths in live_path:
        if live_path[i] not in indexed_path:
            # print('not indexed:',live_path[i])
            write_request = True
        i += 1
    
def get_config():
    global dir_target_aud
    global dir_target_vid
    global dir_target_img
    global dir_target_txt
    global dir_target_root_txt
    global dir_target_root_img
    global dir_target_root_vid
    global dir_target_root_aud
    with open(config, 'r') as fo:
        for line in fo:
            line = line.strip()
            if line.startswith('DIRAUD:'):
                dir_target_aud = line.replace('DIRAUD:', '')
                dir_target_aud = dir_target_aud.strip()
                dir_target_root_aud = str(dir_target_aud.split('\\')[0]+'\\')
                # print(dir_target_root_aud, dir_target_aud)

            if line.startswith('DIRVID:'):
                dir_target_vid = line.replace('DIRVID:', '')
                dir_target_vid = dir_target_vid.strip()
                dir_target_root_vid = str(dir_target_vid.split('\\')[0]+'\\')
                # print(dir_target_root_vid, dir_target_vid)

            if line.startswith('DIRIMG:'):
                dir_target_img = line.replace('DIRIMG:', '')
                dir_target_img = dir_target_img.strip()
                dir_target_root_img = str(dir_target_img.split('\\')[0]+'\\')
                # print(dir_target_root_img, dir_target_img)

            if line.startswith('DIRTXT:'):
                dir_target_txt = line.replace('DIRTXT:', '')
                dir_target_txt = dir_target_txt.strip()
                dir_target_root_txt = str(dir_target_txt.split('\\')[0]+'\\')
                # print(dir_target_root_txt, dir_target_txt)

while 1 == 1:
    if not os.path.exists(rawUserDirectory):
        open(rawUserDirectory, 'w').close()
    if not os.path.exists(csvUserDirectory):
        open(csvUserDirectory, 'w').close()
    get_config()
    get_live_paths()
    get_indexed_paths()
    compare_index_to_live_path()
    compare_live_path_to_index()
    to_file_path = []
    indexed_path = []
    live_path = []
    if write_request == True:
        # print('re-write request: True')
        write_index()
##    elif write_request == False:
##        print('re-write request: False')
####    print('done')
    time.sleep(1)
