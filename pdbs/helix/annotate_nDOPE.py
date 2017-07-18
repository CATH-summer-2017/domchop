#!/usr/bin/env python
from modeller import *
from modeller.scripts import complete_pdb

import argparse
import os
from os.path import join

import numpy as np

# log.very_verbose()

parser = argparse.ArgumentParser(description='Short sample app')
parser.add_argument('-r','--makeref', action="store_true", default=False, dest='newref',
					help="Calculate reference nDOPE for structures in ../pdbs/ using cuurent algorithm and store them to ''ref_nDOPEs.csv'' ")
parser.add_argument('-i','--input', action="store", default=None, dest="input_dir",
					help='Input: A pdb file or a directory containing PDB to test')
parser.add_argument('-j','--thread', action="store", default=None, dest="num_threads",
					type = int, help='Number of thread to use')
parser.add_argument('-o','--output', action="store", default=None, dest="output_file",
					help='Name of output csv file')
parser.add_argument('-a','--append', action="store_true", default=False, dest="append",
					help='Append to existing output file')
# parser.add_argument('-c', action="store", dest="c", type=int)
args =  parser.parse_args()


env = environ()
env.edat.dynamic_sphere = False
env.libs.topology.read(file='$(LIB)/top_heav.lib')
env.libs.parameters.read(file='$(LIB)/par.lib')

# Read the sequence, calculate its topology and coordinates:
if args.input_dir:
	# pdbfile = args.input_dir
	input_dir = os.path.abspath(args.input_dir)
	if os.path.isdir(input_dir):
			onlyfiles = [join(input_dir,f) for f in os.listdir(input_dir) if os.path.isfile(join(input_dir, f))]
	else:
		onlyfiles = [input_dir]
	onlyfiles = sorted(onlyfiles)
env.io.atom_files_directory = ['.','../atom_files',input_dir]

fail = 0;
if args.output_file:
	output_dir = os.path.abspath(args.output_file); 
else:
	output_dir = join(input_dir,'doped_pdbs/')
	print("No output dir provided, writing to %s"%output_dir)
if os.path.isdir(output_dir):
	pass 
else:
	try:
		os.mkdir(output_dir)
	except:
		fail = 1
		print("cannot make new directory '%s', writing to input directory instead"%output_dir)
		output_dir = input_dir	

	
print(output_dir)

for pdbfile in onlyfiles: 
	# pdbfile = "1owaA01.pdb";
	pdbfile = os.path.basename(pdbfile);
	if pdbfile.split('.')[-1]=='pdb':
		print("\n\n//Testing structure from %s" % pdbfile)
		# mdl = complete_pdb(env, pdbfile)


		mdl = model(env)
		mdl.read(pdbfile, model_format='PDB', model_segment=('FIRST:@', 'LAST:'), io=None);
		sel = selection(mdl)
		profile = sel.get_dope_profile()
		
		# profile = mdl.get_normalized_dope_profile()
			
		res_energy = [x.energy for x in profile];
		factor = 10 ** ( 
			int(
				np.log10(
					max( 
						(abs(x) for x in res_energy)
						) 
					)
			    - 3  
			   )  + 1 
			)
		
		for res,pf_ele in zip(mdl.residues, profile):
			for a in res.atoms:
				a.biso = pf_ele.energy/factor;
		
		outfname =  pdbfile.rstrip('.pdb')+'_doped.pdb'
		outfile = join(output_dir,outfname);
		
		mdl.remark='''HEADER nDOPE_unit=%fau
		''' % (factor,)

		mdl.write(file=outfile)
	
