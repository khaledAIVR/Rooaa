#!/bin/bash

# Downloading yolov3 weights
if [ -f yolov3.weights ]
  then
    echo "yolov3.weights already exists"
else
    curl https://pjreddie.com/media/files/yolov3.weights --output yolov3.weights
fi; 

# Downloading densedepth weights
if [ -f nyu.h5 ]
  then
    echo "nyu.h5 already exists"
else
    wget https://s3-eu-west-1.amazonaws.com/densedepth/nyu.h5 -O nyu.h5
fi;
