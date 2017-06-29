# Example for 'atom' objects

from modeller import *
from modeller.scripts import complete_pdb




# env = environ()
# #env.io.atom_files_directory = ['../atom_files']
# env.io.atom_files_directory = ['../pdbs']
# env.libs.topology.read(file='$(LIB)/top_heav.lib')
# env.libs.parameters.read(file='$(LIB)/par.lib')


pdbfile = "../pdbs/4xz8A_chop"
nDOPE_correct = -1.675

# def get_nDOPE( pdbfile, env = env):
def get_nDOPE( pdbfile):
# pdbfile = "4xz8A_chop"
#mdl = complete_pdb(env, "1fas")
	env = environ()
	#env.io.atom_files_directory = ['../atom_files']
	env.io.atom_files_directory = ['../pdbs']
	env.libs.topology.read(file='$(LIB)/top_heav.lib')
	env.libs.parameters.read(file='$(LIB)/par.lib')

	mdl = complete_pdb(env, pdbfile)
	nDOPE = mdl.assess_normalized_dope()
	return nDOPE


import unittest

class testcase(unittest.TestCase):
	def test_dope(self):
		nDOPE = get_nDOPE(pdbfile);
		errmsg = "nDOPE is incorrect being %.3f, should be %.3f"%( nDOPE, nDOPE_correct);
		self.assertAlmostEqual(nDOPE, nDOPE_correct, places=3, msg=errmsg, delta=None)


if __name__ == '__main__':
	unittest.main();


# print("Normalised z-score for DOPE (nDOPE) = %.3f " %( nDOPE) )

# # 'mdl.atoms' is a list of all atoms in the model
# print("Name of C-alpha atom in residue 4 in chain A: %s " \
#       % mdl.atoms['CA:4:A'].name)
# a = mdl.atoms[0]
# print("Coordinates of first atom: %.3f, %.3f, %.3f" % (a.x, a.y, a.z))

# # Each 'residue' object lists its own atoms, as does each chain
# a = mdl.residues['10:A'].atoms[0]
# print("Biso for first atom in residue 10 in chain A %.3f" % a.biso)

# a = mdl.chains[0].residues[-1].atoms[-1]
# print("Biso for last atom in last residue in first chain: %.3f" % a.biso)