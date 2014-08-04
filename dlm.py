#!/usr/bin/python

'''Calculating the discrete log modulo a prime p using meet in the middle attack.
        Input parameter:
        g,h,p
        Out parameter:
        x such that h = g^x % p, where x \in (1,2^40)
'''

__author__ = "Jin Zhang(zj@utexas.edu)"
__version__ = "$Version: 1.0 $"
__date__ = "$Date: 2014/08/03 09:12"
__copyright__ = "Copyright: (c) 2014 Jin Zhang"
__license__ = "Python"

import gmpy2
import timeit
from gmpy2 import mpz


def dlm_calc(p,g,h):
        '''calculating discrete log modulo'''
        # convert to mpz object, which represents integers with abitrary precisions
        p = mpz(p)
        g = mpz(g)
        h = mpz(h)
        x = 0
	scale = 20
	

	start = timeit.default_timer()
        # building hash table storing the potential tempo values
        print "build hash table"
        lookup_table = {}
	lhs = h % p
	ginv = gmpy2.invert(g,p)
        for x1 in range(0,2**scale):
		if x1:
			lhs = lhs * ginv % p
		
		#print "x1, lhs ", x1, lhs
		#print "numer", numer
                lookup_table[lhs] = x1
        print "done"
	#print lookup_table
	t = timeit.default_timer() - start
	print "time: ", t

        # find x0`
        print "find x0"
	gb = g**(2**scale) % p
	#print "gb: ",gb
	rhs = 1
        for x0 in range(0,2**scale):
		if x0:
			rhs *= gb
			rhs %= p

		#print "x0, rhs: ", x0,rhs
                if rhs in lookup_table:
			print "found"
			print rhs, lookup_table[rhs]
                        x = x0*(2**scale) + lookup_table[rhs]
			break
        print "done"

	t2 = timeit.default_timer() - start - t
	print "time: ", t2

        return x


if __name__ == "__main__":
        # run the testing parameter
        p = '134078079299425970995740249982058461274793658205923933\
77723561443721764030073546976801874298166903427690031\
858186486050853753882811946569946433649006084171'

        g = '11717829880366207009516117596335367088558084999998952205\
59997945906392949973658374667057217647146031292859482967\
5428279466566527115212748467589894601965568'

	h = '323947510405045044356526437872806578864909752095244\
952783479245297198197614329255807385693795855318053\
2878928001494706097394108577585732452307673444020333'

	x = dlm_calc(p,g,h)

	# a simple unit test
	print "x:", x

