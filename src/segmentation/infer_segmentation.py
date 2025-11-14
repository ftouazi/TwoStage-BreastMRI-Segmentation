import argparse, torch, numpy as np
from PIL import Image
from src.segmentation.models import get_seg_model

def infer(image_path, weights, model_name="unetplusplus", encoder="resnet34"):
    img = Image.open(image_path).convert("L").resize((224,224))
    arr = np.array(img).astype("float32")/255.0
    x = torch.tensor(arr[None,None,:,:]).float()
    model = get_seg_model(name=model_name, encoder_name=encoder)
    model.load_state_dict(torch.load(weights, map_location="cpu"))
    model.eval()
    with torch.no_grad():
        out = model(x).squeeze(0).squeeze(0).numpy()
    mask = (out > 0).astype("uint8")*255
    return mask

if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--image", required=True)
    parser.add_argument("--weights", required=True)
    args=parser.parse_args()
    m = infer(args.image, args.weights)
    from PIL import Image
    Image.fromarray(m).save("pred_mask.png")
    print("Saved pred_mask.png")
