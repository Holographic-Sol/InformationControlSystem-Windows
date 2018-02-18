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
rawUserDirectory = (mainDir+'/Raw-Indexes/raw-d7_directory-index.py')
csvUserDirectory = (mainDir+'/CSV-Indexes/csv-d7-directory-index.py')

dir_target_d7 = ''
dir_target_root_d7 = ''

live_path = []
indexed_path = []
to_file_path = []

write_request = False

def write_index():
    global dir_target_d7
    global dir_target_root_d7
    global live_path
    global indexed_path
    global write_request
    print('index d7 directory: writing...')
    refreshIndex = open(rawUserDirectory, "w").close()
    for dirname, dirnames, filenames in os.walk(dir_target_d7):
        for subdirname in dirnames:
            fullpath = os.path.join(dir_target_root_d7, dirname, subdirname)
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
    print('index d7 directory: wrote.')
    write_request = False

def get_live_paths():
    global dir_target_d7
    global dir_target_root_d7
    global live_path
    # print('attaining paths...')
    for dirname, dirnames, filenames in os.walk(dir_target_d7):
        for subdirname in dirnames:
            fullpath = os.path.join(dir_target_root_d7, dirname, subdirname)
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
    global dir_target_d7
    global dir_target_root_d7
    with open(config, 'r') as fo:
        for line in fo:
            line = line.strip()
            if line.startswith('DRIVE7:'):
                dir_target_d7 = line.replace('DRIVE7:', '')
                dir_target_d7 = dir_target_d7.strip()
                dir_target_root_d7 = str(dir_target_d7.split('\\')[0]+'\\')
                # print(dir_target_root_d7, dir_target_d7)

while 1 == 1:
    if not os.path.exists(rawUserDirectory):
        open(rawUserDirectory, 'w').close()
    if not os.path.exists(csvUserDirectory):
        open(csvUserDirectory, 'w').close()
    get_config()
    if os.path.exists(dir_target_d7):
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
##    else:
##        print('waiting for path to be updated in config.conf')
##    print('done')
    time.sleep(1)
