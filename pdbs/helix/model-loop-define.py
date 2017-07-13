from modeller import *
from modeller.automodel import *
from modeller.parallel import *
from myloop import MyLoop
log.verbose()
env = environ()

env.io.atom_files_directory = ['.', '../atom_files']

# Create a new class based on 'loopmodel' so that we can redefine
# select_loop_atoms

j = job()
j.append(local_slave())
j.append(local_slave())
j.append(local_slave())
j.append(local_slave())
j.append(local_slave())
j.append(local_slave())
j.append(local_slave())


aln = alignment(env)
mdl = model(env)
env = environ()


code = "1favA00_mod1.pdb"
mdl.read(file=code,model_segment=('FIRST:@','END:'))
aln.append_model(mdl,align_codes=code,atom_files=code)

mdl.read(file=code,model_segment=('FIRST:@','END:'))
aln.append_model(mdl,align_codes=code,atom_files=code)

aln.malign()
alifile = 'temp_self.ali'
aln.write(file=alifile)


a = MyLoop(env,
              alnfile  = alifile,     # alignment filename
              knowns   = code,              # codes of the templates
              sequence = code,              # code of the target
              inifile  = code,
              loop_assess_methods=assess.DOPE)    # use 'my' initial structure
# a = MyLoop(env,
#            alnfile  = 'al.ali',      # alignment filename
#            knowns   = '5fd1',               # codes of the templates
#            sequence = '1fdx',               # code of the target
#            loop_assess_methods=assess.DOPE) # assess each loop with DOPE
a.starting_model= 1                 # index of the first model
a.ending_model  = 1                 # index of the last model

a.loop.starting_model = 1           # First loop model
a.loop.ending_model   = 10           # Last loop model
a.use_parallel_job(j) 


a.make()                            # do modeling and loop refinement
