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

nDOPE_lst = [('4xz8A_chop', -1.675),
				]

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
	def test(self):
		# self.pass()
		# mdl = complete_pdb(env, pdbfile)
		# self.fail('what\'s this???')
		pass
	def test_dope(self):
		import csv
		with open("ref_DOPEs.csv", "r") as f:
			c = csv.reader(f);
			nDOPE_lst = c;

			for pdbfile, nDOPE_correct in nDOPE_lst:
				nDOPE = get_nDOPE(pdbfile);
				nDOPE_correct = float(nDOPE_correct)
				errmsg = "nDOPE for %s is incorrect being %.3f, should be %.3f"%( pdbfile, nDOPE, nDOPE_correct);
				self.assertAlmostEqual(nDOPE, nDOPE_correct, places=3, msg=errmsg, delta=None)


if __name__ == '__main__':
	unittest.main();
	

	# # get_nDOPE("")
	# mypath = "../pdbs/"
	# from os import listdir
	# from os.path import isfile, join
	# onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
	# nDOPEs=[];
	# for pdbfile in onlyfiles:
	# 	nDOPEs.append(get_nDOPE(pdbfile));

	# import csv
	# with open("ref_DOPEs.csv", "w") as f:
	# 	c = csv.writer(f)
	# 	for row_vals in zip(onlyfiles, nDOPEs):
	# 		# row = "\t".join(row_vals)+"\n"
	# 		c.writerow(row_vals);
	# 	# print(zip(onlyfiles, nDOPEs))



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