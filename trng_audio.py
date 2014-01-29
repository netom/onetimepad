#!/usr/bin/env python
# -*- coding: utf8 -*-

RATE = 44100
#
# 64*16bit = 1024 bit. Estimated entropy density is
# 60%, that means 614 bit entropy per buffer.
# SHA512 emits 512 bits, therefore we have 102 bits
# or about 20% more entropy in, than out. 10% more
# is already plenty.
BUF = 64

import sys
import pyaudio
import numpy
import hashlib

p = pyaudio.PyAudio()

stream = p.open(
	format = pyaudio.paInt16,
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
        sys.stdout.write(s.tostring())

