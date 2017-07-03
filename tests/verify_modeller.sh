source modpy.sh

if [ $? -eq 0 ]
then
	echo Modeller is present. Add "source modpy.sh" to ".bashrc" to enable it. 
else
	echo Could not source modpy.sh. Did you installed Modeller and include it in \$PATH?
fi