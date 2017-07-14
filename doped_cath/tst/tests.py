# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from .models import *
from datetime import datetime
from django.db import connection


def lookup(node,db_version):
	lst = (int(x) for x in node.split('.'))
	c = classification.objects.get(
		Class=next(lst,0),
		arch=next(lst,0),
		topo=next(lst,0),
		homsf=next(lst,0),
		s35=next(lst,0),
		s60=next(lst,0),
		s95=next(lst,0),
		s100=next(lst,0),
		version__name=db_version
		)
	return c 

# Create your tests here.
class EntryModelTest(TestCase):

	fixtures = ['c410_s35_fixed.json']
	
	def sest_superfamily(self):
		# 1.10.3460.10	
		node = '1.10.3460.10'
		lst = (int(x) for x in node.split('.'))
		c = classification.objects.get(
			Class=next(lst,None),
			arch=next(lst,None),
			topo=next(lst,None),
			homsf=next(lst,None),
			s35=next(lst,None),
			s60=next(lst,None),
			s95=next(lst,None),
			s100=next(lst,None)
			)
		l = len( c.domain_set.all() )
		assert l > 1, 'Node %s does not associate to multiple (>1) domains '

	def st_classification(self):
		# self.fail("TODO Test incomplete")
		# for i in range(2):
		c = classification(
			Class=1,
			arch=10,
			topo=10,
			homsf=10,
			s35=283)
		c.save()
		# c.refresh_from_db()

		q = classification.objects.raw('select * from tst_classification;')
		print(q[0])
		qus = Question(question_text='tstqus',pub_date=datetime.now())
		qus.save()
		# q = Question.objects.raw('select * from tst_question')
		# print(q.values())

		from django.db import connection

		with connection.cursor() as c:
				c.execute("show columns from tst_classification")
				print(c.fetchone())

				c.execute("select * from tst_classification")
				row = c.fetchone()
				print(row)

	def test_relationship(self):
		# 1.10.3460.10	
		node = '1.10.10.10'
		correct_cnt = 407
		db_version = 'v4_1_0'
# 
		sf = lookup('1.10.10.10','v4_1_0')

		real_cnt = len( sf.classification_set.all() )
		assert real_cnt == correct_cnt, 'Node %s does not the correct number of children nodes (Tested %d, should be %d)' % (	
			  node, real_cnt, correct_cnt) 

		
		# print(classification.objects.all())

		# c = classification(
		# 	Class=2,
		# 	arch=10,
		# 	topo=10,
		# 	homsf=10,
		# 	s35=283)
		# c.save()
		pass
	def test_homepage(self):
		response = self.client.get('/')
		# print('HTTP %d')
		assert response.status_code < 400, 'Index page not working, HTTP %d'%response.status_code
	def test_domain_template(self):
		response = self.client.get('/tst/domain/?a=100')
		request = response.wsgi_request
		print(request)
		assert response.status_code < 400, 'Default domain collection PAGE not reachable, HTTP %d'%response.status_code
	# Class = models.IntegerField(default=None)
	# arch = models.IntegerField(default=None)
	# topo = models.IntegerField(default=None)
	# homsf = models.IntegerField(default=None)
	# s35 = models.IntegerField(default=None)
	# s60 = models.IntegerField(default=None)
	# s95 = models.IntegerField(default=None)
	# s100 = models.IntegerField(default=None)
	# level = models.ForeignKey(level, default=None, on_delete=models.CASCADE)
	# version =  models.ForeignKey(version, default=None,on_delete= models.CASCADE);