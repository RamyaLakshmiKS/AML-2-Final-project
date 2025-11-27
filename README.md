# AML-2 Final Project

This repository contains two major components for floor plan analysis and 3D visualization.

---

## 🏗️ **NEW: 3D Floor Plan Converter** ⭐

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Status: Production Ready](https://img.shields.io/badge/status-production%20ready-brightgreen.svg)]()

**A production-ready web application that transforms 2D vector floor plans (JSON) into interactive 3D models (GLB format).**

### Quick Start

```bash
# Activate virtual environment
source aml2/bin/activate

# Install dependencies (if needed)
pip install trimesh mapbox-earcut

# Launch web application
cd src && python app.py
```

Visit **http://localhost:7860** in your browser.

### Features
- 🎨 Interactive 3D visualization in browser
- 📁 Simple JSON input format (wall coordinates)
- 💾 GLB export (universal 3D format)
- 🧪 Comprehensive test suite (100% passing)
- 📚 Extensive documentation

### Documentation
- **[DELIVERY_SUMMARY.md](DELIVERY_SUMMARY.md)** - Complete project overview
- **[docs/PROJECT_README.md](docs/PROJECT_README.md)** - User guide
- **[docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)** - Technical details
- **[docs/USAGE_GUIDE.md](docs/USAGE_GUIDE.md)** - How-to with examples
- **[docs/WORKFLOW_DIAGRAMS.md](docs/WORKFLOW_DIAGRAMS.md)** - Visual diagrams

### Example Usage

```python
from src.builder import HouseBuilder
import json

floor_plan = {
    "walls": [
        [[0, 0], [0, 5]],
        [[0, 5], [5, 5]],
        [[5, 5], [5, 0]],
        [[5, 0], [0, 0]]
    ]
}

builder = HouseBuilder()
scene = builder.process_floorplan(floor_plan)
builder.export_to_glb(scene, 'house.glb')
```

### Tech Stack
- **Python 3.10+** | **trimesh** | **shapely** | **gradio** | **numpy**

### Testing

```bash
# Run tests
python tests/test_builder.py

# Run demo
python examples/quickstart.py
```

---

## 📊 Floor Plan Analysis ML Project

This component analyzes floor plan data to predict property values using machine learning.

### Dataset
- Source: Kaggle ResPlan dataset
- Contains 17,000 annotated floor plans with room polygons and areas

### Setup
1. Create virtual environment: `python -m venv aml2`
2. Activate: `source aml2/bin/activate`
3. Install dependencies: `pip install -r requirements.txt`

### Notebooks
- `notebooks/download_dataset.ipynb`: Downloads the dataset
- `notebooks/eda_resplan.ipynb`: Exploratory data analysis
- `notebooks/feature_extraction_modeling.ipynb`: Feature extraction and ML model

### UI Demo
Run the demo UI: `cd ui && python app.py`
- Inputs: Total rooms, total area, average room area
- Output: Predicted property area

### Model
- Random Forest Regressor
- Features: Total rooms, total area, average room area
- R² Score: ~0.43

---

## 📁 Project Structure

```
.
├── src/                    # 3D Floor Plan Converter
│   ├── builder.py         # Core geometry engine
│   └── app.py             # Web interface
│
├── tests/                 # Test suite
│   └── test_builder.py
│
├── examples/              # Demo scripts
│   └── quickstart.py
│
├── models/                # Generated 3D models
│
├── docs/                  # Comprehensive documentation
│
├── notebooks/             # ML analysis notebooks
│
├── ui/                    # ML prediction UI
│
└── data/                  # Dataset storage
```

---

## 📄 License

MIT License

---

## 👤 Authors

**Senior Python Engineer**  
Specializing in Computational Geometry, 3D Visualization, and Machine Learning

---

**Status**: ✅ Production Ready | **Last Updated**: November 26, 2025