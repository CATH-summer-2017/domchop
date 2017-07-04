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
