cd "$(dirname "$0")" ### set directory to the same as this script
# source config_modeller.sh ## config environment variables for Modeller 
cd tests
for f in *.py
do
echo running $f
# python $f > $f.log
python $f

done
echo 'All tests done'