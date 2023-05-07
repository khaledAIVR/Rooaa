import pathlib as pl


class Config:
    # Directory to Darknet ml model
    DARKNET_PATH = pl.Path("MLService/ml-model/darknet").absolute()
    DARKNET_WEIGHTS_PATH = pl.Path("yolov3.weights")
    DARKNET_CFG_PATH = DARKNET_PATH / pl.Path("yolov3.cfg")
    DARKNET_COCO_PATH = DARKNET_PATH / pl.Path("coco/coco.names")

    # Directory to DenseDepth ml model
    DENSE_PATH = pl.Path("MLService/ml-model/densedepth").absolute()
    DENSE_WEIGHTS_PATH = pl.Path("nyu.h5")
