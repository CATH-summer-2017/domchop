# Comparative using a provided initial structure file (inifile)
from modeller import *
from modeller.automodel import *    # Load the automodel class

log.verbose()
env = environ()

# directories for input atom files


# loopmodel(env, sequence, alnfile=None, knowns=[], inimodel=None, deviation=None,
# library schedule=None, csrfile=None, inifile=None, assess methods=None,
# loop assess methods=None)

env.io.atom_files_directory = ['.', '../atom_files']

a = automodel(env,
              alnfile  = '1favA00_self.ali',     # alignment filename
              knowns   = '1favA00.pdb',              # codes of the templates
              sequence = '1favA00.pdb',              # code of the target
              inifile  = '1favA00.pdb')    # use 'my' initial structure
a.starting_model= 1                 # index of the first model
a.ending_model  = 1                 # index of the last model
                                    # (determines how many models to calculate)
a.make()                            # do comparative modeling


