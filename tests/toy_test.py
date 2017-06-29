import unittest
import sys
sys.path.append('../lib')

from toy import *

class tdd_example( unittest.TestCase ):
	def test_add( self ):
		calc = Calculator()
		result = calc.add(2,2)
		self.assertEqual(4,result)

if __name__ == '__main__':
	unittest.main();
