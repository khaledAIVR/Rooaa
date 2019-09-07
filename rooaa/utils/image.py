import base64
import os


def decode_image_base64(data):
    "Returns decoded base64 image if successful, else returns None"
    try:

        # Removing header that is encoded at the beginning of data
        header, encoded = data.split(",", 1)

        img = base64.b64decode(encoded)

    # Incorrect encoding format received
    except ValueError:
        return
    except base64.binascii.Error:
        return
    else:
        return img


def save_image(path, binary_data, filename):
    """Creates given path directory if it doesn't exist and 
    saves image at the path with given filename and binary data.
    Raises OSError if it isn't able to save image or create directory
    """
    if not os.path.exists(path):
        os.makedirs(path)

    try:
        with open(os.path.join(path, filename), "wb") as img:
            img.write(data)
    except FileExistsError:
        pass
