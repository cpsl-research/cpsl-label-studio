set -e

DATADIR=mydata

if [ ! -d $DATADIR ]; then
	mkdir -p $DATADIR
	chmod 777 $DATADIR
fi

docker pull heartexlabs/label-studio:1.12.1
docker run -it -p 8080:8080 -v $(pwd)/$DATADIR:/label-studio/data heartexlabs/label-studio:1.12.1
