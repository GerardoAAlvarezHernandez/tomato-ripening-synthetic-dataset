# Synthetic Dataset Generation for Tomato Ripening Stage Detection in Different Scenes

**Journal:** IEEE Latin America Transactions  
**Manuscript ID:** 10390   

**Authors:**
- Gerardo A. Álvarez-Hernández — Centro de Innovación y Desarrollo Tecnológico en Cómputo (CIDETEC), 
Instituto Politécnico Nacional, Mexico City, Mexico (galvarezh1400@alumno.ipn.mx)
- Juan Irving Vasquez Gomez — Centro de Innovación y Desarrollo Tecnológico en Cómputo (CIDETEC), 
Instituto Politécnico Nacional, Mexico City, Mexico
- Abril Valeria Uriarte Arcia — Centro de Innovación y Desarrollo Tecnológico en Cómputo (CIDETEC), 
Instituto Politécnico Nacional, Mexico City, Mexico
- Luis Alberto Tovar Ortiz — Centro de Innovación y Desarrollo Tecnológico en Cómputo (CIDETEC), 
Instituto Politécnico Nacional, Mexico City, Mexico

---

## 📄 Description

This repository contains all scripts required to reproduce the results presented in the paper:

> *"Synthetic Dataset Generation for Tomato Ripening Stage Detection in Different Scenes"*  
> IEEE Latin America Transactions, 2026

We propose a pipeline for generating synthetic greenhouse image datasets using a **genetic algorithm**, **background substitution**, and **leaf occlusion**. The generated dataset is used to train a YOLOv5-based detector for tomato ripening stage classification according to the Mexican standard **NMX-FF-031-1997**, which defines 6 ripening stages.

---

## 📁 Included Scripts

All scripts are located in the `src/` directory. The table below maps each script to the corresponding figures and results in the paper.

| Script | Figure(s) in Paper | Description |
|--------|--------------------|-------------|
| `src/augmentation.py` | Fig. 2 | Genetic algorithm-based synthetic image generation. Applies background substitution and leaf occlusion to produce augmented training images. |
| `src/train.py` | Fig. 2 | Trains a YOLOv5 detection model on the synthetic augmented dataset. |
| `src/evaluate.py` | Fig. 3 | Evaluates the trained model on the test split and reports Precision, Recall, and mAP metrics. |

> **Note:** If the script names in your local clone differ from the table above (e.g., `argumentation1_1.py`), please refer to the docstring at the top of each file to identify its purpose.

---

## 📂 Dataset

The base dataset (3,000 images with 6 ripening stages and segmentation masks) is publicly available on Kaggle:

