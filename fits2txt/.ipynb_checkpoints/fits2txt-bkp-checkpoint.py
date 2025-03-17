#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 10:59:07 2024

@author: heitor
Modified by Morgan on 2025 Mar 17
"""

try:
    import pyfits
except:
    from astropy.io import fits as pyfits
 
    
from astropy.io import fits
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import csv
import sys
import math
import os
from matplotlib.ticker import (MultipleLocator, AutoMinorLocator)

sns.set_style("white")
sns.set_context("paper", font_scale=1.5, rc={"lines.linewidth": 1.5})

#---------------      
             
def rv(centre,centre2):
     dwl=centre-centre2
     wl=centre2
     rv= (dwl*299792.458)/wl
     return rv 


def corrv(wl,flux,rv):
    
    
     wlnewl=[]
     for wlp in wl:
         dwl=-(rv/299792.458)*wlp
         wlnew=wlp-dwl
         wlnewl.append(wlnew)
     return [wlnewl,flux]
#---------------      
        

# Example usage

#file_path = '../AP-MR-Bulge/apStar-dr17-2M17193684-2748495.fits' 


#path = '../AP-MR-Bulge/'
#file_path = path + sys.argv[1]  # Path to your FITS file


file_path = sys.argv[1]

name_out = str(file_path.split('/')[-1])[:-5] + '.txt'

print('---------------')
print('Executing for ' + name_out[:-4] + '\n \n')


#making dir to save the output and the fig
try:
    os.system('mkdir save-spec')
except:
    print('save-spec already created')

try:
    os.system('mkdir figs-spec')
except:
    print('figs-spec already created')

#---------------

#opening fits
hdu = pyfits.open(file_path)
#hdu.info

lenn = hdu[0].header['NWAVE']

wavelengths = np.linspace(hdu[1].header['CRVAL1'],hdu[1].header['CRVAL1']+lenn*hdu[1].header['CDELT1'], num=lenn)
wavelengths = 10**wavelengths

if wavelengths is not None:
    print("Wavelength array:", wavelengths)
    print("length",len(wavelengths))
    print('---------------')

#flux ext

flux_data = hdu[1].data[0]

if flux_data is not None:
    print("Flux array:", flux_data)
    print("length",len(flux_data))
    print('---------------')
    
#tellurics
    
tel = hdu[6].data[0]

#sky

sk = hdu[4].data[0]

vhelio = hdu[0].header['VHELIO']
star = hdu[0].header['OBJID']

new_wv, new_fl = corrv(wavelengths,flux_data,vhelio)


#------------------- plotting ------------------------

fig, axs = plt.subplots(1, 2, figsize=(15, 5), sharey=True)

# Remove horizontal space between axes
fig.subplots_adjust(wspace=0)

axs[0].plot(wavelengths, flux_data, color='gray', label = star)
axs[0].plot(new_wv, new_fl, color='k')
axs[0].plot(wavelengths, tel*np.median(flux_data), color='red',alpha=0.5)
axs[0].plot(wavelengths, sk/np.median(sk), color='blue',alpha=0.5)

axs[0].set_ylabel('Flux')
axs[0].tick_params(which="both", bottom=True, top=True, left=True, right=True, direction='in')
axs[0].set_xlabel('Wavelength')

#axs[0].set_ylim([-1.5,1.5])
#axs[0].set_xlim([-1.7,0.7])

axs[0].grid()

#-----

axs[1].title.set_text("Cutted")

axs[1].plot(wavelengths, flux_data, color='gray', label = star)
axs[1].plot(new_wv, new_fl, color='k',label = 'corrected')


axs[1].tick_params(which="both", bottom=True, top=True, left=True, right=True, direction='in')
axs[1].set_xlabel('Wavelength')

axs[1].set_xlim([16700,16800])

axs[1].legend(loc=4)

axs[1].grid()

plt.savefig('figs-spec/flux-'+name_out[:-4]+'.pdf')


#---------------------------------------------------

#Saving spectrum

print('\nSaving spectrum: ')
print(name_out)

with open('save-spec/'+name_out[:-4]+'.txt', 'w') as f:
    writer = csv.writer(f)
    writer.writerows(zip(new_wv, new_fl))

#---------------------------------------------------


plt.close()
hdu.close()




























#
