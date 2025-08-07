def setxTicks(ax, N = 5):
    xmin, xmax = ax.get_xlim()
    custom_ticks = np.linspace(xmin, xmax, N, dtype=int)
    ax.set_xticks(custom_ticks)
    ax.set_xticklabels(custom_ticks)

def plotP(flist, obsf, labels,
             starname = '',
             syntdir = "/home/morgan/Turbospectrum2019/COM-v19.1/syntspec/",
             apogdir = "/home/morgan/PhD/Data/apogee/",
             xlim1 = (15702,15720), xlim2 = (16480,16488), ylim1 = (0.84,1.01), ylim2 = (0.84,1.01),
             xoffset1 = 0, yoffset1 = 0, ncorr1 = 1,
             xoffset2 = 0, yoffset2 = 0, ncorr2 = 1):
    """
    This function will plot the region around the lines of P, S and K in the IR with the input for a list of synthetic spectra and a APOGEE one
    :param flistac:  List of names of files containing the synthetic spectra used for the P lines, around 15600 and 16600, 
                as to include the PI line in 16482.9, in flux per wavelength
    :param flistbc:  List of name of files containing the synthetic spectra in the range for the S and K lines, 
                from 15000 to 16000.
    :param obsf:  Name of the file containing the observed spectra from APOGEE. 
                This spectra is not normalized, so additional normalization parameters should be entered as well
    :param norm: Normalization parameters to be divided from flux values, one for each range around the interested lines, to be entered manually for each input star. 
                Five parameters, ordered for: PI 15711.6, PI 16482.9, KI 15163.067 and KI 15168.376, SI 15469.8036, SI 15475.604 and SI 15478.469.
    """

    fname = apogdir + obsf
    apogdata = pd.read_csv(fname, sep='\s+', header=None, names=["Wavelength", "Flux"], comment="#")
    
    specdata = []
    
    for f in flist:
        fname = syntdir + f
        specdata.append(pd.read_csv(fname, sep='\s+', header=None, names=["Wavelength", "Flux"]))

    norm = [apogdata[apogdata['Wavelength'].between(15702,15720)]['Flux'].median(),
           apogdata[apogdata['Wavelength'].between(16480,16490)]['Flux'].median()]

    # PI lines plots

    fig, ax = plt.subplots(2)

    ax[0].plot(apogdata["Wavelength"] + xoffset1, (apogdata["Flux"]/norm[0])/ncorr1 + yoffset1, color="red", label="obs")
    for d, l in zip(specdata, labels):
        ax[0].plot(d["Wavelength"], d["Flux"], label = l)

    ax[0].set_title("PI lines - " + starname)
    ax[0].set_xlim(*xlim1)
    ax[0].set_ylim(*ylim1)
    ax[0].vlines(x = 15711.6, ymin = 1.0, ymax=1.05, color="purple") # PI 15711.6
    setxTicks(ax[0])

    
    ax[1].plot(apogdata["Wavelength"] + xoffset2, (apogdata["Flux"]/norm[1])/ncorr2 + yoffset2, color="red", label="obs")
    for d, l in zip(specdata, labels):
        ax[1].plot(d["Wavelength"], d["Flux"], label = l)

    ax[1].set_xlim(*xlim2)
    ax[1].set_ylim(*ylim2)
    ax[1].set_xlabel("Wavelength (A)")
    ax[1].vlines(x = 16482.9, ymin = 1.0, ymax=1.05, color="purple") # PI 16482.9
    setxTicks(ax[1])
    plt.legend(loc = 'lower left')
    figname = starname + "_p.png"
    plt.savefig(figname)
    plt.show()


    
def plotK(flist, obsf, labels,
             starname = '',
             syntdir = "/home/morgan/Turbospectrum2019/COM-v19.1/syntspec/",
             apogdir = "/home/morgan/PhD/Data/apogee/",
             xlim1 = (15160,15170), ylim1 = (0.84,1.01),
             xoffset1 = 0, yoffset1 = 0, ncorr1 = 1):
    """
    This function will plot the region around the lines of P, S and K in the IR with the input for a list of synthetic spectra and a APOGEE one
    :param flistac:  List of names of files containing the synthetic spectra used for the P lines, around 15600 and 16600, 
                as to include the PI line in 16482.9, in flux per wavelength
    :param flistbc:  List of name of files containing the synthetic spectra in the range for the S and K lines, 
                from 15000 to 16000.
    :param obsf:  Name of the file containing the observed spectra from APOGEE. 
                This spectra is not normalized, so additional normalization parameters should be entered as well
    :param norm: Normalization parameters to be divided from flux values, one for each range around the interested lines, to be entered manually for each input star. 
                Five parameters, ordered for: PI 15711.6, PI 16482.9, KI 15163.067 and KI 15168.376, SI 15469.8036, SI 15475.604 and SI 15478.469.
    """

    fname = apogdir + obsf
    apogdata = pd.read_csv(fname, sep='\s+', header=None, names=["Wavelength", "Flux"], comment="#")
    
    specdata = []
    
                        
    for f in flist:
        fname = syntdir + f
        specdata.append(pd.read_csv(fname, sep='\s+', header=None, names=["Wavelength", "Flux"]))

    norm = apogdata[apogdata['Wavelength'].between(15155,15175)]['Flux'].median()
    
    # These set of parameters are the limits of each plot, around the zones containing our lines of interest
    lim = (15160, 15170)

    # KI lines plot

    fig, ax = plt.subplots()

    ax.plot(apogdata["Wavelength"] + xoffset1, (apogdata["Flux"]/norm)/ncorr1 + yoffset1, color="red", label="obs")
    for d, l in zip(specdata, labels):
        ax.plot(d["Wavelength"], d["Flux"], label = l)

    ax.set_title("KI lines - " + starname)
    ax.set_xlim(*xlim1)
    ax.set_ylim(*ylim1)
    ax.vlines(x = [15163.067, 15168,376], ymin = 1.0, ymax=1.05, color="purple") # KI 15163.067 and KI 15168.376
    setxTicks(ax)
    plt.legend(loc = 'lower left')
    figname = starname + "_k.png"
    plt.savefig(figname)
    plt.show()



    
