-- drop table cath;
-- create table cath(domainID char(10),
--    class int,
--    arch int,
--    topo int,
--    homsf int,
--    s35  int,
--    s60  int,
--    s95  int,
--    s100 int,
--    s100_seqcnt int,
--    domain_length int,
--    resolution float);


ALTER TABLE cath
   ADD COLUMN s35_cnt

UPDATE cath
 SELECT COUNT(*) from 





use CATH;

delete from dopes;

load data local infile '/home/shouldsee/Documents/repos/cathdb/ref_DOPEs.csv' 
into table `dopes` 
fields terminated by ',' 
lines terminated by '\n';


delete from cath; 
-- // need fixing
load data local infile '/home/shouldsee/Documents/repos/cathdb/cath-domain-list-S35.txt' 
into table `cath` 
fields terminated by '     ' lines terminated by '\n';

-- // create new table
drop table doped_cath;
create table doped_cath 
select cath.*,dopes.nDOPE from cath 
inner join dopes on cath.domainID = dopes.domainID;


-- select * from doped_cath where nDOPE > 1.0;
select * from doped_cath where nDOPE > 1.0 
ORDER by nDOPE DESC, class ASC, arch ASC, topo ASC, homsf ASC
into OUTFILE '/tmp/out.tsv'
fields terminated by '\t';










alter table doped_cath add column homsf_id varchar(25);
update doped_cath set homsf_id = CONCAT(class,'.',arch,'.',topo,'.',homsf);


-- create table 410_doped_homsf select distinct homsf from 410_doped_s35;
create table 410_doped_homsf select distinct homsf from 410_doped_s35;


DROP table version;
create table version
	(id INT NOT NULL,
	name char(10),
	primary key (id)
	);
insert into version ( id, name)
	Values 
	(1, 'v4_1_0'),
	(2, 'current');

DROP table level;
create table level
	(id INT NOT NULL AUTO_INCREMENT,
	name char(30),
	letter char(1),
	primary key (id)
	);
insert into `level` ( letter, name)
	Values 
	('R', 'root')
	('C', 'Class'),
	('A', 'Architecture'),
	('T', 'Topology'),
	('H', 'Homologous Superfamily'),
	('S', 'Sequence Family (s35)'),
	('O', 'Orthologous Family (S60)'),
	('L', '“Like” domain (S95) '),
	('I', 'Identical domain (S100)'),
	('D', 'Domain counter');



use CATH;

drop table temp;
create table temp select * from doped_cath_high;

select * from temp limit 5;
alter table temp change domainID domain_id char(10);
alter table temp change class Class INT;
alter table temp ADD class_id INT NOT NULL AUTO_INCREMENT primary key;


drop table temp_s35;
drop table temp_class;
create table temp_class select distinct class_id, Class, arch, topo, homsf, s35, s60, s95, s100 from temp;
-- ALTER TABLE temp_class ADD class_id int NOT NULL AUTO_INCREMENT primary key;
alter table temp_class 
  ADD version_id INT NOT NULL, -- EDIT to make sure trustworthy
  ADD level_id INT NOT NULL,
  CHANGE class_id id INT;
UPDATE temp_class 
  SET version_id=1,
    level_id=5; -- EDIT to make sure trustworthy

-- Declare primary id 
alter table temp_class
  MODIFY id INT NOT NULL primary key AUTO_INCREMENT;
-- alter table temp_class
--   ADD CONSTRAINT version_fk
--   FOREIGN KEY(version_id)
--   REFERENCES version(id);
-- alter table temp_class
--   ADD CONSTRAINT level_fk
--   FOREIGN KEY(level_id)
--   REFERENCES level(id);
-- alter table temp_class MODIFY class_id INT NOT NULL primary key;


drop table temp_s35;
create table temp_s35 select domain_id, domain_length,resolution,nDOPE,class_id from temp;
-- alter table temp_s35 ADD raw_DOPE Float;

alter table temp_s35
  ADD id INT NOT NULL primary key AUTO_INCREMENT;
ALTER TABLE temp_s35 
  ADD raw_DOPE Double;
ALTER TABLE temp_s35 
  MODIFY nDOPE Double,
  MODIFY resolution DOUBLE,
  MODIFY domain_id varchar(7);
ALTER TABLE temp_s35
 change class_id classification_id INT;

ALTER TABLE temp_s35
 MODIFY classification_id INT NOT NULL,
 ADD CONSTRAINT classification_fk
 FOREIGN KEY(classification_id)
 REFERENCES temp_class(id);

SHOW columns from temp_s35;
SHOW columns from tst_domain;



USE DJANGO_CATH;

-- alter table version
--   rename to tst_version;

-- ALTER TABLE temp_s35
--  DROP COLUMN class_id;

INSERT INTO tst_version SELECT * FROM CATH.version;
INSERT INTO tst_level SELECT * FROM CATH.level;

-- create TABLE temp_class select * from CATH.temp_class;

delete from tst_version;
insert into tst_version ( id, name)
	Values 
	(1, 'v4_1_0'),
	(2, 'current');

delete from tst_level;
insert into tst_level ( letter, name)
	Values 
	('R', 'root')
	('C', 'Class'),
	('A', 'Architecture'),
	('T', 'Topology'),
	('H', 'Homologous Superfamily'),
	('S', 'Sequence Family (s35)'),
	('O', 'Orthologous Family (S60)'),
	('L', '“Like” domain (S95) '),
	('I', 'Identical domain (S100)'),
	('D', 'Domain counter');

