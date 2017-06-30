
#Python modules are fun, once you understand it

#### Brief:
Having the privilege of joining Orengo's group as a summer student, I feel urged to improve my coding as well as documentation skills. Thus I intend to log my coding and thinking in a series of blog posts, on a weekly basis. 

Today's blog post will cover some basics of organising Python code, in the hope of easing future maintenance. We will go through:
1. How to import python modules.
	* Comparing alternative implementations
2. How to write importable python modules.
	* Simplistic approach "``.py``" 
3. How to structure your python modules.
	* How does import work anyway?



#### 1. How to import python modules.
In Python, importing a module is common and useful. For example, "``numpy``" is a widespread module with handy matrix operations. If numpy is not installed on your machine. Try "``pip install numpy``".

For example, in python do:
```python
import numpy
rd = numpy.random.random()
print('Random number' + str(rd) + ' is generated')
```

You can also use your own alias when importing a module


```python
import numpy as np
rd = np.random.random()
print('Random number' + str(rd) + ' is generated')
```

You can even import a submodule on its own


```python
import numpy.random as random

#### Which is the right one to do now?
rd = random.random()
rd = random()

print('Random number' + str(rd) + ' is generated')
```


Question 1:


```python

#### Modify the import statement to make the code work

# import numpy.random as random

rd = rand()

print('Random number' + str(rd) + ' is generated')
```


You can also do "``help(np)``" or "``help(np.random)``" to read the manual, which would hopefully tell you about the submodules available for call. The above should remind you of how to import a installed module. Note I did not talk about what "``import``" does exactly, but this won't affect your usage of the command -- you know how it should look like.

Now, developers not only need to import installed modules, but also to actually write an importable module. To make it in context, we need a toy example. My favourite toy is cellular automata so I will just outline it here. 

Imagine you got a circular peptide chain of a fixed length, say 12 amino-acid(aa) residues(res). At every residue position, it can have one of the 20 universally-encoded amino acid. Now this protein has some strange behaviour. Every time it is passed from parent to progeny, its sequence change in a deterministic way. Each residue would look at the residue adjacent to it, and decide what aa it become in the next round. We call this process one round of evolution.

There are 20\*20\*20 = 8000 possible permutations that could happen, and we need to specify the resultant residue of the 8000 permutations. First let's assume the rule is simple, every of them become Ala (id:1) 

Let's create a python script "``main.py``" with the following commands.


```python
import numpy as np

### We fill the rule array with loads of 1's
rule = np.ones([ 20, 20, 20]) 

old = np.array([ 1, 5, 19, 7, 4, 6, 12, 6, 2, 9, 17, 3]);

new = old[:]; ## Create a independent copy. 
l = len(old)

for ( i, res) in enumerate(old):
	i_lef = i - 1;  ### numpy handle -1th entry swiftly as expected
	i_rig = ( i + 1 ) % l ## We do not want to access 13th entry from a 12-entry array.
	
	# res = old[ i ]; ### from definition
	res_lef = old[ i_lef ];
	res_rig = old[ i_rig ];

	### Look up the rule array
	new [i] = rule [ res_lef, res, res_rig  ];

print(new)
```


Due to the simplistic rule, we would expect a simple result.
```python
[1 1 1 1 1 1 1 1 1 1 1 1]
```

Okay this code is functional. But we feel the updating process is a bit lengthy. It'd be great if we can achieve some condensation, and that's where modules come in.

#### 2. How to write importable python modules.

##### Before making a module, make a function first:

Let's forget about modules and functions for a moment, just imagine you could tell python to do:

