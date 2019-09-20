#!/bin/bash

# Installing pip requirements
touch rooaa/local_settings.py
pip install -r requirements.txt

# Installing darknet model
if [  -d rooaa/ml-model/darknet ]; then
    rmdir rooaa/ml-model/darknet
fi
cd rooaa/ml-model
git clone https://github.com/pjreddie/darknet.git
cd darknet
make
wget https://pjreddie.com/media/files/yolov3.weights

# Installing densedepth model
cd ..
mkdir densedepth
cd densedepth
wget https://s3-eu-west-1.amazonaws.com/densedepth/nyu.h5
