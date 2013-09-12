#!/usr/bin/env python
# -*- coding: utf8 -*-

RATE = 44100
#
# 32*32bit = 1024 bit. Estimated entropy density is
# 60%, that means 614 bit entropy per buffer.
# SHA512 emits 512 bits, therefore we have 102 bits
# or about 20% more entropy in, than out. 10% more
# is already plenty.
BUF = 32

import pyaudio
import numpy
import hashlib

_pmf = numpy.array([0.000001]*(1<<16), dtype=numpy.float64)
_pmfhash = numpy.array([0.000001]*(1<<16), dtype=numpy.float64)

def pmf(values, a):
  for v in values:
	  a[v] += 1

p = pyaudio.PyAudio()

stream = p.open(
	format = pyaudio.paInt32,
	channels = 1,
	rate = RATE,
	input = True,
	output = False,
	frames_per_buffer = BUF
)

f = open('random_data.random', 'a')

i = 0
h = hashlib.new('sha512')
while True:
	i += 1
	s = stream.read(BUF)

	h.update(s)
	s2 = h.digest()

	# Overflow is very-very unlikely, so we ignore it for now.
	pmf(numpy.fromstring(s, dtype=numpy.uint16), _pmf)
	s = numpy.fromstring(s2, dtype=numpy.uint16)
	pmf(s, _pmfhash)
	f.write(s)

	if i % 1000 == 0:
		x  = _pmf / _pmf.sum()
		xh = _pmfhash / _pmfhash.sum()

		print "Input entropy: ", (x*numpy.log2(1/x)).sum()
		print "Output entropy: ", (xh*numpy.log2(1/xh)).sum()

f.close()
