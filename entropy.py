#!/usr/bin/env python
# -*- coding: utf8 -*-

RATE = 44100
BUF = 32

UINT32LIMIT = 1<<32

import sys
import numpy
import pyaudio
import hashlib
import matplotlib.pyplot as plt

pmf = {}

p = pyaudio.PyAudio()

stream = p.open(
    format = pyaudio.paInt32,
    channels = 1,
    rate = RATE,
    input = True,
    output = False,
    frames_per_buffer = BUF
)

n = 1000000
for i in xrange(n):
    if i % 100 == 0:
        sys.stdout.write("\rGathering data... %.2f%%" % (float(i)/n*100))
        sys.stdout.flush()

    s = stream.read(BUF)

    for v in numpy.fromstring(s, dtype=numpy.uint32):
        pmf[v] = pmf.get(v,0) + 1.0

print "\nADC bitsize estimation: %f bits" % numpy.log2(len(pmf.keys()))

pmfsum = 0
i = 0
l = len(pmf)
for x in pmf.values():
    if i % 10000 == 0:
        sys.stdout.write("\rCalculating distribution sum... %.2f%%" % (float(i)/l*100))
        sys.stdout.flush()
    pmfsum += x
    i += 1

print

e = 0.0
i = 0
l = len(pmf)
for x in pmf.values():
    if i % 10000 == 0:
        sys.stdout.write("\rCalculating entropy... %.2f%%" % (float(i)/l*100))
        sys.stdout.flush()
    e += x/pmfsum * numpy.log2(pmfsum/x)
    i += 1

print

print "Estimated entropy of raw audio: %f bits" % e

#plt.plot(_pmf.keys(), _pmf.values())
#plt.show()
