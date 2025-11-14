import os
import pydicom
import json
import numpy as np
from PIL import Image
import nibabel as nib
from src.utils.utils import mask_to_bbox, ensure_dirs

def extract_bbox(mask_np):
    ys, xs = np.where(mask_np > 0)
    if len(xs) == 0:
        return None
    return {
        "xmin": int(xs.min()),
        "ymin": int(ys.min()),
        "xmax": int(xs.max()),
        "ymax": int(ys.max())
    }

def preprocess_qin(dicom_dir, mask_file, output_dir, img_size=224):
    ensure_dirs(os.path.join(output_dir, "images"))
    ensure_dirs(os.path.join(output_dir, "masks"))
    ensure_dirs(os.path.join(output_dir, "bboxes"))

    dicom_files = sorted([os.path.join(dicom_dir, f) for f in os.listdir(dicom_dir) if f.lower().endswith(".dcm")])
    mask_nii = nib.load(mask_file).get_fdata()

    for i, dc_path in enumerate(dicom_files):
        try:
            ds = pydicom.dcmread(dc_path)
        except Exception as e:
            continue

        img = ds.pixel_array.astype(np.float32)
        img = (img - img.min()) / (img.max() - img.min() + 1e-8)

        if i >= mask_nii.shape[2]:
            break

        mask_slice = (mask_nii[:, :, i] > 0).astype(np.uint8)

        img_pil = Image.fromarray((img * 255).astype(np.uint8))
        mask_pil = Image.fromarray(mask_slice * 255)

        img_pil = img_pil.resize((img_size, img_size))
        mask_pil = mask_pil.resize((img_size, img_size))

        img_pil.save(os.path.join(output_dir, "images", f"{i}.png"))
        mask_pil.save(os.path.join(output_dir, "masks", f"{i}.png"))

        bbox = extract_bbox(np.array(mask_pil))

        with open(os.path.join(output_dir, "bboxes", f"{i}.json"), "w") as fp:
            json.dump(bbox, fp)

    print("QIN preprocessing completed!")