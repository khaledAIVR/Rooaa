import base64
import os
from contextlib import suppress


def decode_image_base64(data):
    """
    Returns decoded base64 image if successful, else returns None.

    :param data: base64 string
    """
    try:

        # Removing header that is encoded at the beginning of the data
        _, encoded = data.split(",", 1)

        img = base64.b64decode(encoded)

    # Incorrect encoding format received
    except base64.binascii.Error:
        pass
    # Exception thrown when spliting header fails
    except ValueError:
        pass
    else:
        return img


def save_image(path, binary_data, filename):
    """
    Creates given path directory if it doesn't exist and saves image,
    raises OSError if it isn't able to save image or create directory.

    :param path: path to save image to.
    :param binary_data: image data in bytes.
    :param filename: image file name that is going to be saved
    """
    with suppress(OSError):
        os.makedirs(path)

    with open(os.path.join(path, filename), "wb") as img:
        with suppress(FileExistsError):
            img.write(binary_data)
