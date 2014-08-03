#!/usr/bin/python

'''Implement the cipher/decipher sytems using AES in either
CBC or CTR mode.
	
	In CTR mode, the IV (initialization vector) is incremented
one each time.
'''

__author__ = "Jin Zhang(zj@utexas.edu)"
__version__ = "$Version: 1.0 $"
__date__ = "$Date: 2014/07/14 00:12:15"
__copyright__ = "Copyright: (c) 2014 Jin Zhang"
__license__ = "Python"

from Crypto.Cipher import AES
from Crypto.Util import Counter
from textwrap import wrap
import os

def AESencryptCBC(iv,key,message):
	'''Encrypting text using AES in CBC mode.'''
	idx = 0
	encrypt_message = iv
	cipher = AES.new(key, AES.MODE_CBC, iv)
	while(idx + AES.block_size <= len(message)):
		pt = message[idx:idx+AES.block_size]
		ct = cipher.encrypt(pt)
		encrypt_message += ct
		idx += AES.block_size

	gap = idx + AES.block_size - len(message) 
	pt = message[idx:]+chr(gap)*gap
	ct = cipher.encrypt(pt)
	encrypt_message += ct

	return encrypt_message.encode('hex')

def AESdecryptCBC(key,ciphertext):
	'''Decrypting text using AES in CBC mode.'''
	iv = ciphertext[0:AES.block_size]
	idx = AES.block_size
	message = ''
	cipher= AES.new(key, AES.MODE_CBC, iv)
	while (idx + AES.block_size <= len(ciphertext)):
		ct = ciphertext[idx:idx+AES.block_size]
		pt = cipher.decrypt(ct)
		message += pt
		idx += AES.block_size

	# get the padding number
	#padding = ord(message[-1])*-1

	return message

def AESencryptCTR(iv,key,message):
	'''Encrypting text using AES in CTR mode.'''
	encrypt_message = iv
	idx = 0
	ctr = Counter.new(128,initial_value=int(iv.encode('hex'),16))
	cipher = AES.new(key, AES.MODE_CTR, counter=ctr)
	while(idx + AES.block_size <= len(message)):

		pt = message[idx:idx+AES.block_size]
		ct = cipher.encrypt(pt)
		encrypt_message += ct
		idx += AES.block_size

	if (idx != len(message)):
		pt = message[idx:]
		ct = cipher.encrypt(pt)
		encrypt_message += ct

	return encrypt_message.encode('hex')

# decrypt using AES in CTR mode
def AESdecryptCTR(key,ciphertext):
	'''Decrypting text using AES in CTR mode.'''
	iv = ciphertext[0:AES.block_size]
	idx = AES.block_size
	message = ''
	ctr = Counter.new(128,initial_value=int(iv.encode('hex'),16))
	cipher= AES.new(key, AES.MODE_CTR, counter=ctr)
	while (idx + AES.block_size <= len(ciphertext)):

		ct = ciphertext[idx:idx+AES.block_size]
		pt = cipher.decrypt(ct)
		message += pt
		idx += AES.block_size

	if (idx != len(ciphertext)):
		ct = ciphertext[idx:]
		pt = cipher.decrypt(ct)
		message += pt

	return message


if __name__ == "__main__":

	print 'Implement encrypting/decrypting system using AES in CBC/CTR mode.'
	

	input='A block cipher by itself is only suitable for the secure cryptographic transformation\
 (encryption or decryption) of one fixed-length group of bits called a block'
	
	key = os.urandom(AES.block_size)
	iv = os.urandom(AES.block_size)

	print "="*70
	print "The testing input is: "
	for e in wrap(input):
		print e
	print "The cipher key is: ",
	print key.encode('hex')
	print "The IV is: ",
	print iv.encode('hex')
	print "="*70

	print "In CBC mode:"
	print "The encrypt text is:"
	ct = AESencryptCBC(iv,key, input)
	for e in wrap(ct,width=32):
		print e
	print "The decrypt text is:"
	for e in wrap(AESdecryptCBC(key,ct.decode('hex'))):
		print e
	print "="*70

	print "In CTR mode:"
	print "The encrypt text is:"
	ct = AESencryptCTR(iv,key, input)
	for e in wrap(ct,width=32):
		print e
	print "The decrypt text is:"
	for e in wrap(AESdecryptCTR(key,ct.decode('hex'))):
		print e
	print "="*70


	cbc = []
	ctr = []	
	with open ("hw2_text") as f:
		for line in f:
			data = line[:-1].split()
			if data[0] == 'CBC:':
				cbc.append(data[1].decode('hex'))
			else:
				ctr.append(data[1].decode('hex'))
	
	print AESdecryptCBC(cbc[0],cbc[1])
	print AESdecryptCBC(cbc[2],cbc[3])
	print AESdecryptCTR(ctr[0],ctr[1])
	print AESdecryptCTR(ctr[2],ctr[3])
