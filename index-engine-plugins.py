# FILE-INDEXER/VALUE-GENERATOR, Written by Benjamin Jack Cullen

import os
import sys
import csv
import time
import codecs
import distutils.dir_util

rootDir = 'C:\\'
curDir = os.getcwd()
encode = u'\u5E73\u621015\u200e'
rawPath = 'Indexes//'
csvPath = 'Indexes//'
plugin_dir = 'Plugins//'
distutils.dir_util.mkpath(rawPath)
distutils.dir_util.mkpath(csvPath)
distutils.dir_util.mkpath(plugin_dir)
target = 'Indexes//Raw-Indexes//raw-plugin-index.py'
targetCSV = 'Indexes//CSV-Indexes//csv-plugin-index.py'

#print("QUICK INDEX : PROGRAMS")
while 1 == 1:
    open(target, "w").close
    for dirName, subdirList, fileList in os.walk(plugin_dir):
        for fname in fileList:
            lnkext = [".py"]
            if fname.endswith(tuple(lnkext)):
                #print('\t%s' % fname)
                exeFile = codecs.open(target, "a", encoding="utf-8")
                toFile = os.path.join(curDir, dirName, fname)
                exeFile.writelines(toFile.lower() + "\n")
                exeFile.close()
    time.sleep(5)
    #print("Attempting format of updated Index...")
    open(targetCSV, "w").close
    ifile  = codecs.open(target, "r", encoding="utf-8")
    reader = csv.reader(ifile)
    ofile  = codecs.open(targetCSV, "w", encoding="utf8")
    writer = csv.writer(ofile, delimiter='	', quotechar='"', quoting=csv.QUOTE_ALL)
    for row in reader:
        writer.writerow(row)
    ifile.close()
    ofile.close()
    time.sleep(5)
