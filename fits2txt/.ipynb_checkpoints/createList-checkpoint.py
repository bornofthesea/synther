import os
import sys
from astropy.io import fits


def createlist(listfiledir, listfilename):
    listdir = '/home/morgan/PhD/Data/spectra/' + listfiledir + '/'
    listfile = open(listdir + listfilename + '.lis', 'r')
    runfilename = 'run' + listfilename + '.sh'
    runfile = open(runfilename, 'w')
    for line in listfile:
        #myString = 'python fits2txt.py ' + listdir + str(line) + ' ' + listfilename
        myString = f"python fits2txt.py {listdir}{line} {listfilename}".replace('\n', '')
        runfile.write(myString + '\n')

    runfile.close()


createlist('hp1', 'hp1')
createlist('Ton2', 'ton2')
createlist('n6380', 'n6380')