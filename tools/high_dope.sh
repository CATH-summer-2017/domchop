
### You need to have "doped_cath" created in you MySQL database in order to run this routine 

## Custom commands used:
	# sqlcmd: Default to use "root" user at localhost to query MySQL;
	# tsv2csv



sqlcmd "CREATE TABLE doped_cath_high
		SELECT * FROM doped_cath WHERE nDOPE > 1.0
		ORDER BY nDOPE DESC, class ASC, arch ASC, topo ASC, homsf ASC;"

sqlcmd "SELECT * FROM doped_cath_high;" > high_nDOPE.csv
tsv2csv high_nDOPE.csv 
# 
# git commit . -m fixed_header;git push;
