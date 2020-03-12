import pickle

import cv2

# danger_dictionary takes the label index as a key and the value is the estimated danger value
danger_dict = {'person': 9, 'bicycle': 8, 'car': 10, 'motorbike': 9, 'aeroplane': 0, 'bus': 10, 'train': 0, 'truck': 10, 'boat': 0, 'traffic light': 10, 'fire hydrant': 0, 'stop sign': 10, 'parking meter': 8, 'bench': 6, 'bird': 4, 'cat': 4, 'dog': 5, 'horse': 0, 'sheep': 0, 'cow': 0, 'elephant': 0, 'bear': 0, 'zebra': 0, 'giraffe': 0, 'backpack': 0, 'umbrella': 0, 'handbag': 0, 'tie': 0, 'suitcase': 0, 'frisbee': 0, 'skis': 0, 'snowboard': 5, 'sports ball': 7, 'kite': 0, 'baseball bat': 7, 'baseball glove': 0, 'skateboard': 7, 'surfboard': 0, 'tennis racket': 0,
               'bottle': 0, 'wine glass': 0, 'cup': 0, 'fork': 0, 'knife': 0, 'spoon': 0, 'bowl': 0, 'banana': 0, 'apple': 0, 'sandwich': 0, 'orange': 0, 'broccoli': 0, 'carrot': 0, 'hot dog': 0, 'pizza': 0, 'donut': 0, 'cake': 0, 'chair': 8, 'sofa': 8, 'pottedplant': 8, 'bed': 8, 'diningtable': 8, 'toilet': 8, 'tvmonitor': 5, 'laptop': 0, 'mouse': 0, 'remote': 0, 'keyboard': 0, 'cell phone': 5, 'microwave': 7, 'oven': 7, 'toaster': 0, 'sink': 7, 'refrigerator': 6, 'book': 0, 'clock': 0, 'vase': 5, 'scissors': 0, 'teddy bear': 0, 'hair drier': 0, 'toothbrush': 0}


class filtration:
    def __init__(self, label, location, depth):
        self.label = label
        self.location = location
        self.depth = depth

    def __str__(self):
        return f"{self.location} {self.label} "


def filter_results(pkl_path, dense_path):
    with open(pkl_path, "rb") as f:
        yolo_data = pickle.load(f)
        filtered_text = "Nothing"

        if yolo_data is not None:
            filtered_text = sort_by_most_dangerous(dense_path, *yolo_data)
    return filtered_text


def sort_by_most_dangerous(dense_path, classes, locations, centers):
    depthes = depth_approx(dense_path=dense_path, centers=centers)

    filtration_arr = [filtration(c, l, d)
                      for c, l, d in zip(classes, locations, depthes)]
    # ---------------------------------
    warning_area = []
    informing_area = []
    for i in filtration_arr:
        if i.depth <= 35:
            warning_area.append(i)
        else:
            informing_area.append(i)
    # ---------------------------------
    area = warning_area if len(warning_area) > 0 else informing_area

    left_objs = []
    right_objs = []
    center_objs = []
    for i in area:
        if i.location == 'center':
            center_objs.append(i)
        elif i.location == 'left':
            left_objs.append(i)
        elif i.location == 'right':
            right_objs.append(i)

    most_dangerous_center = most_dangerous(arr=center_objs)
    most_dangerous_left = most_dangerous(arr=left_objs)
    most_dangerous_right = most_dangerous(arr=right_objs)

    texts = "Watch out " if area == warning_area else ""
    if most_dangerous_center != -1:
        texts += str(most_dangerous_center)

    if most_dangerous_left != -1:
        texts += str(most_dangerous_left)

    if most_dangerous_right != -1:
        texts += str(most_dangerous_right)

    return texts


def depth_approx(dense_path, centers):
    img = cv2.imread(dense_path)
    return [img[x, y][0] for x, y in centers]


def most_dangerous(arr):
    return max(arr, default=-1, key=lambda f: danger_dict[f.label])
