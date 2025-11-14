import argparse, torch, numpy as np
from PIL import Image
from src.yolo.yolov11_n import YOLOv11Nano

def infer(image_path, weights, conf_thresh=0.3):
    img = Image.open(image_path).convert("L").resize((640,640))
    arr = np.array(img).astype("float32")/255.0
    x = torch.tensor(arr[None,None,:,:]).float()
    model = YOLOv11Nano()
    model.load_state_dict(torch.load(weights, map_location="cpu"))
    model.eval()
    with torch.no_grad():
        out = model(x).squeeze(0).numpy()
    # out: [x,y,w,h,conf] normalized
    bx = out[:4].tolist()
    conf = float(out[4])
    if conf < conf_thresh:
        return None
    return bx, conf

if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--image", required=True)
    parser.add_argument("--weights", required=True)
    args=parser.parse_args()
    print(infer(args.image, args.weights))
