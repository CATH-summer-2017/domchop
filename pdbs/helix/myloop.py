from modeller import *
from modeller.automodel import *
from modeller.parallel import *

class MyLoop(loopmodel):
    # This routine picks the residues to be refined by loop modeling
    def select_loop_atoms(self):
        # Two residue ranges (both will be refined simultaneously)
        return selection(
        	self.residue_range('2:', '78:'),
             # self.residue_range('45:', '50:')
             )
