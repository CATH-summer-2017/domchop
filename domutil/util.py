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
