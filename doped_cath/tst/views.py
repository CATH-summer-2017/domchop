# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.


from django.http import HttpResponse


from .models import *

def index(request):
	latest_question_list = Question.objects.order_by('-pub_date')[:5]
	output = ',</br> '.join([q.question_text for q in latest_question_list])
	# return HttpResponse("Hello, world. You're at the polls index.")
	return HttpResponse( '<!DOCTYPE HTML><html>' + ' The output is: <br/>'+ output+'</html>')


def detail(request, question_id):
    return HttpResponse("You're looking at question %s." % question_id)

def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)

def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)


####
def domain_detail(request, domain_id):
    return HttpResponse("You're viewing detail page on CATH domian %s." % domain_id)

def domain_collection(request):
    return HttpResponse("You're viewing the whole collection of CATH domains" )

def homsf_s35_collection(request, homsf_id):
    return HttpResponse("You're viewing the s35 representative structures of homology family %s" % homsf_id)
