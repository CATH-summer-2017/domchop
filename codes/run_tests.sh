cd "$(dirname "$0")" ### set directory to the same as this script

# source modpy.sh ##config environment variables for Modeller 
cd tests
for f in *.py
do
echo running $f

### alternatively, logging to individual files
# python $f > $f.log 

python $f

done
# echo 'All tests done'