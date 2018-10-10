#!/bin/bash

. ./env.list

MYDIR=$(pwd)

REPO="maprpaccstreams"

git clone https://github.com/johnomernik/$REPO

# Build maprpaccstreams first
cd $REPO
sudo docker build -t $REPO .
if [ "$?" == "0" ]; then
    echo "Image Build $REPO- Success!"
else
    echo "$REPO Image did not build correctly - exiting"
    exit 1
fi
cd ..

# Build maprrtsp2stream
sudo docker build -t $APP_IMG .

if [ "$?" == "0" ]; then
    echo "Image Build - Sucess!"
else
    echo "Image did not build correctly"
    exit 1
fi
