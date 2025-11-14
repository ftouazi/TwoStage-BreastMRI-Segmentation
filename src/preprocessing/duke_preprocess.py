import os
import nibabel as nib
import numpy as np
from PIL import Image
import tqdm
from src.utils.utils import ensure_dirs

def preprocess_duke(input_dir, output_dir, img_size=224):
    os.makedirs(os.path.join(output_dir, "images"), exist_ok=True)
    os.makedirs(os.path.join(output_dir, "masks"), exist_ok=True)

    cases = sorted(os.listdir(input_dir))

    for case in tqdm.tqdm(cases, desc="Processing DUKE"):
        case_path = os.path.join(input_dir, case)

        # expect files named image.nii.gz and mask.nii.gz inside each case folder
        img_file = os.path.join(case_path, "image.nii.gz")
        mask_file = os.path.join(case_path, "mask.nii.gz")

        if not os.path.exists(img_file) or not os.path.exists(mask_file):
            continue

        img_nii = nib.load(img_file)
        mask_nii = nib.load(mask_file)

        img = img_nii.get_fdata()
        mask = mask_nii.get_fdata()

        # normalize per-volume
        img = (img - img.min()) / (img.max() - img.min() + 1e-8)

        # assume axial slices in last dimension
        if img.ndim==3:
            depth = img.shape[2]
            for i in range(depth):
                slice_img = img[:, :, i]
                slice_mask = mask[:, :, i]

                if slice_img.sum() == 0:
                    continue

                img_pil = Image.fromarray((slice_img * 255).astype(np.uint8))
                mask_pil = Image.fromarray((slice_mask > 0).astype(np.uint8) * 255)

                img_pil = img_pil.resize((img_size, img_size))
                mask_pil = mask_pil.resize((img_size, img_size))

                img_pil.save(os.path.join(output_dir, "images", f"{case}_{i}.png"))
                mask_pil.save(os.path.join(output_dir, "masks", f"{case}_{i}.png"))

    print("DUKE preprocessing completed!")