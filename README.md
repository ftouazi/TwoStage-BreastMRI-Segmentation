<h1>Localization-Guided Breast Tumor Segmentation in MRI</h1>

<!-- Framework overview -->
<p align="center">
  <img src="images/approach.jpg" alt="Framework Overview" width="70%">
</p>

<p>
This repository contains the implementation of a two-stage deep learning framework for breast MRI segmentation:
</p>

<ul>
  <li><strong>YOLOv11-n nano</strong> for lesion localization</li>
  <li><strong>UNet++, UNet3+, TransUNet, Attention UNet</strong> for segmentation</li>
</ul>

<hr>

<h2>🚀 Overview of the Two-Stage Pipeline</h2>

<h3>1️⃣ Lesion Localization (YOLOv11-n)</h3>
<p>YOLOv11-n detects suspicious tumor regions and generates bounding boxes.</p>

<h3>2️⃣ Region-Guided Segmentation</h3>
<p>Each detected ROI is cropped and segmented using an advanced segmentation network.</p>

<hr>

<h2>📊 Datasets</h2>

<h3>DUKE Breast MRI</h3>
<ul>
  <li>251 curated patient studies</li>
  <li>49,236 axial slices (224×224)</li>
  <li>Ground-truth tumor masks + bounding boxes</li>
</ul>

<h3>QIN Breast MRI</h3>
<ul>
  <li>Used only for external validation</li>
  <li>76,000+ DICOM images</li>
  <li>Expert-drawn tumor segmentations</li>
</ul>

<hr>

<h2>🛠️ Pre-processing Pipeline</h2>

<ol>
  <li>Extract 2D slices from NIfTI/DICOM</li>
  <li>Remove empty slices</li>
  <li>Export to PNG</li>
  <li>Resize to 224×224 pixels</li>
  <li>Normalize pixel intensities to [0,1]</li>
  <li>Extract segmentation masks</li>
  <li>Generate YOLO bounding boxes</li>
  <li>Split into train/validation/test</li>
</ol>

<hr>

<!-- TABLE STYLE (Github-compatible) -->
<style>
table {
  border-collapse: collapse;
  width: 100%;
  margin-top: 10px;
}
table th, table td {
  border: 1px solid #666;
  padding: 8px;
  text-align: center;
}
table th {
  background-color: #f0f0f0;
}
</style>

<h2>📈 Performance Comparison</h2>

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

    <tr>
      <td rowspan="4"><strong>Without Detection</strong></td>
      <td>Attention UNet</td><td>83.49</td><td>72.07</td><td>88.71</td><td>79.31</td>
    </tr>
    <tr>
      <td>TransUNet</td><td>83.92</td><td>72.65</td><td>86.65</td><td>81.66</td>
    </tr>
    <tr>
      <td>UNet++</td><td>87.73</td><td>78.36</td><td>86.40</td><td>89.31</td>
    </tr>
    <tr>
      <td><strong>UNet3+</strong></td><td><strong>88.19</strong></td><td><strong>79.70</strong></td><td><strong>91.48</strong></td><td><strong>89.57</strong></td>
    </tr>

    <tr>
      <td rowspan="4"><strong>With Detection</strong></td>
      <td>UNet3+</td><td>93.49</td><td>91.78</td><td><strong>93.49</strong></td><td>93.90</td>
    </tr>
    <tr>
      <td>Attention UNet</td><td>93.44</td><td>91.74</td><td>93.43</td><td>93.88</td>
    </tr>
    <tr>
      <td>TransUNet</td><td>93.48</td><td>91.79</td><td>93.32</td><td>94.13</td>
    </tr>
    <tr>
      <td><strong>UNet++</strong></td><td><strong>93.62</strong></td><td><strong>91.96</strong></td><td>93.43</td><td><strong>94.19</strong></td>
    </tr>

  </tbody>
</table>

<hr>

<h2>📷 Qualitative Results</h2>

<!-- DUKE -->
<h3>1️⃣ DUKE Segmentation Results</h3>
<p align="center">
  <img src="images/duke_results.png" width="75%">
</p>

<!-- YOLO IMPACT -->
<h3>2️⃣ YOLO Detection Impact</h3>
<p align="center">
  <img src="images/yolo_irM.png" width="65%">
</p>

<!-- MODEL COMPARISON -->
<h3>3️⃣ Model Comparison</h3>
<p align="center">
  <img src="images/seg_results.png" width="70%">
</p>

<!-- QIN -->
<h3>4️⃣ QIN External Validation</h3>
<p align="center">
  <img src="images/qin_results.png" width="75%">
</p>

<hr>

<h2>📜 Citation</h2>
<pre>
@article{touazi2025breastmri,
  title={Enhancing Breast Tumor Segmentation in MRI Using a Localization-Guided Deep Learning Framework},
  author={Touazi, Fayçal and Gaceb, Djamel and Benzenati, Tayeb and Arioua, Fayçal},
  year={2025}
}
</pre>

<hr>

<h2>📄 License</h2>
<p>Released under the MIT License.</p>