def plotS(flist, obsf, labels,
             starname = '',
             syntdir = "/home/morgan/Turbospectrum2019/COM-v19.1/syntspec/",
             apogdir = "/home/morgan/PhD/Data/apogee/",
             xlim1 = (15465, 15473), xlim2 = (15472, 15482), ylim1 = (0.84,1.01), ylim2 = (0.84,1.01),
             xoffset1 = 0, yoffset1 = 0, ncorr1 = 1,
             xoffset2 = 0, yoffset2 = 0, ncorr2 = 1):
    """
    This function will plot the region around the lines of P, S and K in the IR with the input for a list of synthetic spectra and a APOGEE one
    :param flistac:  List of names of files containing the synthetic spectra used for the P lines, around 15600 and 16600, 
                as to include the PI line in 16482.9, in flux per wavelength
    :param flistbc:  List of name of files containing the synthetic spectra in the range for the S and K lines, 
                from 15000 to 16000.
    :param obsf:  Name of the file containing the observed spectra from APOGEE. 
                This spectra is not normalized, so additional normalization parameters should be entered as well
    :param norm: Normalization parameters to be divided from flux values, one for each range around the interested lines, to be entered manually for each input star. 
                Five parameters, ordered for: PI 15711.6, PI 16482.9, KI 15163.067 and KI 15168.376, SI 15469.8036, SI 15475.604 and SI 15478.469.
    """

    fname = apogdir + obsf
    apogdata = pd.read_csv(fname, sep='\s+', header=None, names=["Wavelength", "Flux"], comment="#")
    
    specdata = []
    
    for f in flist:
        fname = syntdir + f
        specdata.append(pd.read_csv(fname, sep='\s+', header=None, names=["Wavelength", "Flux"]))

    norm = [apogdata[apogdata['Wavelength'].between(15465,15475)]['Flux'].median(),
           apogdata[apogdata['Wavelength'].between(15470,15485)]['Flux'].median()]
    
    # These set of parameters are the limits of each plot, around the zones containing our lines of interest
    lim1 = (15465, 15473)
    lim2 = (15472, 15482)

    fig, ax = plt.subplots(2)

    ax[0].plot(apogdata["Wavelength"] + xoffset1, (apogdata["Flux"]/norm[0])/ncorr1 + yoffset1, color="red", label="obs")
    for d, l in zip(specdata, labels):
        ax[0].plot(d["Wavelength"], d["Flux"], label = l)

    ax[0].set_title("SI lines - " + starname)
    ax[0].set_xlim(*xlim1)
    ax[0].set_ylim(*ylim1)
    ax[0].vlines(x = 15469.8036, ymin = 1.0, ymax=1.05, color="purple") # SI 15469.8036
    setxTicks(ax[0])
    
    ax[1].plot(apogdata["Wavelength"] + xoffset2, (apogdata["Flux"]/norm[0])/ncorr2 + yoffset2, color="red", label="obs")
    for d, l in zip(specdata, labels):
        ax[1].plot(d["Wavelength"], d["Flux"], label = l)
    
    ax[1].set_xlim(*xlim2)
    ax[1].set_ylim(*ylim2)
    ax[1].set_xlabel("Wavelength (A)")
    ax[1].vlines(x = [15475.604, 15478.469], ymin = 1.0, ymax=1.05, color="purple") # SI 15475.604 and SI 15478.469
    setxTicks(ax[1])
    plt.legend(loc = 'lower left')
    figname = starname + "_s.png"
    plt.savefig(figname)
    plt.show()


