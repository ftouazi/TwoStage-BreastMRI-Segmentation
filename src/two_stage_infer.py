import argparse, json, os
from src.yolo.infer_yolo import infer as yolo_infer
from src.segmentation.infer_segmentation import infer as seg_infer
from PIL import Image
import numpy as np

def two_stage(image_path, yolo_weights, seg_weights, out_path="two_stage_out.png"):
    # 1) run detector on full image
    det = yolo_infer(image_path, yolo_weights)
    if det is None:
        print("No detection")
        return None
    bbox_norm, conf = det
    # bbox_norm = [x_center,y_center,w,h] normalized on 640x640
    img = Image.open(image_path).convert("L").resize((640,640))
    w,h = img.size
    xc,yc,ww,hh = bbox_norm
    xmin = int((xc - ww/2.0)*w); ymin = int((yc - hh/2.0)*h)
    xmax = int((xc + ww/2.0)*w); ymax = int((yc + hh/2.0)*h)
    # crop and save temp
    crop = img.crop((xmin,ymin,xmax,ymax)).resize((224,224))
    crop.save("temp_crop.png")
    # 2) run segmentation on crop
    mask = seg_infer("temp_crop.png", seg_weights)
    # 3) paste mask back to original for visualization
    full = Image.open(image_path).convert("RGB").resize((640,640))
    mask_img = Image.fromarray(mask).convert("L").resize((xmax-xmin, ymax-ymin))
    overlay = full.copy()
    overlay.paste(Image.fromarray(np.zeros((1,1),dtype=np.uint8)), (0,0))
    # simple overlay: paste mask as red channel on cropped area
    r,g,b = overlay.split()
    mask_color = Image.new("RGB", overlay.size)
    mask_full = Image.new("L", overlay.size)
    mask_full.paste(mask_img, (xmin,ymin))
    # tint overlay red where mask==255
    overlay_np = np.array(overlay)
    mask_np = np.array(mask_full)
    overlay_np[mask_np==255] = [255,0,0]
    Image.fromarray(overlay_np).save(out_path)
    print("Saved", out_path)

if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--image", required=True)
    parser.add_argument("--yolo_weights", required=True)
    parser.add_argument("--seg_weights", required=True)
    parser.add_argument("--out", default="two_stage_out.png")
    args=parser.parse_args()
    two_stage(args.image, args.yolo_weights, args.seg_weights, args.out)
