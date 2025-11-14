# Localization-Guided Breast Tumor Segmentation in MRI

![Framework Overview](images/approach.jpg)

This repository contains the official implementation of the two-stage deep learning framework described in the manuscript:

**“Enhancing Breast Tumor Segmentation in MRI Using a Localization-Guided Deep Learning Framework”**

The project introduces a hybrid pipeline that combines:

- **Tumor localization** using YOLOv11-n-nano (2M params)  
- **Region-guided semantic segmentation** using UNet++, UNet3+, Attention UNet, and TransUNet  

to improve breast lesion segmentation in MRI scans.

---

## 🚀 Overview of the Two-Stage Pipeline

### **1. Lesion Localization (YOLOv11-n)**
A lightweight detector identifies suspicious regions on MRI slices and produces bounding boxes.

### **2. Region-Guided Segmentation**
The detected ROI is cropped and passed to a segmentation network:

- UNet++  
- UNet3+  
- Attention UNet  
- TransUNet  

This “focus-on-lesion” strategy reduces false positives and improves boundary accuracy.

---

# 📊 Datasets

### **DUKE Breast MRI (MAMA-MIA subset)**
- 922 patients → curated 251 cases  
- 3D DCE-MRI volumes (.nii.gz)  
- Converted to **49,236 2D slices (224×224)**  
- Includes binary segmentation masks + bounding boxes  

### **QIN Breast MRI (TCIA)**
Used only for **external validation**:  
- 10 patients × 2 studies  
- 76,000+ DICOM images  
- Expert-drawn masks provided  

---

# 🛠️ Pre-processing Pipeline

For both DUKE and QIN datasets:

1. Extract 2D slices from 3D DICOM/NIfTI volumes  
2. Remove empty slices  
3. Convert to PNG  
4. Resize to **224×224**  
5. Normalize intensities to **[0,1]**  
6. Extract segmentation masks  
7. Generate bounding boxes for YOLO  
8. Train / validation / test split

---

# 📈 Results

# 📷 Qualitative Results

## 1️⃣ DUKE Breast MRI – Segmentation Results
Below are visual examples comparing:

- **(a)** Ground Truth  
- **(b)** Predicted Mask  
- **(c)** Overlay (Prediction + Ground Truth)

![DUKE Segmentation Results](images/duke_results.png)

---

## 2️⃣ Impact of YOLO Detection Before Segmentation

Left: segmentation **without** detection  
Right: segmentation **with YOLOv11-n detection**

![YOLO Detection Comparison](images/yolo_detection.png)

---

## 3️⃣ Comparison with Various Segmentation Architectures  
Example using ultrasound (UNet++, TransUNet, DeepLabv3+, etc.)  
(*used to show robustness of architectures*)

![Segmentation Model Comparison](images/ultrasound_comparison.png)

---

## 4️⃣ QIN External Validation – Segmentation Results  
The Duke-trained UNet++ model generalizes strongly on the QIN dataset.

- **(a)** Ground Truth  
- **(b)** Predicted Mask  
- **(c)** Overlay  

![QIN Segmentation Results](images/qin_results.png)

