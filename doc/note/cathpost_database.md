[markdown]

[#### 1. How to fail your deadline? - Starting learning MySQL thinking you can master it in one day!]

Recently, I touched upon MySQL because I wanted it to be the backend for my incoming Django-based data browser. After 4 days of prolonged fiddling I finally manage to make some notes of its functionality. It is very fast, but equally importantly, very different from Python! The other lesson is that one should allocate enough time for learning when starting a new language (depending on [single linkage distance](https://en.wikipedia.org/wiki/Single-linkage_clustering))

Today's blog will go through:
1. Loading a table into MySQL, be it fixed-width or regularly delimited.
2. Create relations between entries.
3. How to deal with errors, and fix your relationship:

<!--more-->
#### Overview:
MySQL is a SQL(standard query language), that is specialised for:
1. database management: To create and maintain the structure of a database  
2. Data I/O: Retrieval and deposition of data.

These functions all look good, so I went on firing a "`mysql`" shell to try out all different commands it provides, including `SELECT`, `SHOW`, `DROP`, `LOAD DATA`. 

#### 1. Loading a table into MySQL.

The original goal was to load a fixed-width flatfile into MySQL to form the original dataset. I used regex to transform the flatfile into a delimited form and load it with the command:


```mysql
## Engage a database before doing anything
CREATE DATABASE IF NOT EXISTS TEST;
USE TEST;

## Reset the table
DROP TABLE IF EXISTS s35;
CREATE table s35(
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


#### For a regularly delimited file.
LOAD DATA LOCAL INFILE '/home/shouldsee/Documents/repos/cathdb/cath-domain-list-S35.txt'
INTO TABLE s35 
FIELDS TERMINATED by '     ' lines terminated by '\n';

#### If however you got fixed-width CATH CLF.
LOAD DATA LOCAL INFILE '/home/shouldsee/Documents/repos/cathdb/cath-domain-list-S35-v4_1_0.txt' 
INTO TABLE s35
(@row)
SET domain_id = TRIM(SUBSTR(@row,1,7)),
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

SELECT domain_id,Class,arch,topo,homsf,s35 from s35 limit 5;
```
```mysql
mysql> select domain_id,Class,arch,topo,homsf,s35 from s35 limit 5; 
+----------+-------+------+------+-------+------+
| domain_id | Class | arch | topo | homsf | s35  |
+----------+-------+------+------+-------+------+
| 1oaiA00  |     1 |   10 |    8 |    10 |    1 |
| 3frhA01  |     1 |   10 |    8 |    10 |    2 |
| 1oksA00  |     1 |   10 |    8 |    10 |    3 |
| 4un2B00  |     1 |   10 |    8 |    10 |    4 |
| 1cukA03  |     1 |   10 |    8 |    10 |    5 |
+----------+-------+------+------+-------+------+

```
* Note that raw [CATH CLF files](http://download.cathdb.info/cath/releases/latest-release/cath-classification-data/README-cath-list-file-format.txt) are fixed-width.
* In case you are not familiar with the organisation of CATH, each "Class" node branches into "Architecture(arch)" children nodes, which in turn branches into "Topology(topo)" children nodes, so on and so forth. [CATH FAQ](http://wiki.cathdb.info/wiki-beta/doku.php?id=faq)
* Original "cath-domain-list-S35.txt" can be downloaded from [CATH](http://download.cathdb.info/cath/releases/all-releases/v4_1_0/cath-classification-data/cath-domain-list-S35-v4_1_0.txt)

Now we have a MySQL table containing all S35 representative structures (S35rep), which allows me to filter the table with some criteria. such as:
1. "`SELECT * FROM s35 WHERE Class=1;`" : This will give you all Class 1 S35rep's (You should get 4645 rows).
2. "`SELECT * FROM s35 WHERE resolution<1.0;`" : This should give all s35rep with a structual resolution < 1.0 (183 rows)

#### 2. Create relations between entries.

But there is something I can not fulfill using this structure: Some homologous family (homsf) will have a large number of s35rep (>100) whereas most homsf's will only have several (<5). So it is desirable to filter out the big homsf's only. For example, to count the s35rep in 1.10.8.10, just issue 
```
SELECT COUNT(*) FROM s35 WHERE (Class,arch,topo,homsf)=(1,10,8,10);
```
And it should return a table saying you got 53 entries, which should all be s35rep's. The problem is: **where should we store this number?** We can certainly add a "s35\_seqcnt" column into the "s35" table and set all s35rep in (1,10,8,10) to have a "s35\_seqcnt" of 53, but careful readers must feel dangerous with this approach, reasons are:
1. All entries in "s35" table represent s35rep nodes. From this perspective, any s35rep should only have a s35_count of 1, which refers to itself. 
2. Every time this number changes, (say one s35rep is removed), we will need to update all ~50 entries with the new value (say 52).

Think about it, s35seq_cnt is a property of homsf, not s35rep itself. If we had a homsf node representing (1,10,8,10), we could have easily set its s35seq_cnt field to be 53, solving both problems at once. Luckily, MySQL is also known as relational database, which means it is built to store relationship. In other words, we can store not only values (e.g: integers,floats,strings), but also cursors to other entries. For this hypothetical homsf node (1,10,8,10), we can actually store a list of cursors pointing to all 53 s35rep's contained within it. 
```mysql
DROP TABLE IF EXISTS homsf;
CREATE TABLE homsf
  (id INT AUTO_INCREMENT PRIMARY KEY, ### Set an index for cursor in the future
  s35_count int, ## This is new!
  Class int,
  arch int,
  topo int,
  homsf int,
  ### For homsf, we don't need index from s35 onwards, but we keep these fields to allow for easier manipulation.
  s35  int DEFAULT NULL,
  s60  int DEFAULT NULL,
  s95  int DEFAULT NULL,
  s100 int DEFAULT NULL,
  domain_length int DEFAULT NULL,
  resolution float DEFAULT NULL
  );

### Insert distinct entries into homsf.
### Since we set "id" to be AUTO_INCREMENT, we don't need to assign it since it will be auto-generated
INSERT INTO homsf (Class,arch,topo,homsf)
   SELECT DISTINCT Class,arch,topo,homsf FROM s35;
```
Now we would have a table containing all 2737 homsf's, but we have yet to establish the relation between 'homsf' and 's35'. We will use the "id" column of homsf since it is the indexed primary key, which allows for fast lookup. We will:
1. Create a "homsf_id" column in s35 to store its parental homsf node's id.
2. Fill this "homsf_id" using a for loop.
3. Add a foreign key constraint to this column. 

In fact, step 1,2 would suffice to specify the relation. Doing step 3 is only for maintainence purpose and constrain any future modification towards the tables, which is essentially a built-in test that every furture version of database has to pass. Though at beginning constraints is very annoying and throws many errors like:
1. ERROR 1215 (HY000): Cannot add foreign key constraint  (Oh gosh I want to add a constraint!!! Please let me do it!!! Plz!!!)
2. Error Code: 1452. Cannot add or update a child row: a foreign key constraint fails (Oh you evil constraint! Let go of my table!!! I need to modify it!!! I need to drop it!!! Now!!! Here!!!)
3. ...


#### 3. How to deal with errors, and fix your relationship:
Errors can be very, very annoying and could ruin hours and hours. However, once you understand how it works, these errors suddenly become useful indications that alert you of the potential hazard within commands you've just thrown upon MySQL. This is strictly speaking not a TDD example, since the test is not written for development but merely for maintaining the integrity of the database. Nevertheless, to understand the conept of "Test" on its own is essential to move on to the idea of TDD.

Now let's implement the stated operations in MySQL.

```mysql

### We split these ADD COLUMN commands since they might throw error if homsf_id already exists, but it would require custom procedure to avert so is not included here.
ALTER TABLE s35 
   ADD COLUMN homsf_id INT;


### Fill s35.homsf_id with correct cursors to homsf.id
### This should only be executed if every s35 can find a homsf. One way to ensure this condition is to create a fresh homsf table from s35. Other approaches with INSERT should be possible.

UPDATE s35
  LEFT JOIN homsf 
  ON  ( s35.Class, s35.arch, s35.topo, s35.homsf) = ( homsf.Class, homsf.arch, homsf.topo, homsf.homsf)
  SET s35.homsf_id=homsf.id;

### Impose the foreign key constraint.
ALTER TABLE s35
   ADD CONSTRAINT homsf_fk
   FOREIGN KEY(homsf_id)
   REFERENCES homsf(id); 

SELECT COUNT(*) FROM homsf; ### Confirm homsf does not change size
```

It is useful to simulate a 1452 error to illustrate how to debug a foreign key.
```mysql
### Temporarily remove the foreign key.
ALTER TABLE s35
   DROP FOREIGN KEY homsf_fk;
### Artificially damage the table
DELETE FROM homsf
  WHERE id = 1;
###
UPDATE s35
  SET homsf_id=1234
  WHERE s35.homsf_id=2;
### NEVER do this to a productive database!!
UPDATE s35
  SET homsf_id=1234567
  WHERE s35.homsf_id=3;

### Attempt to impose the foreign key constraint.
ALTER TABLE s35
   ADD CONSTRAINT homsf_fk
   FOREIGN KEY(homsf_id)
   REFERENCES homsf(id);
```


Commands above should throw a 1452:
```mysql
ERROR 1452 (23000): Cannot add or update a child row: a foreign key constraint fails (`TEST`.`#sql-78c0_66a`, CONSTRAINT `homsf_fk` FOREIGN KEY (`homsf_id`) REFERENCES `homsf` (`id`))
```

We can find out which key is missing with SELECT ... WHERE ...NOT IN. But note this will NOT report that homsf_id=2 has been redirected to homsf_id=1234 !!
```mysql
SELECT DISTINCT Class,arch,topo,homsf,homsf_id FROM s35
   WHERE s35.homsf_id NOT IN (SELECT id FROM homsf);
UPDATE s35
  LEFT JOIN homsf 
  ON  ( s35.Class, s35.arch, s35.topo, s35.homsf) = ( homsf.Class, homsf.arch, homsf.topo, homsf.homsf)
```
```mysql
+-------+------+------+-------+----------+
| Class | arch | topo | homsf | homsf_id |
+-------+------+------+-------+----------+
|     1 |   10 |    8 |    10 |        1 |
|     1 |   10 |    8 |    40 |  1234567 |
+-------+------+------+-------+----------+
```
By inspection, we found homsf_id 1 and 1234567 is not referring to any existing homsf.id, perventing us from installing a constraint. So we might consider create new homsf to accommodate these s35 entries. But wait a minute, we don't want to create new homsf that coincide with an existing homsf! We can ensure this by trying to update homsf_id according to existing homsf table.
```mysql
#### Save the sub-table with failed keys to a temp table.
DROP TABLE IF EXISTS temp;
CREATE TABLE temp
SELECT DISTINCT * FROM s35
   WHERE s35.homsf_id NOT IN (SELECT id FROM homsf);

#### Dump the proposed fix into a table `temp_fix`
DROP TABLE IF EXISTS temp_fix;
CREATE TABLE temp_fix
SELECT s35.id,
  homsf_id,
  homsf.id as fixed_homsf_id FROM temp AS s35
  LEFT JOIN homsf 
  ON ( s35.Class, s35.arch, s35.topo, s35.homsf) = ( homsf.Class, homsf.arch, homsf.topo, homsf.homsf);
####
SELECT * FROM temp_fix;
```
We can see that MySQL proposed a valid change for 58th s35 but NULL for the rest. We can apply the proposed update, and reinstall the foreign key constraint.

```mysql
UPDATE s35 
  JOIN temp_fix ON s35.id = temp_fix.id
  SET s35.homsf_id = temp_fix.fixed_homsf_id;

ALTER TABLE s35
   ADD CONSTRAINT homsf_fk
   FOREIGN KEY(homsf_id)
   REFERENCES homsf(id);  
```
At first glance, one would expect foreign key to fail agian, because we know some homsf_id was updated to NULL, which is not withinse homsf.id. However, a NULL does not constitue a violation to foregin key constraint. To illustrate in more detail:
```mysql
SELECT COUNT(*) FROM s35 WHERE homsf_id is NULL; ## returns 53
SELECT COUNT(*) FROM s35 
  WHERE homsf_id IS NULL 
  AND homsf_id IN (SELECT id FROM homsf); ## Returns 0
```
We see that homsf_id=NULL is indeed not considered within the homsf.id. We conclude foreign key constraint allows exception only if the expcetion is NULL.

Recall that we redirected homsf_id=2 to homsf_id=1234 when destroying the database. Note this was not fixed during the procedure above. We can compare entries from s35 and from homsf
```mysql
SELECT DISTINCT Class, arch, topo, homsf,id,homsf_id
   FROM s35 WHERE homsf_id=1234;
SELECT DISTINCT Class, arch, topo, homsf,id AS homsf_id
   FROM homsf WHERE id=1234;
```

Result:
```mysql
mysql> SELECT DISTINCT Class, arch, topo, homsf,id,homsf_id
    ->    FROM s35 WHERE homsf_id=1234;
+-------+------+------+-------+------+----------+
| Class | arch | topo | homsf | id   | homsf_id |
+-------+------+------+-------+------+----------+
|     1 |   10 |    8 |    20 |   54 |     1234 |
|     1 |   10 |    8 |    20 |   55 |     1234 |
|     1 |   10 |    8 |    20 |   56 |     1234 |
|     1 |   10 |    8 |    20 |   57 |     1234 |
|     2 |   60 |   40 |  1330 | 7906 |     1234 |
+-------+------+------+-------+------+----------+
5 rows in set (0.00 sec)

mysql> SELECT DISTINCT Class, arch, topo, homsf,id AS homsf_id
    ->    FROM homsf WHERE id=1234;
+-------+------+------+-------+----------+
| Class | arch | topo | homsf | homsf_id |
+-------+------+------+-------+----------+
|     2 |   60 |   40 |  1330 |     1234 |
+-------+------+------+-------+----------+
1 row in set (0.01 sec)
```
Some homsf_id is clearly pointing to the wrong homsf entry, without breaking the foregin key constraint, which render the foregin key meaningless. Think about it, if we want to access the homsf_index of a given s35 (id=54), should we:
    1. query the s35 table at (Class,arch,topo,homsf) or
    2. query the homsf entry as specified homsf_id '1234' ?  


With the first approach , query returns 1.10.8.20, whereas with the second approach, query returns 2.60.40.1330. How should we resolve such conflict? Obviously, if we were to enjoy the privlege of foreign key, we should keep the result from second approach. Why? Because we don't even need foreign key in the first approach! 

In reality, however, one would prefer to avoid generating such conflict in the first place, which can be achieved by dropping the (Class, arch, topo, homsf) columns from s35 table, effectively rendering first approach inviable and forcing the second approach. We will not expand the full implementation here and please feel free to practice it.



#### Sidenotes:
* NULL or NOT NULL, this is a question:

  ​Recall we updated some homsf_id to NULL in s35 when attempting the fix. This is only possible if the homsf_id column is nullable. We can check the column property by calling
  ```sql
  SHOW COLUMNS FROM s35;
  ```
  And check the "Null" column of the output.

* DROP TABLE IF NOT EXISTS: 
  This command may not work on some version of SQL. It is quite handy to append "if not exists" to avoid error, but unfortunately it is not available for commands like ADD COLUMN, DROP COLUMN.

* Cross database FOREIGN KEY error:

  When attempting to drop a database that is referred by other database, one would raise ERROR 1217 (23000) at line xxx: Cannot delete or update a parent row: a foreign key constraint fails. Two options availabe:
  1. Inspect the violated foreign key and attempt manual fix by checking "LATEST FOREIGN KEY ERROR" from the output of :
  ```mysql
  SHOW ENGINE INNODB STATUS;
  ```
  2. Disable foreign key constraint and force a drop (only if you are confident this won't break anything.)

  ```mysql
  SET foreign_key_checks = 0;
  DROP DATABASE ...
  SET foreign_key_checks = 1;
  ```

* CUSTOM PROCEDURE: 
  Custom functions in SQL is called procedures, but beginners like me should avoid writing custom functions whenever possible, because they are very difficult to write correctly!
* Version Control:
  To make sure results are reproducible, one should always write purposeful codes stored in files, preferably ending with ".sql". To avoid having to write SQL procedures, one may consider defining bash function that execute a designated ".sql" file instead and writing corresponding tests in bash. Another workaround is to store SQL code in Django migration files and execute using [django.db.migrations.RunSQL()](https://docs.djangoproject.com/en/1.11/ref/migration-operations/#runsql). By keeping a track of data source flatfiles,".sql" files and ".py" migration files and even ".json" [fixtures](https://coderwall.com/p/mvsoyg/django-dumpdata-and-loaddata), we can restore to any state we want.

Feng Geng<br />
Summer Student<br />
ISMB,UCL

[/markdown]