```python

import numpy as np

### We fill the rule array with loads of 1's
rule = np.ones([ 20, 20, 20]) 

old = np.array([ 1, 5, 19, 7, 4, 6, 12, 6, 2, 9, 17, 3]);

#### One line looks much simpler
new = evolve( old, rule)   ### Magic happens

#### Old code
# new = old[:]; ## Create a independent copy. 
# l = len(old)

# for ( i, res) in enumerate(old):
# 	i_lef = i - 1;  ### numpy handle -1th entry swiftly as expected
# 	i_rig = ( i + 1 ) % l ## We do not want to access 13th entry from a 12-entry array.
	
# 	# res = old[ i ]; ### from definition
# 	res_lef = old[ i_lef ];
# 	res_rig = old[ i_rig ];

# 	### Look up the rule array
# 	new [i] = rule [ res_lef, res, res_rig  ];
print(new)
```

This one-liner will become handy if we'd like to see the result after 1000 rounds, it will just be

```python

import numpy as np

### We fill the rule array with loads of 1's, and use a predefined starting sequence
rule = np.ones([ 20, 20, 20]) 
seq = np.array([ 1, 5, 19, 7, 4, 6, 12, 6, 2, 9, 17, 3]);

for evocount in range( 1000 ):
	new_seq = evolve( seq, rule)
	seq = new_seq

### both should work
print(seq) 
print(new_seq) 

```

This code obviously is not functional yet. Running it throws "``NameError: name 'evolve' is not defined``", which makes sense, for we did not define "``evolve``" anywhere at all. Define a function in python is straight forward. Let's define this magic called "``evolve()``":

```python
import numpy as np

def evolve( old, rule):
	new = old[:]; ## Create a independent copy. 
	l = len(old)

	for ( i, res) in enumerate(old):
		i_lef = i - 1;  ### numpy handle -1th entry swiftly as expected
		i_rig = ( i + 1 ) % l ## We do not want to access 13th entry from a 12-entry array.
		
		# res = old[ i ]; ### from definition
		res_lef = old[ i_lef ];
		res_rig = old[ i_rig ];

		### Look up the rule array
		new [i] = rule [ res_lef, res, res_rig  ];
	return(new) ### we return the output of the function to global namespace. 




rule = np.ones([ 20, 20, 20]) 
seq = np.array([ 1, 5, 19, 7, 4, 6, 12, 6, 2, 9, 17, 3]);

for evocount in range( 1000 ):
	new_seq = evolve( seq, rule)
	seq = new_seq

print(seq) 

```

Swift! The error was no more, at the expense of introducing a "``def``" statement. This "``def``" spans 14 lines, which is Okay, but sometimes it can get very lengthy and it destroys the effect of our simplification. Thus it'd be good to replace the "``def``" even further with "``import``".

##### So let's do some import magic

```python
import numpy as np
import evolve  #### Magic happens

rule = np.ones([ 20, 20, 20]) 
seq = np.array([ 1, 5, 19, 7, 4, 6, 12, 6, 2, 9, 17, 3]);

for evocount in range( 1000 ):
	new_seq = evolve( seq, rule)
	seq = new_seq

print(seq) 
```
As the module "``evolve``" is not defined yet (no magic yet), we'd expect "``ImportError: No module named evolve``". So, how on earth do we pack "``def``" into a module? A python module is essentially a "``.py``" script or a **directory** containing "``.py``" scripts. 

To create a "``evolve``" module, let's make a "``evolve.py``" under the **same** directory as "``main.py``" created earlier. 

"``evolve.py``"
```python
import numpy as np

def evolve( old, rule):
	new = old[:]; ## Create a independent copy. 
	l = len(old)

	for ( i, res) in enumerate(old):
		i_lef = i - 1;  ### numpy handle -1th entry swiftly as expected
		i_rig = ( i + 1 ) % l ## We do not want to access 13th entry from a 12-entry array.
		
		# res = old[ i ]; ### from definition
		res_lef = old[ i_lef ];
		res_rig = old[ i_rig ];

		### Look up the rule array
		new [i] = rule [ res_lef, res, res_rig  ];
	return(new) ### return the output of the function to global namespace
```

Remember to always save your changes in text editor! 

Let's run "``main.py``" again. Unfortunately, it still throws an error. "``TypeError: 'module' object is not callable``" If you look at the line reported, you should find the "``evolve( seq, rule)``" statement in "``main.py``". Generally, to "call" "``foo``", just means running "``foo()``".

