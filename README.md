# 
Make sure you are on nDOPE branch before you test anything

```sh
git fetch nDOPE
git checkout nDOPE
```


# Pre-requisite and configuration
You should have **modeller** installed and configured as a pre-requisite. 

You should have modeller/bin on your $PATH variable. To set this temporarily, run 

```sh
export PATH="$PATH:/path-to-modeller/bin/"
source modpy.sh
```

For example, if you installed Modeller to /home/linux/modeller, run

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

Please run tests with 

```bash
chmod +x run_tests.sh # To make the script executable
./run_tests.sh ## To run the tests
```

It should take ~10s to run all the tests.

