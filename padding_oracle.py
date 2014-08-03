#!/usr/bin/python

'''Implement padding oracle attack against given server.

'''

__author__ = "Jin Zhang(zj@utexas.edu)"
__version__ = "$Version: 1.0 $"
__date__ = "$Date: 2014/07/26 16:39"
__copyright__ = "Copyright: (c) 2014 Jin Zhang"
__license__ = "Python"

import urllib2
from math import ceil

#-----------------------------------
#padding oracle
#-----------------------------------
class PaddingOracle(object):
	def __init__(self, t):
		self.Target = t

	# The query function is got from sample code
	def query(self, q):
		target = self.Target + urllib2.quote(q)	# Create query URL
		req = urllib2.Request(target)			# Send HTTP request to server
		try:
			f = urllib2.urlopen(req)
		except urllib2.HTTPError, e:
			#print "We got: %d" % e.code
			if e.code == 404:
				return True # good padding
			return False


def po_attack(po, cipher_text):
	'''Implement padding oracle attack with given cipher text'''

	# try all ASCII character based on their frequency of usage
	# the frequency table is from Binesh Bannerjee
	ordered = [
     32, 101, 116,  97, 111, 110, 105, 115, 114, 104, 108, 100, 117,  99, 121, 109, 
    119, 103, 102, 112,  46,  98,  10, 118, 107,  44,  13,  73,  39,  45,  84,  83, 
     65,  47,  67,  77,  87,  49,  66, 120,  34,  50,  48,  41,  80, 106,  72,  40, 
     33,  79,  68,  76,  58,  78,  63,  82,  70,  69,  71, 122,  89,  51, 113,  38, 
     56,  59,  53,  86,  52,  74,  62,  35,  55,  85,  75,  60,  54,  95,  57,  36, 
     61,  90,  37,  42,  81,  88,  43,  91,  93,  64,   9, 126,  96,  94, 125, 123, 
    124,  92,  16,   1,  20,   0,  11,  12, 127, 128, 129, 130, 131, 132, 133, 134, 
    135, 136, 137, 138, 139, 140, 141,  14, 142, 143, 144, 145, 146, 147, 148, 149, 
    150, 151,  15, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 
    165, 166, 167, 168, 169, 170, 171,  17, 172, 173, 174, 175, 176, 177, 178, 179, 
    180, 181,  18, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191,  19, 192, 193, 
    194, 195, 196, 197, 198, 199, 200, 201, 202, 203, 204, 205, 206, 207, 208, 209, 
    210, 211,  21, 212, 213, 214, 215, 216, 217, 218, 219,   2, 220, 221,  22, 222, 
    223, 224, 225, 226, 227, 228, 229, 230, 231,  23, 232, 233, 234, 235, 236, 237, 
    238, 239, 240, 241,  24, 242, 243, 244, 245, 246, 247, 248, 249, 250, 251,  25, 
    252, 253, 254, 255,  26,  27,  28,  29,  30,  31,   3,   4,   5,   6,   7,   8
	]	


	pt =  [0]* (len(cipher_text)/2 + 1)


	# current position for guessing (in bytes) in the cipher text 
	# skip the first block since it's the IV
	for pos in  range(len(cipher_text)/2, 16, -1):
		curblock = int(ceil(pos*1.0/16))
		preblock = curblock - 1
		padding = len(cipher_text)/2 - pos + 1

		# cipher text affecting current guessing position
		cur_ct = cipher_text[pos*2 - 34: pos*2 - 32]
		# all cipher text prior to it doesn't need to change
		prefix = cipher_text[:pos*2 - 34]

		appending = ''
		# all cipher text after that need to xor with 
		for i in range(1,padding):
			letter = hex(int(cipher_text[(pos+i)*2-34: (pos+i)*2-32],16) ^ pt[pos+i] ^ padding)[2:]
			if len(letter) == 1:
				letter = '0' + letter
			appending += letter

		postfix = cipher_text[curblock*32-32:]

		for real in ordered:
			guess = hex(real ^ padding ^ int(cur_ct,16))[2:] 
			if len(guess) == 1:
				guess = '0'+guess


			# if return 404 error, it's the correct guess
			if po.query(prefix + guess + appending + postfix):
				pt[pos]  = real
				break

	return "".join([chr(pt[i]) for i in range(17,len(cipher_text)/2+1)])

if __name__ == "__main__":
	Target = 'http://crypto-class.appspot.com/po?er='
	po = PaddingOracle(Target)

	with open("hw3_text") as f:
		filedata = f.read()
		ct = filedata.split("=")[1].strip()

	
	print ">"+po_attack(po,ct[0:64])+"<"
	print ">"+po_attack(po,ct[32:96])+"<"
	print ">"+po_attack(po,ct[64:128])+"<"



