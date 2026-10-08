import streamlit as st

from irisgarden.store import get_bundle
from irisgarden.theme import html, page_header

bundle = get_bundle()
page_header("About this project", "A small machine learning project, from notebook to web app.")

st.markdown("""
#### The data
The Iris dataset holds 150 flowers, 50 from each of three species. It was collected by the botanist Edgar Anderson
and made famous by the statistician Ronald Fisher in 1936. Every flower has four measurements: sepal length, sepal width,
petal length and petal width.

#### The model
The notebook compared six models. The final model is a **Decision Tree** tuned with grid search
(Gini criterion, minimum 4 samples per leaf). Before training, the features were standardised and the training
set was balanced with SMOTE.

#### The pipeline in this app
1. Clean the CSV and encode the three species as 0, 1, 2
2. Split 80% training and 20% testing
3. Standardise the four measurements
4. Balance the training classes
5. Train the tuned decision tree
""")
html(f'<div class="note">Model source in this session: {bundle["source"]}.</div>')
st.markdown("""
#### Built with
Streamlit for the interface, scikit-learn for the model, Plotly for the charts, and hand-drawn SVG irises.
""")
