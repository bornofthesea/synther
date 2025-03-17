import os
import sys
from astropy.io import fits

hp1dir = '/home/morgan/PhD/Data/spectra/hp1/'
smcdir = '/home/morgan/PhD/Data/spectra/smc/'

hp1list = open(hp1dir + 'hp1.lis', 'r')
smclist = open(smcdir + 'smc.lis', 'r')

hp1file = open('runhp1.sh', 'w')

for line in hp1list:
    myString = 'python fits2txt.py ' + hp1dir + str(line)
    hp1file.write(myString + '\n')

hp1file.close()

smcfile = open('runsmc.sh', 'w')

for line in smclist:
    myString = 'python fits2txt.py ' + smcdir + str(line)
    smcfile.write(myString + '\n')

smcfile.close()
