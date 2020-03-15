import glob
import os
import pathlib as pl
from threading import Lock

import cv2
import keras.backend as K
import keras.utils.conv_utils as conv_utils
import numpy as np
import tensorflow as tf
from keras.engine.topology import InputSpec, Layer
from keras.models import load_model
from PIL import Image

from settings import Config


class BilinearUpSampling2D(Layer):
    def __init__(self, size=(2, 2), data_format=None, **kwargs):
        super(BilinearUpSampling2D, self).__init__(**kwargs)
        self.data_format = K.normalize_data_format(data_format)
        self.size = conv_utils.normalize_tuple(size, 2, 'size')
        self.input_spec = InputSpec(ndim=4)

    def compute_output_shape(self, input_shape):
        if self.data_format == 'channels_first':
            height = self.size[0] * \
                input_shape[2] if input_shape[2] is not None else None
            width = self.size[1] * \
                input_shape[3] if input_shape[3] is not None else None
            return (input_shape[0],
                    input_shape[1],
                    height,
                    width)
        elif self.data_format == 'channels_last':
            height = self.size[0] * \
                input_shape[1] if input_shape[1] is not None else None
            width = self.size[1] * \
                input_shape[2] if input_shape[2] is not None else None
            return (input_shape[0],
                    height,
                    width,
                    input_shape[3])

    def call(self, inputs):
        input_shape = K.shape(inputs)
        if self.data_format == 'channels_first':
            height = self.size[0] * \
                input_shape[2] if input_shape[2] is not None else None
            width = self.size[1] * \
                input_shape[3] if input_shape[3] is not None else None
        elif self.data_format == 'channels_last':
            height = self.size[0] * \
                input_shape[1] if input_shape[1] is not None else None
            width = self.size[1] * \
                input_shape[2] if input_shape[2] is not None else None

        return tf.image.resize(inputs, [height, width], method=tf.image.ResizeMethod.BILINEAR, align_corners=True)

    def get_config(self):
        config = {'size': self.size, 'data_format': self.data_format}
        config.update(super(BilinearUpSampling2D, self).get_config())
        return config


def dense_load_model():
    """ Loads model"""

    # Keras / TensorFlow
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '5'

    # Custom object needed for inference and training
    custom_objects = {
        'BilinearUpSampling2D': BilinearUpSampling2D, 'depth_loss_function': None}

    print('Loading model...')
    K.clear_session()

    # Load model into GPU / CPU
    model = load_model(Config.DENSE_PATH / pl.Path("nyu.h5"),
                       custom_objects=custom_objects, compile=False)
    model._make_predict_function()
    return model


class DenseModel:
    """ Class containing DenseDepth ML model and helper methods. """
    model = dense_load_model()
    model_lock = Lock()

    def __init__(self, image_path):
        """ Loads model with given image. """
        self.image_path = image_path
        img = cv2.imread(image_path)
        self.img_h, self.img_w, _ = img.shape

    def dense_predict(self):

        inputs = load_images(glob.glob(self.image_path))
        outputs = predict(inputs)
        save_images(self.image_path, outputs)
        resize(self.image_path, self.img_w, self.img_h)


def predict(images, minDepth=10, maxDepth=1000, batch_size=2):
    # Support multiple RGBs, one RGB image, even grayscale
    if len(images.shape) < 3:
        images = np.stack((images, images, images), axis=2)
    if len(images.shape) < 4:
        images = images.reshape(
            (1, images.shape[0], images.shape[1], images.shape[2]))

    # Compute predictions
    with DenseModel.model_lock:
        predictions = DenseModel.model.predict(images, batch_size=batch_size)
    # Put in expected range
    return np.clip(maxDepth / predictions, minDepth, maxDepth) / maxDepth


def load_images(image_files):
    loaded_images = []
    for img in image_files:
        x = np.clip(np.asarray(Image.open(img), dtype=float) / 255, 0, 1)
        loaded_images.append(x)
    return np.stack(loaded_images, axis=0)


def to_multichannel(i):
    if i.shape[2] == 3:
        return i
    else:
        i = i[:, :, 0]
        return np.stack((i, i, i), axis=2)


def display_images(outputs, inputs=None, gt=None, is_colormap=True, is_rescale=True):
    import matplotlib.pyplot as plt
    import skimage
    from skimage.transform import resize

    plasma = plt.get_cmap('plasma')

    shape = (outputs[0].shape[0], outputs[0].shape[1], 3)

    all_images = []

    for i in range(outputs.shape[0]):
        imgs = []

        if isinstance(inputs, (list, tuple, np.ndarray)):
            x = to_multichannel(inputs[i])
            x = resize(x, shape, preserve_range=True,
                       mode='reflect', anti_aliasing=True)
            imgs.append(x)

        if isinstance(gt, (list, tuple, np.ndarray)):
            x = to_multichannel(gt[i])
            x = resize(x, shape, preserve_range=True,
                       mode='reflect', anti_aliasing=True)
            imgs.append(x)

        if is_colormap:
            rescaled = outputs[i][:, :, 0]
            if is_rescale:
                rescaled = rescaled - np.min(rescaled)
                rescaled = rescaled / np.max(rescaled)
            imgs.append(plasma(rescaled)[:, :, :3])
        else:
            imgs.append(to_multichannel(outputs[i]))

        img_set = np.hstack(imgs)
        all_images.append(img_set)

    all_images = np.stack(all_images)

    return skimage.util.montage(all_images, multichannel=True, fill=(0, 0, 0))


def save_images(filename, outputs, inputs=None, gt=None, is_colormap=True, is_rescale=False):
    montage = display_images(outputs, inputs, is_colormap, is_rescale)
    im = Image.fromarray(np.uint8(montage*255))
    im.save(filename)


def resize(path, width, height):
    """Takes an image and resizes it with given width & height"""
    imageFile = path
    img = cv2.imread(imageFile)
    dim = (width, height)
    img = cv2.resize(img, dim)
    cv2.imwrite(path, img)