🔗 [Dataset for Tomatoes — Kaggle](https://www.kaggle.com/datasets/gerardoantony/dataset-for-tomatoes-to-use-for-augmentation)

### Ripening Stages (NMX-FF-031-1997)

| Stage | Label | Description |
|-------|-------|-------------|
| 1 | `Green` | Completely green surface |
| 2 | `Broken` | Predominantly green with slight color change |
| 3 | `Salmon` | Green and red/yellow equally distributed |
| 4 | `Orange` | Predominantly red/yellow |
| 5 | `Orange-red` | Surface mostly red/yellow |
| 6 | `Red` | Fully red, ready for harvest |

### Expected Directory Structure

After downloading the dataset from Kaggle, when you run aumentatio_1.py, generate the dataset as follows:

```
data/
├── images/
│   ├── train/          # Training images
│   └── val/            # Validation images
├── labels/
│   ├── train/          # YOLO-format annotation files (.txt)
│   └── val/
```

The `data/` folder also contains:

| File | Description |
|------|-------------|
| `data/tomates.yaml` | YOLOv5 dataset configuration file (class names, paths) |

The `model/` folder contains:

| File | Description |
|------|-------------|
| `model/weights.pt` | Pre-trained model weights |

---

## 💻 Requirements

- Python 3.8 or later
- pip 21.0 or later
- CUDA 11.x compatible GPU (optional but recommended for training)
- No additional MATLAB or proprietary toolboxes required

### Python Dependencies

All dependencies are listed in `requirements.txt` (based on YOLOv5):

```
torch>=1.8.0
torchvision>=0.9.0
ultralytics>=8.0.232
opencv-python>=4.1.1
numpy>=1.23.5
Pillow>=10.0.1
matplotlib>=3.3
PyYAML>=5.3.1
tqdm>=4.64.0
scipy>=1.4.1
pandas>=1.1.4
seaborn>=0.11.0
```

---

## 🔧 Installation

```bash
# 1. Clone the repository
git clone https://github.com/GerardoAAlvarezHernandez/tomato-ripening-synthetic-dataset.git
cd tomato-ripening-synthetic-dataset

# 2. Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate        # Linux / macOS
# venv\Scripts\activate         # Windows

# 3. Install dependencies
pip install -r requirements.txt
```

---

## 🚀 Usage

### Step 1 — Generate the synthetic dataset

Run the genetic algorithm to produce augmented images with background substitution and leaf occlusion:

```bash
python src/augmentation.py \
    --input  data/images/ \
    --masks  data/masks/ \
    --backgrounds data/backgrounds/ \
    --output data/augmented/ \
    --generations 50 \
    --pop_size 30
```

Expected output: the `data/augmented/` folder will be populated with synthetic images and their corresponding YOLO-format label files.

### Step 2 — Train the detection model

Train YOLOv5 on the generated synthetic dataset:

```bash
python src/train.py \
    --weights model/weights.pt \
    --data    data/tomates.yaml \
    --epochs  100 \
    --batch   16 \
    --imgsz   640
```

### Step 3 — Evaluate the model

Evaluate the trained model on the validation split and generate result metrics:

```bash
python src/evaluate.py \
    --weights runs/train/exp/weights/best.pt \
    --data    data/tomates.yaml \
    --imgsz   640
```

Results (Precision, Recall, mAP@0.5, mAP@0.5:0.95) will be printed to stdout and saved in `runs/val/`.

---

## 📊 Results

The following table reproduces the main detection results reported in the paper (Table III):

| Ripening Stage | Precision | Recall | mAP@0.5 |
|----------------|-----------|--------|---------|
| Green          |     0.498 |  0.266 |   0.249 | 
| Broken         |    0.0649 | 0.214  | 0.0999  |
| Salmon         |    0.0439 |  0.0952| 0.0263  |
| Orange         | 0         | 0      | 0.0165  | 
| Orange-red     | 0.418     | 0.261  | 0.364   | 
| Red            | 0.0902    | 0.0345 | 0.033   | 
| **Mean (all)** | **0.186** | **0.145** | **0.131** | 

> All results were obtained using the model trained exclusively on the synthetic dataset generated by the proposed pipeline.

---

## 📖 Citation

If you use this code or dataset in your research, please cite:

```bibtex
@article{alvarez2025tomato,
  author  = {Álvarez-Hernández, Gerardo A. and Vasquez-Gomez,J. Irving and Uriarte-Arcia, Abril Valeria and Tovar-Ortiz, Luis Alberto},
  title   = {Synthetic Dataset Generation for Tomato Ripening Stage Detection in Different Scenes},
  journal = {IEEE Latin America Transactions},
  year    = {2026}
}
```

---

## 📋 Required Files Summary

| File | Required by | Notes |
|------|-------------|-------|
| `data/tomates.yaml` | `train.py`, `evaluate.py` | Dataset config for YOLOv5 |
| `data/masks/` | `augmentation.py` | Segmentation masks per image |
| `data/backgrounds/` | `augmentation.py` | Alternative background scenes |
| `model/weights.pt` | `train.py` | Pre-trained base weights |

---

## ✉️ Contact

For questions about this code or requests to reproduce the results:

**Gerardo A. Álvarez-Hernández**  
Centro de Innovación y Desarrollo Tecnológico en Cómputo (CIDETEC), 
Instituto Politécnico Nacional, Mexico City, Mexico  
📧 galvarezh1400@alumno.ipn.mx

---

## License

This project is released under the [MIT License](LICENSE) for the code.  
The dataset hosted on Kaggle is subject to its own terms of use.
