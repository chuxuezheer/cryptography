#!/usr/bin/python

'''Decipher the cipher text encoded by MTP(many time pad).

The scripts takes 11 input strings, all encoded by the same
cipher key. The last one is the target text which we can to
transfer into plain text.
'''

__author__ = "Jin Zhang(zj@utexas.edu)"
__version__ = "$Version: 1.0 $"
__date__ = "$Date: 2014/07/04 13:35:15"
__copyright__ = "Copyright: (c) 2014 Jin Zhang"
__license__ = "Python"

from itertools import permutations

def strxor(a,b):
	if len(a) > len(b):
		return "".join([chr(ord(x) ^ ord(y)) for (x,y) in zip(a[:len(b)],b)])
	else:
		return "".join([chr(ord(x) ^ ord(y)) for (x,y) in zip(a,b[:len(a)])])

if __name__ == "__main__":

		# read in the text
		text = []
		with open ("hw1_text") as f:
			for line in f:
				#convert cipher text in ascii format, which can be used in xor correctly#
				text.append(line[:-1].decode('hex'))


		key=[0]*83

		xortext = [strxor(x,y) for (x,y) in permutations(text,2)]

		print len(xortext)

		# the idea is: if a given text place is space, then it xor with character will
		# convert low/upper letter to upper/low letter. So we can use an abitrary count
		# of frequency of letters in given positions to infer the probability of space in
		# the plain text, and using the cipher text to infer back the key.
		for i in range(10):
			for j in range(83):
				count = sum([1 for k in range(10) if xortext[i*10+k][j].isalpha()])
				if count > 5:
					key[j] = chr(ord(text[i][j]) ^ ord(' '))


		print key
		strkey = ''.join(str(e) for e in key)
		output =  [e for e in strxor(text[-1],strkey)]
		print output

		for j in range(83):
			count = 0
			count = sum([1 for k in range(10) if xortext[90+k][j].isalpha()])
			if count > 5 and not key[j]:
				output[j] = ' ';

		print ''.join(output)
