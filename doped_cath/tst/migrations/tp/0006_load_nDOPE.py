
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


# def load_classes_sql():
#     from coffeehouse.settings import PROJECT_DIR
#     import os
#     sql_statements = open(os.path.join(PROJECT_DIR,'tst/sql/load_classes.sql'), 'r').read()
#     return sql_statements


'''
INSERT INTO DJANGO_CATH.tst_classification (id,Class,arch,topo,homsf,s35,s60,s95,s100,version_id,level_id)
 select * from CATH.temp_class;
'''

def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

def load_nDOPE(apps, schema_editor):
    import sys
    # classification = apps.get_model("tst", "classification")
    domain = apps.get_model("tst", "domain")
    import os
    cwd = os.getcwd()
    print >>sys.stdout, '\n\n\n %s'%cwd
    dope_file=('tst/migrations/bak/nDOPE-s35-v410.csv');
    import csv

    cnt = 0;
    cmax = file_len(dope_file);

    with open(dope_file,'r') as f:
    	c = csv.reader(f);
    	for row in c:
    		dom = domain.objects.get(domain_id=row[0])
    		dom.nDOPE = float(row[1]);
    		dom.save()

    		cnt += 1
    		if not cnt%100:
    			print >>sys.stdout, '%d of %d lines loaded'%(cnt,cmax);
    	# f.readlines() 
    # for d in domain.objects.

def do_nothing(apps, schema_editor):
	pass

class Migration(migrations.Migration):

    dependencies = [
        ('tst', '0005_make_parents'),
    ]

    operations = [
        migrations.RunPython(load_nDOPE,do_nothing),
    ]
