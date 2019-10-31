#!/bin/bash

# Installing darknet model
cd rooaa/ml-model/darknet
wget https://pjreddie.com/media/files/yolov3.weights

# Installing densedepth model
cd ..
mkdir densedepth
cd densedepth
wget https://s3-eu-west-1.amazonaws.com/densedepth/nyu.h5
