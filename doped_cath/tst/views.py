# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.


from django.http import HttpResponse
from django.template import loader

from .models import *

from CATH_API.lib import *
import urllib
import re

def index(request):

	output = 'index is now empty'
	return HttpResponse(output)


	# output = ',</br> '.join([q.question_text for q in latest_question_list])
	# return HttpResponse("Hello, world. You're at the polls index.")
	# return HttpResponse( '<!DOCTYPE HTML><html>' + ' The output is: <br/>'+ output+'</html>')


def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)
####
def domain_detail(request, domain_id):
    return HttpResponse("You're viewing detail page on CATH domian %s." % domain_id)

def view_domain_list(request, domain_list):

	template = loader.get_template('tst/index.html')
	# for 
	sf_list = CATH_superfamily('v4_1_0')[1]

	for q in domain_list:
		q.s35cnt = 'not found'
		q_sf =  q.superfamily();
		for sf in sf_list:
			if 	sf['cath_id'] == q_sf:
				q.s35cnt = sf['child_count_s35_code'];
				break
	# domain_list = domain_list.all().order_by('-nDOPE','-s35cnt')
	context = {'domain_list':domain_list,'tst_a':0,
				}
	return render(request,
				 'tst/index.html',
				  context)

def domain_collection(request):
	# latest_question_list = Question.objects.order_by('-pub_date')[:5]
	dquery = request.GET.get('dquery', [])

	# dquery = ['1000','1tf6D01']
	if dquery:
		dquery = re.sub('[^A-Za-z0-9\,]+', '', dquery).split(',');
		domain_list = domain.objects.filter(domain_id__in=dquery)
		# domain_list = domain_list.order_by('classification__Class','-nDOPE')

	else:
		# domain_list
		domain_list = domain.objects.filter(nDOPE__gte=1.5);

		# s35cnt_lst=[]
		sf_list = CATH_superfamily('v4_1_0')[1]

		s = domain_list.all()
		for q in s:
				q.s35cnt = 'not found'
				q_sf =  q.superfamily();
				for sf in sf_list:
					if 	sf['cath_id'] == q_sf:
						q.s35cnt = sf['child_count_s35_code'];
						# s35cnt_lst.append(sf['child_count_s35_code']);
						break
		# dope_lst = domain_list.values_list('nDOPE');
		# s = domain_list.all()
		s = sorted(s, key = lambda x: (-int(x.s35cnt), - x.nDOPE))
		domain_list = s;
		# domain_list = domain_list.all().order_by('-s35cnt','-nDOPE',)
		# domain_list = domain.objects.filter(resolution__lte=1.0);

	# domain_list = 

	# request.GET
	# tst_a = dquery
	'tst/domain/?dquery=1gjjA00&dquery=4567Cud'

	return view_domain_list(request,domain_list)


def homsf_s35_collection(request, homsf_id):
	lst = (int(x) for x in homsf_id.split('.'))
	homsf = classification.objects.filter(Class=next(lst,None),
								arch=next(lst,None),
								topo=next(lst,None),
								homsf=next(lst,None),
								s35=next(lst,0),
								# s35=None
								)[0]

	domain_list = domain.objects.filter(classification__in=homsf.classification_set.all())
	domain_list = domain_list.order_by('-nDOPE')
	return view_domain_list(request,domain_list)
    
    # return HttpResponse("You're viewing the s35 representative structures of homology family %s" % homsf_id)
