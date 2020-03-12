import pathlib as pl


class Config:
    # Directory to Darknet ml model
    DARKNET_PATH = pl.Path("MLService/ml-model/darknet").absolute()

    # Directory to DenseDepth ml model
    DENSE_PATH = pl.Path("MLService/ml-model/densedepth").absolute()
