
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


# def load_classes_sql():
#     from coffeehouse.settings import PROJECT_DIR
#     import os
#     sql_statements = open(os.path.join(PROJECT_DIR,'tst/sql/load_classes.sql'), 'r').read()
#     return sql_statements


init_meta_sql='''

delete from tst_version;
insert into tst_version ( id, name)
	Values 
	(1, 'v4_1_0'),
	(2, 'current');

delete from tst_level;
insert into tst_level ( letter, name)
	Values 
	('R', 'root'),
	('C', 'Class'),
	('A', 'Architecture'),
	('T', 'Topology'),
	('H', 'Homologous Superfamily'),
	('S', 'Sequence Family (s35)'),
	('O', 'Orthologous Family (S60)'),
	('L', '“Like” domain (S95) '),
	('I', 'Identical domain (S100)'),
	('D', 'Domain counter');

'''
delete_meta_sql='''
DELETE from tst_version;
DELETE from tst_level;
'''

class Migration(migrations.Migration):

    dependencies = [
        ('tst', '0002_make_tables'),
    ]

    operations = [
        migrations.RunSQL(init_meta_sql, delete_meta_sql),
    ]
