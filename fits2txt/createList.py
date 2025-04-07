import os
import sys
from astropy.io import fits

hp1dir = '/home/morgan/PhD/Data/spectra/hp1/'
smcdir = '/home/morgan/PhD/Data/spectra/smc/'
n6558dir = '/home/morgan/PhD/Data/spectra/n6558/'
n6522dir = '/home/morgan/PhD/Data/spectra/n6522/'
uks1dir = '/home/morgan/PhD/Data/spectra/uks1/'
"""
hp1list = open(hp1dir + 'hp1.lis', 'r')
smclist = open(smcdir + 'smc.lis', 'r')
n6558list = open(n6558dir + '6558.lis', 'r')
n6522list = open(n6522dir + '6522.lis', 'r')
"""
uks1list = open(uks1dir + 'uks1.lis', 'r')
"""

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

n6558file = open('run6558.sh', 'w')

for line in n6558list:
    myString = 'python fits2txt.py ' + n6558dir + str(line)
    n6558file.write(myString + '\n')

n6558file.close()

n6522file = open('run6522.sh', 'w')

for line in n6522list:
    myString = 'python fits2txt.py ' + n6522dir + str(line)
    n6522file.write(myString + '\n')

n6522file.close()
"""
uks1file = open('runuks1.sh', 'w')

for line in uks1list:
    myString = 'python fits2txt.py ' + uks1dir + str(line)
    uks1file.write(myString + '\n')

uks1file.close()