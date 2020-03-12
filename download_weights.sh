# Installing darknet model
cd mlservice/ml-model/darknet
curl https://pjreddie.com/media/files/yolov3.weights --output yolov3.weights

# Installing densedepth model
cd ..
mkdir densedepth
cd densedepth
curl https://s3-eu-west-1.amazonaws.com/densedepth/nyu.h5 --output nyu.h5
