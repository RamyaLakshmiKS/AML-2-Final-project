# Floor Plan Analysis ML Project

This project analyzes floor plan data to predict property values using machine learning.

## Dataset
- Source: Kaggle ResPlan dataset
- Contains 17,000 annotated floor plans with room polygons and areas

## Setup
1. Create virtual environment: `python -m venv aml2`
2. Activate: `source aml2/bin/activate`
3. Install dependencies: `pip install -r requirements.txt`

## Notebooks
- `notebooks/download_dataset.ipynb`: Downloads the dataset
- `notebooks/eda_resplan.ipynb`: Exploratory data analysis
- `notebooks/feature_extraction_modeling.ipynb`: Feature extraction and ML model

## UI Demo
Run the demo UI: `cd ui && python app.py`
- Inputs: Total rooms, total area, average room area
- Output: Predicted property area

## Model
- Random Forest Regressor
- Features: Total rooms, total area, average room area
- R² Score: ~0.43