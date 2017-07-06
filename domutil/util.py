from modeller import *
from modeller.scripts import complete_pdb
def get_nDOPE( pdbfile, env = None):
# pdbfile = "4xz8A_chop"
#mdl = complete_pdb(env, "1fas")
	
	### Use existing environment to avoid redundant re-initialisation.
	if not env:
		env = environ()

		
	#env.io.atom_files_directory = ['../atom_files']
	env.io.atom_files_directory = ['../pdbs']
	env.libs.topology.read(file='$(LIB)/top_heav.lib')
	env.libs.parameters.read(file='$(LIB)/par.lib')

	mdl = complete_pdb(env, pdbfile)
	nDOPE = mdl.assess_normalized_dope()
	return nDOPE
	
import csv

def csv_listener(q):
    '''listens for messages on the q, writes to file. '''
    ## Read "fname" from global. "fname" file must exists prior to call.

    f = open(fname, 'ra') 
    c = csv.writer(f)
    while 1:
        m = q.get()
        if m == 'kill':
            f.write('killed \n')
            break
        elif m == 'clear':
        	f.truncate();	
        else:## Asumme a csv row
        	row = m
        	c.writerow( row )
        f.flush()
    f.close()



def worker( i, q, slist):
	# global wait, waitname
	# pdbfile = onlyfiles[i];
	(wait,waitname,reset,fname,env) = slist
	pdbfile = i;
	import os 
	pdbname = os.path.basename(pdbfile);

	if pdbname.split(".")[-1] in ["bak","csv"] or wait:
		if pdbname == waitname:
			q.put('start');
			nDOPE = get_nDOPE( pdbfile, env = env)
		row = [pdbname, nDOPE ];
	else:	
		print("\n\n//Testing structure from %s" % pdbfile)
		nDOPE = get_nDOPE( pdbfile, env = env)				
		row = [pdbname, nDOPE] ;
	q.put( row );
	
	return row
