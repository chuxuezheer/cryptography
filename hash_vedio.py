#!/usr/bin/python

'''Implement a hash function for verifying data integrity.

'''

__author__ = "Jin Zhang(zj@utexas.edu)"
__version__ = "$Version: 1.0 $"
__date__ = "$Date: 2014/07/20 00:29:15"
__copyright__ = "Copyright: (c) 2014 Jin Zhang"
__license__ = "Python"

from Crypto.Hash import SHA256
import os

def generate_hash(fn):
	'''Return hash h0 for given file'''
	
	filedata = ''
	with open(fn,'r') as f:
		filedata = f.read()
	
	# split data into 1KB, or 2K-hex-chactacters blocks
	blocks = [filedata[i:i+1024] for i in range(0,len(filedata),1024)]

	# iteratively hash each block from the end to the start
	hash = ''
	for block in blocks[::-1]:
		h = SHA256.new(block+hash)
		hash = h.digest()

	return hash.encode('hex')

if __name__ == "__main__":
	print "generate hashs for verifying data integrity."

	# for the purpose of assignment 3
	filename = '6 - 1 - Introduction (11 min).mp4'
	print "the hash h0 for sample file is: "
	print generate_hash(filename)
