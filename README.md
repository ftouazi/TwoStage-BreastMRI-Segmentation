<h1>Localization-Guided Breast Tumor Segmentation in MRI</h1>

<!-- Framework overview -->
<p align="center">
  <img src="images/approach.jpg" alt="Framework Overview" width="70%">
</p>

<p>
This repository contains the implementation of a two-stage deep learning pipeline for breast MRI segmentation, combining:
</p>

<ul>
  <li><strong>YOLOv11-n nano</strong> for tumor localization</li>
  <li><strong>UNet++, UNet3+, TransUNet, Attention UNet</strong> for semantic segmentation</li>
</ul>

<hr>

<h2>🚀 Overview of the Two-Stage Pipeline</h2>

<h3>1️⃣ Lesion Localization (YOLOv11-n)</h3>
<p>A lightweight YOLOv11-n model detects suspicious tumor regions on MRI slices.</p>

<h3>2️⃣ Region-Guided Segmentation</h3>
<p>
Each detected region-of-interest is extracted and segmented using an advanced segmentation model.
This improves precision and reduces false positives.
</p>

<hr>

<h2>📊 Datasets</h2>

<h3>DUKE Breast MRI Dataset</h3>
<ul>
  <li>251 curated patient studies</li>
  <li>49,236 axial slices (224×224)</li>
  <li>Pixel-level segmentation masks + YOLO bounding boxes</li>
</ul>

<h3>QIN Breast MRI (TCIA)</h3>
<ul>
  <li>Used exclusively for external validation</li>
  <li>76,000+ DICOM images</li>
  <li>Expert-annotated tumor masks</li>
</ul>

<hr>

<h2>🛠️ Pre-processing Pipeline</h2>

<ol>
  <li>Extract 2D slices from DICOM/NIfTI volumes</li>
  <li>Remove empty slices</li>
  <li>Resize to <strong>224×224</strong></li>
  <li>Normalize intensity to <strong>[0,1]</strong></li>
  <li>Extract segmentation masks</li>
  <li>Generate YOLOv11-n bounding boxes</li>
  <li>Split into train / validation / test sets</li>
</ol>

<hr>

<h2>📈 Performance Comparison</h2>

<p>
The table below compares segmentation models trained directly vs. trained with YOLO-based localization.
</p>

<table>
  <thead>
    <tr>
      <th>Approach</th>
      <th>Model</th>
      <th>DSC (%)</th>
      <th>IoU (%)</th>
      <th>Precision (%)</th>
      <th>Recall (%)</th>
    </tr>
  </thead>
  <tbody>

    <!-- WITHOUT DETECTION -->
    <tr>
      <td><strong>Without Detection</strong></td>
      <td>Attention UNet</td><td>83.49</td><td>72.07</td><td>88.71</td><td>79.31</td>
    </tr>
    <tr>
      <td><strong>Without Detection</strong></td>
      <td>TransUNet</td><td>83.92</td><td>72.65</td><td>86.65</td><td>81.66</td>
    </tr>
    <tr>
      <td><strong>Without Detection</strong></td>
      <td>UNet++</td><td>87.73</td><td>78.36</td><td>86.40</td><td>89.31</td>
    </tr>
    <tr>
      <td><strong>Without Detection</strong></td>
      <td><strong>UNet3+</strong></td>
      <td><strong>88.19</strong></td><td><strong>79.70</strong></td>
      <td><strong>91.48</strong></td><td><strong>89.57</strong></td>
    </tr>

    <!-- WITH DETECTION -->
    <tr>
      <td><strong>With Detection</strong></td>
      <td>UNet3+</td>
      <td>93.49</td><td>91.78</td><td><strong>93.49</strong></td><td>93.90</td>
    </tr>
    <tr>
      <td><strong>With Detection</strong></td>
      <td>Attention UNet</td>
      <td>93.44</td><td>91.74</td><td>93.43</td><td>93.88</td>
    </tr>
    <tr>
      <td><strong>With Detection</strong></td>
      <td>TransUNet</td>
      <td>93.48</td><td>91.79</td><td>93.32</td><td>94.13</td>
    </tr>
    <tr>
      <td><strong>With Detection</strong></td>
      <td><strong>UNet++</strong></td>
      <td><strong>93.62</strong></td><td><strong>91.96</strong></td>
      <td>93.43</td><td><strong>94.19</strong></td>
    </tr>

  </tbody>
</table>

<hr>

<h2>📷 Qualitative Results</h2>

<h3>1️⃣ DUKE Segmentation Results</h3>
<p align="center">
  <img src="images/aff_duke2.png" width="60%">
</p>

<h3>2️⃣ YOLO Detection vs. No Detection</h3>
<p align="center">
  <img src="images/yolo_irM.png" width="45%">
</p>

<h3>3️⃣ Comparison Across Segmentation Models</h3>
<p align="center">
  <img src="images/résultats de seg.png" width="65%">
</p>

<h3>4️⃣ QIN External Validation</h3>
<p align="center">
  <img src="images/QIN_affi (1).png" width="60%">
</p>

<hr>

<h2>📜 Citation</h2>

<pre>
@article{touazi2025breastmri,
  title={Enhancing Breast Tumor Segmentation in MRI Using a Localization-Guided Deep Learning Framework},
  author={Touazi, Fayçal and Gaceb, Djamel and Benzenati, Tayeb et a
