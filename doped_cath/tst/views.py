# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.


from django.http import HttpResponse
from django.template import loader


from django.db.models import Avg,Count,Q
from .models import *

from CATH_API.lib import *
import urllib
import re
import random

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

def view3d(request):
	did = "2c7wA00";
	did = "1fzpD00";
	context={ "d" :domain.objects.get(domain_id=did)};
	return render(request,
			 'tst/3dviewer.html',
			  context)

def view_domain_list(request, query_set, orders = None, cols = None):

	sf_list = CATH_superfamily('v4_1_0')[1]

	if query_set.model == domain:
		query_set = query_set.annotate(sf_s35cnt=Count('classification__parent__classification'))	
		orders = orders or ['-sf_s35cnt','-nDOPE'];
		query_set = query_set.order_by(*orders)
		cols=cols or ['domain_id_urled','superfamily_urled','view_chopped','sf_s35cnt','domain_length','nDOPE'];

	if query_set.model == classification:
		# query_set = query_set.annotate(sf_s35cnt=Count('classification__parent__classification'))	
		# orders = orders or ['-s35_count','-nDOPE_avg'];
		query_set = query_set.order_by(*orders)
		# cols=cols or ['superfamily','s35_count','rep_s35','domain_length','nDOPE'];

		cols=cols or ['superfamily_urled','s35_count','nDOPE_avg','nDOPE_std'];


	context = {
		'query_set':query_set,
		'tst_a':0,	
		's35cnts':[],
		'field_names':cols}
	return render(request,
				 # 'tst/index.html',
				 'tst/view_table.html',
				  context)

def domain_collection(request):
	# latest_question_list = Question.objects.order_by('-pub_date')[:5]
	dquery = request.GET.get('dquery', [])

	if dquery:
		dquery = re.sub('[^A-Za-z0-9\_]+', '', dquery).split('_');
		# domain_list = domain.objects.filter(domain_id__in=dquery)
		domain_list = domain.objects.none();
		for q in dquery:
			if q:
				domain_list = domain_list | domain.objects.filter(domain_id__startswith=q[:4]); 
	else:
		domain_list = domain.objects.filter(nDOPE__gte=1.5);

	orders = ['-sf_s35cnt','-nDOPE']

	# domain_list = 

	# request.GET
	# tst_a = dquery
	'tst/domain/?dquery=1gjjA00&dquery=4567Cud'

	return view_domain_list(request,domain_list,orders)


def homsf_s35_collection(request, homsf_id = None):
	if not homsf_id:
		### filter for the superfamily/ index page
		# homsf_list = (classification.homsf_objects.filter(nDOPE_avg__gte=1.0 ) | 
		# 	classification.homsf_objects.filter(nDOPE_std__gte = 0.1 ))
		homsf_list = classification.homsf_objects.filter(s35_count__gte=1000)

		return view_domain_list(request,homsf_list,
				orders = ['-nDOPE_avg'],
				cols = ['superfamily_urled','s35_count','nDOPE_avg','nDOPE_std'])
	else:
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
		# cols = ['domain_id','superfamily_urled','sf_s35cnt','domain_length','nDOPE'];
		cols = [];
		return view_domain_list(request,domain_list,cols=cols)
    
    # return HttpResponse("You're viewing the s35 representative structures of homology family %s" % homsf_id)
