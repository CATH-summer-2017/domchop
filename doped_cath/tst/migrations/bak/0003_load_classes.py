
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


# def load_classes_sql():
#     from coffeehouse.settings import PROJECT_DIR
#     import os
#     sql_statements = open(os.path.join(PROJECT_DIR,'tst/sql/load_classes.sql'), 'r').read()
#     return sql_statements
load_classes_sql='''
DELETE from tst_version;
DELETE from tst_level;

INSERT INTO tst_version SELECT * FROM CATH.version;
INSERT INTO tst_level SELECT * FROM CATH.level;

DROP TABLE if exists temp_class; 
CREATE TABLE temp_class select * from CATH.cath;
ALTER TABLE temp_class
  ADD COLUMN version_id int default 1,
  ADD COLUMN level_id int default 5;

DELETE from DJANGO_CATH.tst_classification;
INSERT INTO DJANGO_CATH.tst_classification 
 (Class,arch,topo,homsf,s35,s60,s95,s100,version_id,level_id)
select 
 class,arch,topo,homsf,s35,s60,s95,s100,version_id,level_id from temp_class;
'''
unload_classes_sql='''
DELETE from DJANGO_CATH.tst_classification;
DROP TABLE if exists temp_class; 
DELETE from tst_version;
DELETE from tst_level;
'''
class Migration(migrations.Migration):

    dependencies = [
        ('tst', '0002_make_tables'),
    ]

    operations = [
        migrations.RunSQL(load_classes_sql,unload_classes_sql),
    ]