def plotC(flist, obsf, labels,
             starname = '',
             syntdir = "/home/morgan/Turbospectrum2019/COM-v19.1/syntspec/",
             apogdir = "/home/morgan/PhD/Data/apogee/",
             xlim1 = (15520, 15555), xlim2 = (15555, 15575), xlim3 = (15575, 15590), 
             ylim1 = (0.75, 1.05), ylim2 = (0.75, 1.05), ylim3 = (0.75, 1.05),
             xoffset1 = 0, yoffset1 = 0, ncorr1 = 1,
             xoffset2 = 0, yoffset2 = 0, ncorr2 = 1,
             xoffset3 = 0, yoffset3 = 0, ncorr3 = 1):
    """
    This function will plot the region around the lines of P, S and K in the IR with the input for a list of synthetic spectra and a APOGEE one
    :param flistac:  List of names of files containing the synthetic spectra used for the P lines, around 15600 and 16600, 
                as to include the PI line in 16482.9, in flux per wavelength
    :param flistbc:  List of name of files containing the synthetic spectra in the range for the S and K lines, 
                from 15000 to 16000.
    :param obsf:  Name of the file containing the observed spectra from APOGEE. 
                This spectra is not normalized, so additional normalization parameters should be entered as well
    :param norm: Normalization parameters to be divided from flux values, one for each range around the interested lines, to be entered manually for each input star. 
                Five parameters, ordered for: PI 15711.6, PI 16482.9, KI 15163.067 and KI 15168.376, SI 15469.8036, SI 15475.604 and SI 15478.469.
    """

    fname = apogdir + obsf
    apogdata = pd.read_csv(fname, sep='\s+', header=None, names=["Wavelength", "Flux"], comment="#")
    
    specdata = []
    
    for f in flist:
        fname = syntdir + f
        specdata.append(pd.read_csv(fname, sep='\s+', header=None, names=["Wavelength", "Flux"]))

    norm = [apogdata[apogdata['Wavelength'].between(15520,15555)]['Flux'].median(),
           apogdata[apogdata['Wavelength'].between(15555,15575)]['Flux'].median(),
           apogdata[apogdata['Wavelength'].between(15575,15590)]['Flux'].median()]

    # PI lines plots

    fig, ax = plt.subplots(3)

    ax[0].plot(apogdata["Wavelength"] + xoffset1, (apogdata["Flux"]/norm[0])/ncorr1 + yoffset1, color="red", label="obs")
    for d, l in zip(specdata, labels):
        ax[0].plot(d["Wavelength"], d["Flux"], label = l)

    ax[0].set_title("CNO lines - " + starname)
    ax[0].vlines(x = [15528.063, 15528.734, 15529.9, 15530.8, 15534.4, 15540.23, 15541.40, 15542.20, 15542.20, 15542.90, 15544.5, 15550.45, 15550.9, 15552.6, 15553.5, 15554.5], ymin = 1.01, ymax=1.03, color="red") #CN
    ax[0].vlines(x = [15535.46, 15536.7], ymin = 1.01, ymax=1.03, color="green") #OH    
    ax[0].set_xlim(*xlim1)
    ax[0].set_ylim(*ylim1)
    setxTicks(ax[0])

    
    ax[1].plot(apogdata["Wavelength"] + xoffset2, (apogdata["Flux"]/norm[1])/ncorr2 + yoffset2, color="red", label="obs")
    for d, l in zip(specdata, labels):
        ax[1].plot(d["Wavelength"], d["Flux"], label = l)
    
    ax[1].vlines(x = [15555.435, 15557.9, 15558.7, 155561.4, 15562.2, 15563.4, 15573.2], ymin = 1.01, ymax=1.03, color="red") #CN
    ax[1].vlines(x = [15572.1], ymin = 1.01, ymax=1.03, color="purple") #CO
    ax[1].vlines(x = [15560.24, 15565.91, 15568.78], ymin = 1.01, ymax=1.03, color="green") #OH
    ax[1].set_xlim(*xlim2)
    ax[1].set_ylim(*ylim2)
    ax[1].set_xlabel("Wavelength (A)")
    setxTicks(ax[1])

    ax[2].plot(apogdata["Wavelength"] + xoffset3, (apogdata["Flux"]/norm[2])/ncorr3 + yoffset3, color="red", label="obs")
    for d, l in zip(specdata, labels):
        ax[2].plot(d["Wavelength"], d["Flux"], label = l)
    ax[2].vlines(x = [15577.6, 15577.4, 15578.4, 155578.8, 155579.3, 15579.8, 15581.8, 15582.6, 15583.5, 15584.4, 15586.4, 15586.716, 155586.4], ymin = 1.01, ymax=1.03, color="purple") #CO
    ax[2].vlines(x = [15579.8, 15580.2, 15581.0], ymin = 1.01, ymax=1.03, color="red") #CN
    ax[2].set_xlim(*xlim3)
    ax[2].set_ylim(*ylim3)
    ax[2].set_xlabel("Wavelength (A)")
    setxTicks(ax[2])
    
    figname = starname + "_c.png"
    plt.legend(loc = 'lower right')
    plt.savefig(figname)
    plt.show()