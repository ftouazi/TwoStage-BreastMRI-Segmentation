import argparse, os, torch
from torch.utils.data import DataLoader, Dataset
from torchvision import transforms
from src.yolo.yolov11_n import YOLOv11Nano

class SimpleYoloDataset(Dataset):
    def __init__(self, images_folder, labels_folder, transform=None):
        self.images = sorted([os.path.join(images_folder,f) for f in os.listdir(images_folder) if f.endswith(".png")])
        self.labels = sorted([os.path.join(labels_folder,f) for f in os.listdir(labels_folder) if f.endswith(".txt")])
        self.transform = transform

    def __len__(self): return len(self.images)
    def __getitem__(self, idx):
        from PIL import Image
        import numpy as np
        img = Image.open(self.images[idx]).convert("L")
        img = img.resize((640,640))
        img = np.array(img).astype("float32")/255.0
        img = img[None,:,:] # CxHxW
        # read label (x_center y_center w h)
        with open(self.labels[idx],"r") as f:
            line = f.readline().strip().split()
        y = torch.tensor([float(x) for x in line[1:5]]).float()
        return torch.tensor(img).float(), y

def train(args):
    ds = SimpleYoloDataset(args.images, args.labels)
    dl = DataLoader(ds, batch_size=8, shuffle=True)
    model = YOLOv11Nano()
    opt = torch.optim.Adam(model.parameters(), lr=1e-4)
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model.to(device)
    for epoch in range(args.epochs):
        model.train()
        total_loss=0.0
        for imgs, targets in dl:
            imgs=imgs.to(device); targets=targets.to(device)
            preds = model(imgs)
            # simple MSE loss on bbox coords
            loss = torch.nn.functional.mse_loss(preds[:,:4], targets[:,:4])
            opt.zero_grad(); loss.backward(); opt.step()
            total_loss+=loss.item()
        print(f"Epoch {epoch} loss {total_loss/len(dl):.4f}")
    torch.save(model.state_dict(), args.weights)

if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--images", required=True)
    parser.add_argument("--labels", required=True)
    parser.add_argument("--weights", default="yolov11n.pth")
    parser.add_argument("--epochs", type=int, default=50)
    args=parser.parse_args()
    train(args)
