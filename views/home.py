import streamlit as st

from irisgarden.flowers import garden_svg
from irisgarden.store import get_bundle, get_plot_data
from irisgarden.theme import html, plate

df = get_plot_data()
bundle = get_bundle()
acc = bundle["metrics"]["accuracy"] * 100
n_test = bundle["metrics"]["n_test"]

html(f"""
<div class="hero">
  <div>
    <div class="hero-title">Three irises.<br>One decision tree.</div>
    <div class="hero-sub">Measure the petals and sepals of an iris, and the model tells you
    which of the three species is in your hand.</div>
    <div class="hero-note">Trained on {len(df)} measured flowers &middot; {acc:.0f}% accuracy on {n_test} flowers it had never seen</div>
  </div>
  <div class="hero-art">{garden_svg()}</div>
</div>
""")

st.page_link("views/predict.py", label="Identify a flower", icon="🌷")

st.markdown("### Meet the three irises")
means = df.groupby("Species")[["SepalLengthCm", "SepalWidthCm", "PetalLengthCm", "PetalWidthCm"]].mean()
cols = st.columns(3, gap="large")
for i, (col, name) in enumerate(zip(cols, ["Setosa", "Versicolor", "Virginica"])):
    m = means.loc[name]
    facts = (f'<div class="plate-facts"><div><b>{m.PetalLengthCm:.1f} cm</b>petal length</div>'
             f'<div><b>{m.PetalWidthCm:.1f} cm</b>petal width</div></div>')
    with col:
        html(plate(i, 180, facts))

st.markdown("### How it works")
html("""
<div class="steps">
  <div class="step"><div class="step-n">1</div><div class="step-t">Measure</div>
    <div class="step-d">Enter four measurements in centimetres: sepal length, sepal width, petal length and petal width.</div></div>
  <div class="step"><div class="step-n">2</div><div class="step-t">Ask the tree</div>
    <div class="step-d">Your numbers are scaled and walked down a decision tree, one yes-or-no question at a time.</div></div>
  <div class="step"><div class="step-n">3</div><div class="step-t">Meet your flower</div>
    <div class="step-d">You get the species, how sure the model is, and the exact questions that led to the answer.</div></div>
</div>
""")
