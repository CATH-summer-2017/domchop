from django.conf.urls import url,include

from . import views

urlpatterns = [
    # ex: /tst/
    # url(r'^$', views.index, name='index'),

	# ex: /tst/hello    
    url(r'^hello$', views.index, name='hello'),

    # ex: /tst/5/
    # url(r'^(?P<question_id>[0-9]+)/$', 
    # 	views.detail,
    # 	name='detail'),
    
    # # ex: /tst/5/results/
    # url(r'^(?P<question_id>[0-9]+)/results/$',
    # 	views.results,
    # 	name = 'results'),
    
    # # ex:/tst/5/vote/
    # url(r'^(?P<question_id>[0-9]+)/vote/$',
    # 	views.vote,
    # 	name = 'vote'),


    # ex:/tst/
    url(r'^domain/$',
    	views.domain_collection,
    	name = 'domain_collection'),

    # ex:/tst/d1fpzD00/
    url(r'^domain/(?P<domain_id>[\d,a-z,A-Z]+)/$',
    	views.domain_detail,
    	name = 'domain_detail'),

	# ex:/tst/superfamily/3.90.190.10/
	url(r'^superfamily/(?P<homsf_id>[\d,\.]+)/$',
		views.homsf_s35_collection,
		name = 'homsf_s35_collection'),
]
