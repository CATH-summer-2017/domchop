
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


# def load_classes_sql():
#     from coffeehouse.settings import PROJECT_DIR
#     import os
#     sql_statements = open(os.path.join(PROJECT_DIR,'tst/sql/load_classes.sql'), 'r').read()
#     return sql_statements
load_classes_sql='''

DROP TABLE if exists temp_class; 
CREATE TABLE temp_class select * from CATH.cath;
ALTER TABLE temp_class
  ADD COLUMN version_id int default 1,
  ADD COLUMN level_id int default 6;

SET FOREIGN_KEY_CHECKS=0;
DELETE from DJANGO_CATH.tst_classification;
SET FOREIGN_KEY_CHECKS=1;

INSERT INTO DJANGO_CATH.tst_classification 
 (Class,arch,topo,homsf,s35,s60,s95,s100,version_id,level_id)
select 
 class,arch,topo,homsf,s35,s60,s95,s100,version_id,level_id from temp_class
 ;
'''

'''
INSERT INTO DJANGO_CATH.tst_classification (id,Class,arch,topo,homsf,s35,s60,s95,s100,version_id,level_id)
 select * from CATH.temp_class;
'''

unload_classes_sql='''
SET FOREIGN_KEY_CHECKS=0;
DELETE from DJANGO_CATH.tst_classification;
SET FOREIGN_KEY_CHECKS=1;
DROP TABLE if exists temp_class; 
DELETE from tst_version;
DELETE from tst_level;
'''
class Migration(migrations.Migration):

    dependencies = [
        ('tst', '0003_init_meta'),
    ]

    operations = [
        migrations.RunSQL(load_classes_sql,unload_classes_sql),
    ]
