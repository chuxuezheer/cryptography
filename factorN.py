#!/usr/bin/python

'''Factoring the public modulus N of RSA when it's generated incorrectly.
        Input parameter:
        modulus N
        Out parameter:
        prime p,q such that N = p*q
'''

__author__ = "Jin Zhang(zj@utexas.edu)"
__version__ = "$Version: 1.0 $"
__date__ = "$Date: 2014/08/03 09:12"
__copyright__ = "Copyright: (c) 2014 Jin Zhang"
__license__ = "Python"

import gmpy2
import timeit
from gmpy2 import mpz

def factor(A,N):
	'''Factor big number N, which is product of prime p/q'''
	'''Input: 
		N: big number, 
		A: proposed average of prime p,q
	   Output: 
		prime p,q such that N = p*q and p<q
		or 0 if A is not correct'''
	
	if A*A < N:
		return 0
	x = gmpy2.isqrt(A*A - N)
	p = A-x
	q = A+x

	if gmpy2.is_prime(p) and gmpy2.is_prime(q) and p*q == N:
		return p,q
	else:
		return 0

def factor_N1(N):
	'''Factor genrated N,
which is a product of two relatively close primes p/q such that,
|p-q| < 2*N^(1/4)'''
	
	N = mpz(N)	
	A = gmpy2.isqrt(N)
	if A*A != N:
		A += 1
	
	return factor(A,N)

def factor_N2(N):
	'''Factor in correctly genrated N,
which is a product of two relatively close primes p/q such that,
|p-q| < 2^11*N^(1/4)'''
	
	N = mpz(N)	
	sqrtN = gmpy2.isqrt(N)
	A = sqrtN
	for delta in range(0,2**20):
		A = sqrtN + delta
		if A*A < N:
			continue
		if gmpy2.iroot(A**2-N,2)[1]:	# A^2-N is a perfect square
			return factor(A,N)
	return 0

def factor_N3(N):
	'''Factor in correctly genrated N,
which is a product of two relatively close primes p/q such that,
|3p-2q| < N^(1/4)'''

	N = mpz(N)	
	M = 2*gmpy2.isqrt(6*N)+1	# M = (3p+2q)
	# M = (3p+2q)
	# x = (3p-2q)
	x = gmpy2.isqrt(M*M - 24*N)	# X = (3p-2q)

	# since p,q is not symmetric around M/2, we need to consider two cases
	p1 = (M+x)/6
	q1 = (M-x)/4
			
	p2 = (M-x)/6
	q2 = (M+x)/4

	if gmpy2.is_prime(p1) and gmpy2.is_prime(q1) and p1*q1 == N:
		if p1<q1:
			return p1,q1
		else:
			return q1,p1

	if gmpy2.is_prime(p2) and gmpy2.is_prime(q2) and p2*q2 == N:
		if p2<q2:
			return p2,q2
		else:
			return q2,p2
	return 0

def break_RSA(N,ct):
	e = 65537
	p,q = factor_N1(N)
	phi_N = (p-1)*(q-1)
	pt = ''

	# d is relative prime to e in phi_N
	d = gmpy2.invert(e,phi_N)
	pkcs = hex(gmpy2.powmod(mpz(ct),d,mpz(N)))
	pt = pkcs.split('00')[1]
	return pt.decode('hex')

if __name__ == "__main__":
        # run the testing parameter
	N1 = '17976931348623159077293051907890247336179769789423065727343008115\
77326758055056206869853794492129829595855013875371640157101398586\
47833778606925583497541085196591615128057575940752635007475935288\
71082364994994077189561705436114947486504671101510156394068052754\
0071584560878577663743040086340742855278549092581'

	N2 = '6484558428080716696628242653467722787263437207069762630604390703787\
9730861808111646271401527606141756919558732184025452065542490671989\
2428844841839353281972988531310511738648965962582821502504990264452\
1008852816733037111422964210278402893076574586452336833570778346897\
15838646088239640236866252211790085787877'

	N3 = '72006226374735042527956443552558373833808445147399984182665305798191\
63556901883377904234086641876639384851752649940178970835240791356868\
77441155132015188279331812309091996246361896836573643119174094961348\
52463970788523879939683923036467667022162701835329944324119217381272\
9276147530748597302192751375739387929'
	
	# ciphertext encoded using PKCS v1.5 before applying RSA function with modulus N1
	ct = '220964518674103817763065611348834180174100697878928310717318391436761\
35600120538004282329650473509424343946219751512256465839967942889460\
76454204058156474898801373486412045232522932017648791666640299750918\
87299716905260832220677716000193292608700095799937240774589677736978\
17571267229951148662959627934791540'
	
	print factor_N1(N1)
	start = timeit.default_timer()
	print factor_N2(N2)
	t = timeit.default_timer() - start
	print factor_N3(N3)
	print "message: {" + break_RSA(N1,ct) + '}'
