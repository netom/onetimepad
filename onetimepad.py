#!/usr/bin/env python
# -*- coding: utf8 -*-

import argparse

parser = argparse.ArgumentParser(description='Encrypt or decrypt messages using one time pad')

parser.add_argument('--encrypt', help='Encrypt a message read from the standard output')

parser.add_argument('--decrypt', help='sum the integers (default: find the max)')

parser.add_argument('-r', dest='accumulate', action='store_const',
                   const=sum, default=max,
                   help='sum the integers (default: find the max)')

parser.add_argument('-a', help='ASCII armor')

parser.add_argument('--random-file', help='Use a specific file')

parser.add_argument('--position', help='Use a specific position in the random file')

args = parser.parse_args()
print(args.accumulate(args.integers))

print "-----BEGIN ONETIMEPAD MESSAGE-----"
print "Version: v0.0.0 (Python)"

print "-----END ONETIMEPAD MESSAGE-----"
