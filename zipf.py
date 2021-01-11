# -*- coding: utf-8 -*-
"""
Created on Mon Jun 13 22:02:24 2016

@author: http://stackoverflow.com/questions/31027739/python-custom-zipf-number-generator-performing-poorly
"""
import numpy

tmp=0.0
def randZipf(catalog_size, alpha, numSamples): 
    n=float(catalog_size)
    # Calculate Zeta values from 1 to n: 
    tmp = numpy.power( numpy.arange(1, n+1), -alpha )
    zeta = numpy.r_[0.0, numpy.cumsum(tmp)]
    # Store the translation map: 
    distMap = [x / zeta[-1] for x in zeta]
    # Generate an array of uniform 0-1 pseudo-random values: 
    u = numpy.random.random(numSamples)
    # bisect them with distMap
    v = numpy.searchsorted(distMap, u)
    samples = [t-1 for t in v]
    return samples
      

