from unittest import TestCase,main
# import requests
from lib import * 
class testcase(TestCase):
	def test_http(self):
		# print('\n')
		print('Testing HTTP GET request within CATH_API ' )
		r = fetch_cath('');
		# print()
		try:
			url = r[0][1]
		except:
			url = "No URL is returned from fetch_cath()"
		assert r[0] is not 1, 'HTTP failed in fetch_cath() , or test URL failed at: %s' %( url)
	def test_superfamily_fetch(self):
		v = 'v4_1_0';
		print("Testing superfamily list of version %s" % v)

		r = CATH_superfamily(v)
		assert r[0] is 0, 'Query error: %s, \n URL:%s' % ( r[0][0], r[0][1])
		assert len(r[1]) > 2000, 'Only %i superfamily entries are retrieved. (Required > 2000)' % len(r[1])