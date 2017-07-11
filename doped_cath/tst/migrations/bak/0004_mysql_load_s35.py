
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


# def load_classes_sql():
#     from coffeehouse.settings import PROJECT_DIR
#     import os
#     sql_statements = open(os.path.join(PROJECT_DIR,'tst/sql/load_classes.sql'), 'r').read()
#     return sql_statements
load_classes_sql='''

## Reset the table
DROP TABLE IF EXISTS s35;
CREATE table s35(
   id int AUTO_INCREMENT PRIMARY KEY,
   domain_id char(10),
   Class int, ## Note Capital "C" is used to avoid clash with python "class()" keyword
   arch int,
   topo int,
   homsf int,
   s35  int,
   s60  int,
   s95  int,
   s100 int,
   s100_seqcnt int,
   domain_length int,
   resolution float);

#### If however you got fixed-width CATH CLF.
LOAD DATA LOCAL INFILE '/home/shouldsee/Documents/repos/cathdb/cath-domain-list-S35-v4_1_0.txt' 
INTO TABLE s35
(@row)
SET  domain_id = TRIM(SUBSTR(@row,1,7)),
    Class = TRIM(SUBSTR(@row,8,13)),
    arch  = TRIM(SUBSTR(@row,14,19)),
    topo  = TRIM(SUBSTR(@row,20,25)),
    homsf = TRIM(SUBSTR(@row,26,31)),
    s35   = TRIM(SUBSTR(@row,32,37)),
    s60   = TRIM(SUBSTR(@row,38,43)),
    s95   = TRIM(SUBSTR(@row,44,49)),
    s100  = TRIM(SUBSTR(@row,50,55)),
    s100_seqcnt= TRIM(SUBSTR(@row,56,61)),
    domain_length=TRIM(SUBSTR(@row,62,67)),
    resolution=TRIM(SUBSTR(@row,68,73));

# SELECT domain_id,Class,arch,topo,homsf,s35 from s35 limit 5;


UPDATE tst_classification
  SET temp_id=NULL;


DROP TABLE IF EXISTS homsf;
CREATE TABLE homsf
SELECT DISTINCT a.Class, a.arch, a.topo, a.homsf FROM s35 AS a;
ALTER TABLE homsf 
  ADD COLUMN id INT AUTO_INCREMENT PRIMARY KEY,
  ADD COLUMN s35 INT DEFAULT 1,
  ADD COLUMN s60 INT DEFAULT 1,
  ADD COLUMN s95 INT DEFAULT 1,
  ADD COLUMN s100 INT DEFAULT 1;


DROP TABLE IF EXISTS temp;
CREATE TABLE temp
  SELECT 
    a.id AS id,
    c.id AS classification_id,
    c.level_id FROM homsf AS a
  LEFT JOIN 
    (SELECT * FROM tst_classification WHERE level_id=5) AS c
  ON (a.Class, a.arch, a.topo, a.homsf, a.s35, a.s60, a.s95, a.s100)=(c.Class, c.arch, c.topo, c.homsf, c.s35, c.s60, c.s95, c.s100);

DROP TABLE IF EXISTS temp_null
DROP TABLE IF EXISTS temp_notnull;
CREATE TABLE temp_null SELECT * FROM temp where classification_id IS NULL;
CREATE TABLE temp_notnull SELECT * FROM temp where classification_id IS NOT NULL;

ALTER TABLE homsf ADD COLUMN level_id INT DEFAULT 5;
ALTER TABLE homsf ADD COLUMN version_id INT DEFAULT 1;

INSERT INTO tst_classification 
 (Class,arch,topo,homsf,s35,s60,s95,s100,version_id,level_id,temp_id)
SELECT
  Class,arch,topo,homsf,s35,s60,s95,s100,version_id,level_id, id FROM homsf
  WHERE homsf.id IN 
    (SELECT id FROM temp_null);

UPDATE tst_classification AS c
   JOIN temp_notnull as t 
   ON c.id=t.classification_id
   SET c.temp_id=t.id;




DROP TABLE IF EXISTS temp;
CREATE TABLE temp
  SELECT 
    a.id AS id,
    c.id AS classification_id,
    c.level_id FROM s35 AS a
  LEFT JOIN 
    (SELECT * FROM tst_classification WHERE level_id=6) AS c
  ON (a.Class, a.arch, a.topo, a.homsf, a.s35, a.s60, a.s95, a.s100)=(c.Class, c.arch, c.topo, c.homsf, c.s35, c.s60, c.s95, c.s100);

DROP TABLE IF EXISTS temp_null
DROP TABLE IF EXISTS temp_notnull;
CREATE TABLE temp_null SELECT * FROM temp where classification_id IS NULL;
CREATE TABLE temp_notnull SELECT * FROM temp where classification_id IS NOT NULL;

ALTER TABLE s35 ADD COLUMN level_id INT DEFAULT 6;
ALTER TABLE s35 ADD COLUMN version_id INT DEFAULT 1;

ALTER TABLE tst_classification  ADD COLUMN temp_id INT DEFAULT NULL;

INSERT INTO DJANGO_CATH.tst_classification 
 (Class,arch,topo,homsf,s35,s60,s95,s100,version_id,level_id,temp_id)
SELECT
 Class,arch,topo,homsf,s35,s60,s95,s100,version_id,level_id, id 
 FROM (SELECT * FROM s35 
   WHERE id IN (SELECT id FROM temp WHERE classification_id IS NULL)
   );

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
SELECT
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
