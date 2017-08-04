# Domchop-util
 This repository includes the ongoing efforts in production of useful codes to facilitate the manual curation of domain chopping. Check our [wiki page](https://github.com/CATH-summer-2017/domchop/wiki) if you never heard of **DomChop**.
 
(UPDATE: 2017-08-04) The doped_CATH will be migrating to a separate repo called [`django_CATH`](https://github.com/CATH-summer-2017/django_CATH), to allow for easier management and greater portability. 

(UPDATED!!! 2017-07-14) If you are a Domchop curator. Please find the [`amazing_entries`](https://github.com/CATH-summer-2017/domchop/wiki/amazing_entries) page on `wiki` tab. Please also document interesting structures into `pdbs/` .



* Make sure you are on nDOPE branch before you test anything. **(Obsolete,`nDOPE` already merged into `master`)**


```sh
git fetch nDOPE
git checkout nDOPE
```


# Pre-requisite and configuration
**for Doped_CATH** 
-----
You should have **modeller** installed and configured as a pre-requisite. 

You should have modeller/bin on your $PATH variable. To set this temporarily, run 

```sh
export PATH="$PATH:/path-to-modeller/bin/"
source modpy.sh
```

For example, if you installed Modeller to "/home/linux/modeller", then run:

```sh
export PATH="$PATH:/home/linux/modeller/bin/"
source modpy.sh
```

You can add these two commands into `~/.bashrc`, so that it is automatically set next time you start a new bash shell.

Alternatively, you can simply issue a condensed one-liner.
```sh
source /home/linux/modeller/bin/modpy.sh 
```

# Tests

Please test the Modeller installation with:
```sh
chmod +x tests/verify_modeller.sh
tests/verify_modeller.sh
```

Please run tests with 

```bash
chmod +x run_tests.sh # To make the script executable
./run_tests.sh ## To run the tests
```

It should take ~10s to run all the tests.

