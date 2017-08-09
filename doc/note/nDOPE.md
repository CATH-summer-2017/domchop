Interim Report:

Introduction:
Doped_CATH is a data browser aiming to provide rapid prototyping of data browsing. 

Domchop
One of the major functionality of CATH is to chop newly acquired structures into separated domains to which an evolutionary relation may be assigned. This process is not yet fully automated due to the absence of an algorithmic definition of domain and the inherent subjectivity in structural domain. Nevertheless, manual curation has been very useful in making decisions for tricky cases where existing algorithms become unreliable. The manual curation process is implented on a perl-based platform called "Domchop"

Report:
During the practice of manual curation (Domchop) , we realise the complexity of the chopping varies from case to case. In some cases the structure is completely unpacked (example needed) which supposedly can be rapidly detected using simple algorithms. Whereas in difficult cases (including metabolic assembly, polymerising machinery, spliceosome, transport assembly), even manual inspection cannot easily reach a consensus, where literature/expert advice needs to be consulted. Thus it is desirable to concentrate human efforts on labelling more challenging cases in order to optimise the efficiency of Domchopping. This can be done by filtering the candidate structures algorithmically, or at least sorting them according the predicted task difficulty. Currently Domchop labels each manually chopped structrue with one of "hard","medium","easy", and we hope to use this dataset to test any proposed predictor of task difficulty.

Most of my coding efforts were, however, devoted to another filtering approach proposed by Dr.Natalie Dawson. The hypothesis is that normalised DOPE (Discrete Optimized Protein Energy), also known as nDOPE or zDOPE, should predict the protein-likeness of any given molecular structure, and flag up unpacked structures (destined to be easy cases) as less protein-like (higher nDOPE). Although I have been able to borrow existing modules from Modeller to calculate nDOPE for a given PDB structure, the output seems insensible in some cases: A single helix can have very low nDOPE, and well-packed structure sometimes give high nDOPE. On a closer inspection, we collected residue-specific nDOPE scores and found that nDOPE penalises exposed hydrophobic residues but not charged residues. The reason for two apparently similar structures to have different nDOPE scores is that the cartoon representation does not contain the hyrdophobicity information any more. Thus I suggest Domchop to color protein in nDOPE score or hydrophobicity score. We can also explore the possibility of using DOPE energy predict the assigned fold class to prevent spurious assignment. 

<!-- ![1a02F00_nDOPE](https://github.com/CATH-summer-2017/domchop/blob/master/doc/imgs/1a02F00_nDOPE2.png) -->
<!-- ![1a02F00_hydro](https://github.com/CATH-summer-2017/domchop/blob/master/doc/imgs/1a02F00_hydro2.png) -->
<img src="https://github.com/CATH-summer-2017/domchop/blob/master/doc/imgs/1a02F00_nDOPE2.png" width="340"/>
<img src="https://github.com/CATH-summer-2017/domchop/blob/master/doc/imgs/1a02F00_hydro2.png" width="340"/>

Colored 1a02F00 (left:nDOPE, right:hydrophobicity) nDOPE = -1.87
<!-- ![1favA00_nDOPE](https://github.com/CATH-summer-2017/domchop/blob/master/doc/imgs/1favA00_nDOPE.png)
![1favA00_hydro](https://github.com/CATH-summer-2017/domchop/blob/master/doc/imgs/1favA00_hydro.png)
 -->
<img src="https://github.com/CATH-summer-2017/domchop/blob/master/doc/imgs/1favA00_nDOPE.png" width="340"/>
<img src="https://github.com/CATH-summer-2017/domchop/blob/master/doc/imgs/1favA00_hydro.png" width="340"/>

Colored 1favA00 (left:nDOPE, right:hydrophobicity) nDOPE = +0.77


Another important issue in visualising dataset huge as CATH is to have a good browser. At the start of the nDOPE project, I hacked up a python script that takes in an PDB and return a nDOPE score. The (structure, nDOPE) tuple is then stored in a flat file. I then easily flagged up structures with high nDOPE. However, in order to make sense of the observed nDOPE scores, I had to retrieve the structural information according to the domain_id and need to open different pages at different url. These labours were all simplified when I hacked up a webpage with embedded molecular viewer and meta information using Django, which enabled rapid browsing of multiple entries and displaying superfamily-level statistics. The data browser is useful in reducing the repetitive labour and allowing the user to focus on the critical thinking side. What's more, with superfamily level statistics, we can now test hypotheses on superfamily level, averaging noises from individual structures. In essence, a data browser enables efficient reproducibility, by building up a pipeline and set of routines. 

![browser1](https://github.com/CATH-summer-2017/domchop/blob/master/doc/imgs/browser_1_20_5_170.png)
![browser2](https://github.com/CATH-summer-2017/domchop/blob/master/doc/imgs/browser_1a02F00.png)
![browser3](https://github.com/CATH-summer-2017/domchop/blob/master/doc/imgs/browser_1favA00.png)

From this point, there is still plenty of space for thought: 
1. How should we utilise the nDOPised information to verify the homogeneity of a superfamily and flag potential outliers? Or could we use it to filter for potential remote homologies?
2. The key observation so far, is that nDOPE aggregate the information about domain packing, yet it is unclear how this information should be linked to structural homology. Nevertheless, at least we now have an efficient platform to test whatever hypothese that is of interest. For example, if we have hacked up an intermediate sequence search module, we can visualise very rapidly once the data is computed.
3. What will be the major factor affecting nDOPE? What is its distribution across the Class/Topology?
4. Another potential use of nDOPE, is to flag up co-existence of domains, by defining the domain-domain interaction energy. inter_nDOPE = combineDom_nDOPE - (dom1_nDOPE + dom2_nDOPE). Direct visualisation of (nDOPE1+nDOPE2 , internDOPE) should also help. Otherwise we can also use nDOPE to flag up an evolutionary trace from one superfamily into another superfamily where possible.
5. In the light that nDOPE forcefield includes information about hydrophobicity, should we try a different forcefield that suits better our purpose of filtering out unpacked structure? Or should we accept the fact that hydrophilic residues could stay unpacked anyway? Another idea would be using surface-area:volume ratio to identify structure with weird geometry. 
