# Iris Garden - Flower Species Predictor

A multipage Streamlit app for the Iris project (Decision Tree). Predicts Setosa, Versicolor or Virginica
from four flower measurements.

## Run locally (VS Code terminal / cmd)
```
cd iris-flower-app
python -m venv venv
venv\Scripts\activate          (Mac/Linux: source venv/bin/activate)
pip install -r requirements.txt
streamlit run app.py
```

## Deploy on Streamlit Community Cloud
1. Push this folder to a GitHub repository (`app.py` must be at the repo root).
2. Go to https://share.streamlit.io and click **Create app**.
3. Pick the repository, branch `main`, main file path `app.py`, then **Deploy**.

## Folder layout
```
app.py              entry point + navigation
views/              the six pages
irisgarden/              pipeline (training/prediction), SVG flowers, theme
data/Iris.csv       dataset
model/              saved model, scaler, encoder (re-create with: python train_model.py)
notebooks/          original notebook
.streamlit/         theme config
```
If the saved model was made with a different scikit-learn version, the app silently retrains
from `data/Iris.csv` at start-up, so it keeps working.
