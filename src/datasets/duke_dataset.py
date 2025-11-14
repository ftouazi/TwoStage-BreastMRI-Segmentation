import os
from PIL import Image
from torch.utils.data import Dataset
import numpy as np

class DukeDataset(Dataset):
    def __init__(self, root, transform=None):
        self.img_dir = os.path.join(root, "images")
        self.mask_dir = os.path.join(root, "masks")
        self.files = sorted([f for f in os.listdir(self.img_dir) if f.endswith(".png")])
        self.transform = transform

    def __len__(self):
        return len(self.files)

    def __getitem__(self, idx):
        img_name = self.files[idx]
        img = Image.open(os.path.join(self.img_dir, img_name)).convert("L")
        mask = Image.open(os.path.join(self.mask_dir, img_name)).convert("L")
        img = np.array(img).astype("float32")/255.0
        mask = (np.array(mask)>127).astype("float32")
        img = img[None,:,:]
        mask = mask[None,:,:]
        return img, mask
