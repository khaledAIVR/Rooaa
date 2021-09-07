# Installing darknet model
cd mlservice/ml-model/darknet
curl https://pjreddie.com/media/files/yolov3.weights --output yolov3.weights

# Installing densedepth model
cd ..
mkdir densedepth
cd densedepth
gdown https://drive.google.com/uc?id=19dfvGvDfCRYaqxVKypp1fRHwK7XtSjVu
