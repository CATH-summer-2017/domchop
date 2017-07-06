#!/usr/bin/env python

# Example for 'atom' objects


# env = environ()
# #env.io.atom_files_directory = ['../atom_files']
# env.io.atom_files_directory = ['../pdbs']
# env.libs.topology.read(file='$(LIB)/top_heav.lib')
# env.libs.parameters.read(file='$(LIB)/par.lib')


# pdbfile = "../pdbs/4xz8A_chop"
# nDOPE_correct = -1.675

# nDOPE_lst = [('4xz8A_chop', -1.675),
# 				]

# def get_nDOPE( pdbfile, env = env):

import argparse

parser = argparse.ArgumentParser(description='Short sample app')
parser.add_argument('-r','--makeref', action="store_true", default=False, dest='newref',
					help="Calculate reference nDOPE for structures in ../pdbs/ using cuurent algorithm and store them to ''ref_nDOPEs.csv'' ")
parser.add_argument('-i','--input', action="store", default=None, dest="input_directory",
					help='Input directory containing PDB to test')
# parser.add_argument('-c', action="store", dest="c", type=int)
args =  parser.parse_args()

import sys,os,site
reload(site)
sys.path.append(os.path.abspath(
								os.path.join(
									os.path.realpath(__file__),
									 os.pardir,
									 os.pardir)
								)
				)

# for x in sys.path:
	# print(x)
# cwd = os.getcwd();

import unittest
from domutil.util import *


class testcase(unittest.TestCase):
	def test(self):
		# mdl = complete_pdb(env, pdbfile)
		# self.fail('what\'s this???')
		pass
	def test_modeller(self):	
	    try:
			from modeller import *
			from modeller.scripts import complete_pdb
	    except Exception as e:
	    	self.fail('Modeller is not installed or configured and raised exception:  ' + str(e) +'\n try running \'source config_modeller.sh\' ')
	    else:
			print("modeller module is loaded successfully")
			pass

	def test_dope(self):
		from modeller import log 
		log.none()  ### comment this line to recover verbosity to debug
		import csv
		fname = "ref_DOPEs.csv";
		# if not os.path.isfile(fname): ### Create log file if not existed
		# 	open(fname, "w").close();

		with open(fname, "r") as f:
			c = csv.reader(f);
			nDOPE_lst = list(c);
			i = 0;
			imax = len(nDOPE_lst)
			for pdbfile, nDOPE_correct in nDOPE_lst:
				print("\n\n//Testing structure from %s" % pdbfile)
				nDOPE = get_nDOPE(pdbfile);
				nDOPE_correct = float(nDOPE_correct)
				errmsg = "nDOPE for %s is incorrect being %.3f, should be %.3f"%( pdbfile, nDOPE, nDOPE_correct);
				self.assertAlmostEqual(nDOPE, nDOPE_correct, places=3, msg=errmsg, delta=None)
				i = i + 1
				print("%d of %d structure-nDOPE pairs passed tests" % ( i, imax))

			if i == 0:
				self.fail("No test set availabe")
			print("All pdbs yielded expected nDOPE z-scores")


if __name__ == '__main__':
	


	if args.newref or args.input_directory:
		from modeller import *
		from modeller.scripts import complete_pdb
		# from domutil.util import *
		env = environ();

		if not args.input_directory:
			mypath = "../pdbs/"
		else:
			# mypath = input_directory;#
			mypath = os.path.abspath(args.input_directory)

		# print(mypath)
		from os import listdir
		from os.path import isfile, join

		if os.path.isdir(mypath):
			onlyfiles = [join(mypath,f) for f in listdir(mypath) if isfile(join(mypath, f))]
		else:
			onlyfiles = [mypath]

		onlyfiles = sorted(onlyfiles)

		# print(onlyfiles)

		wait = 0;
		waitname = "4j27A02";
		reset = 1;
		fname = "ref_DOPEs.csv"

		shared_lst = (wait,waitname,reset,fname,env);

		if reset:
			open(fname,"w").close()

		##### Parallel routine
		import multiprocessing as mp
		import logging
		# mpl = mp.log_to_stderr()
		# mpl.setLevel(logging.INFO)
		manager = mp.Manager()
		q = manager.Queue();   
		pool = mp.Pool( mp.cpu_count() - 1);

		### CSV listener I/O to "fname"
		watcher = pool.apply_async( csv_listener, (q,));
		
		#fire off workers
		jobs = [];
		# print(onlyfiles)
		for pdbfile in onlyfiles:
			job = pool.apply_async( worker, (pdbfile,q,shared_lst) )
			jobs.append( job )

		# collect results from the workers through the pool result queue
		for job in jobs:
			job.get()

		#now we are done, kill the listener
		q.put('kill')
		pool.close()


		#### Single-thread routine	
		# import csv
		# nDOPEs = [];
		# tested_files = [];
		# with open(fname, "a") as f:
		# 	c = csv.writer(f)
		# 	for pdbfile in onlyfiles:
		# 		pdbname = os.path.basename(pdbfile);
		# 		if pdbfile.split(".")[-1] in ["bak"] or wait:
		# 			# onlyfiles.pop(pdbfile);
		# 			if pdbname == waitname:
		# 				wait = 0;
		# 			continue
		# 		print("\n\n//Testing structure from %s" % pdbfile)
		# 		nDOPE = get_nDOPE( join(pdbfile), env = env)
		# 		nDOPEs.append( nDOPE );
		# 		tested_files.append( pdbname );
		# 		c.writerow( [pdbname, nDOPE] )
		# 		f.flush()
			
		# 	for row_vals in zip(tested_files, nDOPEs):
		# 		# row = "\t".join(row_vals)+"\n"
		# 		c.writerow(row_vals);

	else:
		unittest.main();

		# print(zip(onlyfiles, nDOPEs))



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