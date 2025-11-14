import os, json
from PIL import Image
import numpy as np

def mask_to_bbox(mask_np, pad=0):
    ys, xs = np.where(mask_np > 0)
    if len(xs)==0:
        return None
    xmin = int(xs.min()) - pad
    ymin = int(ys.min()) - pad
    xmax = int(xs.max()) + pad
    ymax = int(ys.max()) + pad
    return [xmin, ymin, xmax, ymax]

def bbox_to_yolo(bbox, img_w, img_h):
    # bbox = [xmin, ymin, xmax, ymax]
    xmin, ymin, xmax, ymax = bbox
    x_center = (xmin + xmax) / 2.0 / img_w
    y_center = (ymin + ymax) / 2.0 / img_h
    w = (xmax - xmin) / img_w
    h = (ymax - ymin) / img_h
    return [x_center, y_center, w, h]

def save_yolo_label(yolo_bbox, out_path, class_id=0):
    # yolo_bbox: [x_center, y_center, w, h] normalized
    with open(out_path, "w") as f:
        f.write(f"{class_id} " + " ".join([f"{x:.6f}" for x in yolo_bbox]) + "\\n")

def ensure_dirs(path):
    os.makedirs(path, exist_ok=True)

def split_list(lst, ratios=(0.7,0.1,0.2)):
    assert sum(ratios)==1.0
    n = len(lst)
    import math
    t = math.floor(n*ratios[0])
    v = math.floor(n*ratios[1])
    return lst[:t], lst[t:t+v], lst[t+v:]
