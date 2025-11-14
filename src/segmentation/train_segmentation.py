import argparse, os, torch
from torch.utils.data import DataLoader, Dataset
from torchvision import transforms
import segmentation_models_pytorch as smp
from src.segmentation.models import get_seg_model
from PIL import Image
import numpy as np

class SimpleSegDataset(Dataset):
    def __init__(self, images_folder, masks_folder, transform=None):
        self.images = sorted([os.path.join(images_folder,f) for f in os.listdir(images_folder) if f.endswith(".png")])
        self.masks = sorted([os.path.join(masks_folder,f) for f in os.listdir(masks_folder) if f.endswith(".png")])
        self.transform = transform

    def __len__(self): return len(self.images)
    def __getitem__(self, idx):
        img = Image.open(self.images[idx]).convert("L").resize((224,224))
        mask = Image.open(self.masks[idx]).convert("L").resize((224,224))
        img = np.array(img).astype("float32")/255.0
        mask = (np.array(mask)>127).astype("float32")
        img = img[None,:,:]
        mask = mask[None,:,:]
        return torch.tensor(img).float(), torch.tensor(mask).float()

def train(args):
    ds = SimpleSegDataset(args.images, args.masks)
    dl = DataLoader(ds, batch_size= args.batch_size, shuffle=True)
    model = get_seg_model(name=args.model, encoder_name=args.encoder)
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model.to(device)
    loss_fn = smp.utils.losses.DiceLoss()
    opt = torch.optim.Adam(model.parameters(), lr=args.lr)
    for epoch in range(args.epochs):
        model.train()
        total=0.0
        for imgs, masks in dl:
            imgs=imgs.to(device); masks=masks.to(device)
            preds = model(imgs)
            loss = loss_fn(preds, masks)
            opt.zero_grad(); loss.backward(); opt.step()
            total+=loss.item()
        print(f"Epoch {epoch} loss {total/len(dl):.4f}")
    torch.save(model.state_dict(), args.weights)

if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--images", required=True)
    parser.add_argument("--masks", required=True)
    parser.add_argument("--model", default="unetplusplus")
    parser.add_argument("--encoder", default="resnet34")
    parser.add_argument("--weights", default="seg.pth")
    parser.add_argument("--batch_size", type=int, default=8)
    parser.add_argument("--epochs", type=int, default=25)
    parser.add_argument("--lr", type=float, default=1e-4)
    args=parser.parse_args()
    train(args)
