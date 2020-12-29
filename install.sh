MODEL="/modules/model"
CURDIR=`pwd`
if [ -d "$MODEL" ] 
then
	echo "$MODEL installed"
else
	echo "$MODEL not installed"
	echo "installing now"
	mkdir "$CURDIR
fi