If you remember **Question 1** from earlier with "``random.random()``", you should come up with "``evolve.evolve( seq, rule)``" as a solution. To make it clearer, let's change the name of "``evolve.py``" to "``lib.py``". Correspondingly "``main.py``" should change to:

```
import numpy as np
import lib
# from lib import evolve #### Alternative solution


rule = np.ones([ 20, 20, 20]) 
seq = np.array([ 1, 5, 19, 7, 4, 6, 12, 6, 2, 9, 17, 3]);

for evocount in range( 1000 ):
	new_seq = lib.evolve( seq, rule
	# new_seq = evolve( seq, rule) #### Alternative solution
	seq = new_seq

print(seq) 
```

Generally, it is good practice to keep the module name different from the submodules (like "``def``" within the script) contained within. e.g.: Do not place "``def evolve():``" in "``evolve.py``" to avoid confusing statement like "``evolve.evolve()``". 


##### 3. Organising your modules

At the moment everything is under the same directory "``.``" . However as your programme get bigger, more and more "``.py``" will be popping up, when it would be useful to separate modules for different purposes into different folders, so that you don't go through: "Okay I am gonna run a test suite, but which "``.py``"'s' should I run? Hmm let me have a browse..."

Too keep things simple, lets assign some names. We don't really care what the root directory "``.``" is called , but let's call it "``toy``". So at the moment there are two files "``toy/main.py``" and "``toy/lib.py``".

```
.
├── evolve.py
└── main.py

```

Conventionally, we store all easily importable modules into a directory "``lib/``" instead of a script. So let's do "``mkdir lib``" and "``mv lib.py lib/libA.py``". 

```
.
├── lib
│   └── libA.py
└── main.py
```

Runing "``main.py``" throws "``ImportError: No module named lib``". Python does not automatically recognise directory as importable. We need to flag a directory by placing __init__.py under it. Just do "``touch lib/__init__.py``".

Now "``main.py``" throws "``ImportError: cannot import name evolve``". Yah yah, nothing in "``lib/``" has the name "``evolve``". We need to update the "``main.py``" with "``from lib.libA import evolve``". Note "``import lib.libA.evolve``" would not work because "``evolve``" is defined as "``def``" and not a script "``.py``". 

Cool, now we even have a decent "lib/" folder! Another common directory in Test-Driven-Development (TDD) is "tests/". Let's create some look-alike structure with "``mkdir tests``", "``cp main.py tests/test1.py``"
```
.
├── lib
│   ├── __init__.py
│   └── libA.py
├── main.py
└── tests
    └── test1.py
```
Now in "``test1.py``", can we still import normally? Running "``tests1.py``" give "``ImportError: No module named lib.libA``". By default, "``import``" only search the directory where the running script exists, and then any directory on env variable $PYTHONPATH, which itself is default to $PATH if unset. 

Remember the "``main.py``" and "``test1.py``" are essentially identical, except in different directories. There are many possible fiexes here:
1.  include the root directory ("``toy/``") on $PATH, allowing "``test1.py``" to also access it.
2. 	Adding a statement in "``test1.py``" to alter the $PATH variable on the fly
3.	Some other module-based approach (still exploring)

Approach 2: OTF change to $PATH. See "``branch:orig2_tests_opt2``"
In "``test1.py``"
```python
import sys
sys.path.append('..')
``` 

Great! Above concludes my initial effort in organising my Python code, and hopefully reveal the magic behind "``import``" a little bit. I believe every python user is familiar with "``pip install``", and the frustration where this command fails (Or a worse case: it appears successful, but still shouting up "``ImportError``"). After understanding importing, installing a module boils down to place the importable modules on a suitable $PATH. And if your $PATH don't contain your installed module, it is expected to fail. There is also other issue like syntax difference between python2 and python3, but I hope the gist is clear.


Feng Geng<br />
Summer Student<br />
ISMB,UCL