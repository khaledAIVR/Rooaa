import os


def create_image_directory(upload_path):
    """ Creates image upload directory if it doesn't exist """
    try:
        os.makedirs(upload_path)
    except FileExistsError:
        pass
    except OSError as err:
        print(f"{err}")


def save_image(path, data, filename):
    """ Saves image at a given path with given filename and data """
    try:
        with open(os.path.join(path, filename), "wb") as img:
            img.write(data)
    except FileExistsError:
        pass
    except OSError as err:
        print(f"{err}")
