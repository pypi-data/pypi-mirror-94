""" Loading module and variables """

# Internals
import os
import re
import sys
import argparse

# Externals
import numpy
from matplotlib.pyplot import *
from matplotlib        import rc
from astropy.io        import fits
from scipy.ndimage     import gaussian_filter1d
    
def makeatomlist(atompath):
    """
    Store data from atom.dat.

    Parameters
    ----------
    atompath : str
      Path to atom.dat file.
    """
    def isfloat(value):
        try:
            float(value)
            return True
        except ValueError:
            return False
    
    atomlist    = numpy.empty((0,6))
    atomdat     = numpy.loadtxt(atompath,dtype='str',delimiter='\n')
    for element in atomdat:
        l       = element.split()
        i       = 0    if len(l[0])>1 else 1
        species = l[0] if len(l[0])>1 else l[0]+l[1]
        wave    = 0 if len(l)<i+2 or isfloat(l[i+1])==False else l[i+1]
        f       = 0 if len(l)<i+3 or isfloat(l[i+2])==False else l[i+2]
        gamma   = 0 if len(l)<i+4 or isfloat(l[i+3])==False else l[i+3]
        mass    = 0 if len(l)<i+5 or isfloat(l[i+4])==False else l[i+4]
        alpha   = 0 if len(l)<i+6 or isfloat(l[i+5])==False else l[i+5]
        if species!='end' and species[0].isalpha()==True: 
            atomlist = numpy.vstack((atomlist,[species,wave,f,gamma,mass,alpha]))
    return atomlist

def makecustomlist(original,atompath):
    '''
    Get atomic data from selected atomID

    Parameters
    ----------
    original : numpy.array
      Original atom.dat data
    atompath : str
      Path to custom list of metal transitions

    Return
    ------
    atomlist : numpy.array
      New atomic data list with selected transitions only
    '''
    atomlist = numpy.empty((0,6))
    atomdat  = numpy.loadtxt(atompath,dtype='str',ndmin=2)
    for atomID,wrest in atomdat:
        # Identify targeted ion and check list of transitions available in atom.dat
        imet = numpy.where(original[:,0]==atomID)[0]
        # Define target transition parameter list
        target = [0,0,0,0,0,0]
        # List through all transitions found for that ion
        for i in imet:
            # Define transition parameters
            element    = original[i,0]
            wavelength = original[i,1]
            oscillator = original[i,2]  
            gammavalue = original[i,3]
            mass       = original[i,4]
            qcoeff     = original[i,5]
            # Condition 1: transition wavelength must be close to targeted transition
            cond1 = abs( float(wavelength) - float(wrest) ) < 1
            # Condition 2: oscillator strength should be greater than previously found
            cond2 = float(oscillator) > float(target[2])
            # If both condition satisfy, set transition as main target
            if cond1 and cond2:
                target = [element,wavelength,oscillator,gammavalue,mass,qcoeff]
        atomlist = numpy.vstack((atomlist,target))
    return atomlist

def parse_args():
  """Parse command line arguments."""
  parser = argparse.ArgumentParser(prog='QSCAN',description='Manually scanning program of quasar spectra.')
  add_arg = parser.add_argument
  add_arg('spectrum',        help='Path to input spectrum.')
  add_arg('-a','--atom',     help='Input custom atom.dat')
  add_arg('-d','--dv',       help='Custom plotted velocity dispersion.', type=float, default=700)
  add_arg('-f','--fort',     help='Input fort.13 file.')
  add_arg('-l','--list',     help='Custom list of metal transitions.')
  add_arg('-z','--zabs',     help='Starting absorption redshift.', type=float, default=0.1)
  return parser.parse_args()
    
def expand_args(setup):
    datapath         = os.path.abspath(__file__).rsplit('/',1)[0] + '/data/'
    setup.c          = 299792.458
    setup.shift      = -82
    setup.atmolines  = numpy.loadtxt(datapath+'atmolines.dat')
    setup.hydrolist  = makeatomlist(datapath+'hydrolist.dat')[::-1]
    setup.hydroreg   = numpy.zeros((len(setup.hydrolist),4),dtype=object)
    setup.hydrovoigt = numpy.array([[0,numpy.empty((0,5),dtype=object)] \
                                    for i in range(len(setup.hydrolist))],dtype=object)
    setup.dtohflag   = 0
    setup.atmosphere = 0
    setup.wblendmin  = None
    setup.wblendmax  = None
    setup.blendflag  = 0
    setup.z          = 0.01
    setup.anchor     = None
    setup.flag13     = 'no'
    setup.N,setup.b  = 19,10
    setup.mode       = 'scan'
    setup.edgeforce  = []
    setup.dvprev     = None
    setup.atom       = makeatomlist(setup.atom if setup.atom!=None else datapath+'atom.dat')
    setup.zprev      = setup.zabs
    setup.metallist  = makeatomlist(datapath+'metallist.dat')[::-1]
    setup.metalreg   = numpy.zeros((len(setup.metallist),4),dtype=object)
    setup.metalvoigt = numpy.array([[0,numpy.empty((0,5),dtype=object)] \
                                    for i in range(len(setup.metallist))], dtype=object)
    if setup.list!=None:
        setup.metallist = makecustomlist(setup.atom,setup.list)[::-1]
        setup.metalreg   = numpy.zeros((len(setup.metallist),4),dtype=object)
        setup.metalvoigt = numpy.array([[0,numpy.empty((0,5),dtype=object)] \
                                        for i in range(len(setup.metallist))], dtype=object)
    return setup

if os.path.basename(sys.argv[0])=='qscan':
    setup = expand_args(parse_args())