CREATE TABLE temp_class select * from CATH.cath;
ALTER TABLE temp_class
  ADD COLUMN version_id int default 1,
  ADD COLUMN level_id int default 6;

INSERT INTO DJANGO_CATH.tst_classification 
 (Class,arch,topo,homsf,s35,s60,s95,s100,version_id,level_id)
select 
 class,arch,topo,homsf,s35,s60,s95,s100,version_id,level_id from temp_class;


-- ALTER TABLE tst_classification
--   MODIFY version_id int NULL,
--   MODIFY level_id int NULL;

-- INSERT INTO DJANGO_CATH.tst_classification 
--  (Class,arch,topo,homsf,s35,s60,s95,s100
--  select 
--  class,arch,topo,homsf,s35,s60,s95,s100 from CATH.cath;
	

-- ALTER TABLE tst_classification
--   MODIFY version_id int NOT NULL,
--   MODIFY level_id int NOT NULL;

INSERT INTO DJANGO_CATH.tst_classification (id,Class,arch,topo,homsf,s35,s60,s95,s100,version_id,level_id)
 select * from CATH.temp_class;

delete from DJANGO_CATH.tst_domain;
INSERT INTO DJANGO_CATH.tst_domain (domain_id,domain_length,resolution,nDOPE,classification_id,id,raw_DOPE) 
 SELECT * FROM CATH.temp_s35;

-- alter table temp_class
--   ADD CONSTRAINT version_fk
--   FOREIGN KEY(version_id)
--   REFERENCES tst_version(id);

-- alter table temp_class
--   ADD CONSTRAINT version_fk
--   FOREIGN KEY(version_id)
--   REFERENCES tst_version(id);


alter table CATH.temp_class
  ADD CONSTRAINT level_fk
  FOREIGN KEY(level_id)
  REFERENCES DJANGO_CATH.tst_level(id);

INSERT INTO DJANGO_CATH.tst_classification SELECT * FROM CATH.temp_class;


INSERT INTO tst_domain SELECT * FROM CATH.temp_s35;


-- ALTER TABLE `temp_class` ADD INDEX `id` (`id`);

-- alter table temp add homsf INT;




-- DELIMITER $$
-- CREATE PROCEDURE add_homsf_id(IN tablename varchar(100)) 
-- begin
-- alter table tablename add column homsf_id varchar(25);
-- update tablename set homsf_id = CONCAT(class,'.',arch,'.',topo,'.',homsf);
-- END$$
-- DELIMITER ;


-- DELIMITER $$
-- CREATE PROCEDURE add_homsf_id(IN tablename varchar(100)) 
-- begin
-- -- concat()
-- alter table (select tablename) add column homsf_id varchar(25);
-- update (select tablename) set homsf_id = CONCAT(class,'.',arch,'.',topo,'.',homsf);
-- END$$
-- DELIMITER ;


-- ;
-- CREATE PROCEDURE add_homsf_id(IN tablename varchar(100)) 
-- begin
-- alter table tablename add column homsf_id varchar(25);
-- update tablename set homsf_id = CONCAT(class,'.',arch,'.',topo,'.',homsf);
-- END;


update temp_s35, temp_class
SET	temp_s35.class_id = temp_class.class_id
WHERE temp_s35.Class = temp_class.Class
AND temp_s35.arch = temp_class.arch
AND temp_s35.topo = temp_class.topo
AND temp_s35.homsf = temp_class.homsf
AND temp_s35.s35 = temp_class.s35
AND temp_class.s60 = 1;	 

update temp_s35 
	SET  classification = temp_class.id 
	where temp_s35.Class = temp_class.Class
	AND temp_s35.arch = temp_class.arch
	AND temp_s35.topo = temp_class.topo
	AND temp_s35.homsf = temp_class.homsf
	AND temp_s35.s35 = temp_class.s35
	AND temp_class.s60 = 1;

-- SELECT 	*


select *
	FROM temp_s35
	INNER JOIN temp_class
	on temp_s35.Class = temp_class.Class
	AND temp_s35.arch = temp_class.arch
	AND temp_s35.topo = temp_class.topo
	AND temp_s35.homsf = temp_class.homsf
	AND temp_s35.s35 = temp_class.s35
	AND temp_class.s60 = 1 limit 10;

-- CREATE TABLE .table LIKE db1.table;


DROP PROCEDURE IF EXISTS ASSIGN_homsf;

DELIMITER ;;
CREATE PROCEDURE ASSIGN_homsf()
BEGIN
DECLARE n INT DEFAULT 0;
DECLARE i INT DEFAULT 0;
SELECT COUNT(*) FROM s35 INTO n;
SET i=1;
WHILE i<n DO 
  UPDATE 
  INSERT INTO table_B(ID, VAL) VALUES(ID, VAL) FROM table_A LIMIT i,1;
  SET i = i + 1;
END WHILE;
End;
;;

DELIMITER ;



DROP TABLE IF EXISTS temp;
CREATE TABLE temp
  SELECT domain_id,c.id as classification_id,domain_length,resolution FROM TEST.s35 AS a
  LEFT JOIN 
    (SELECT * FROM tst_classification WHERE level_id=5) AS c
  ON (a.Class, a.arch, a.topo, a.homsf, a.s35)=(c.Class, c.arch, c.topo, c.homsf, c.s35);
