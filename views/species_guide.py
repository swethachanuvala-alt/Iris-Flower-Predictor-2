import streamlit as st

from irisgarden.flowers import SPECIES, flower_svg
from irisgarden.store import get_plot_data
from irisgarden.theme import html, page_header

df = get_plot_data()
page_header("Species guide", "How to tell the three irises apart, using the measurements in the dataset.")

TEXT = {
    "Setosa": ("The smallest-petalled of the three. Its standards (the upright petals) are tiny, almost bristle-like, "
               "which is why it is called the bristle-pointed iris. It is found in cold northern regions.",
               "A petal shorter than about 2.6 cm is almost always a Setosa. This is the very first question the model asks."),
    "Versicolor": ("The blue flag. Medium-sized blooms in blue-violet, often with a golden patch at the base of each fall. "
                   "It grows in wet meadows and marshes of eastern North America.",
                   "Sits in the middle: petals around 4 to 5 cm long and under about 1.75 cm wide."),
    "Virginica": ("The Virginia blue flag. The largest flowers in this dataset, with long wide petals in deep violet. "
                  "It lives in wetlands of the south-eastern United States.",
                  "Wide petals (over about 1.75 cm) or very long ones (over about 5 cm) point to Virginica."),
}
for i, name in enumerate(["Setosa", "Versicolor", "Virginica"]):
    s = SPECIES[i]
    sub = df[df["Species"] == name]
    chips = "".join(
        f'<span class="chip">{label}: {sub[col].min():.1f} to {sub[col].max():.1f} cm</span>'
        for label, col in [("Petal length", "PetalLengthCm"), ("Petal width", "PetalWidthCm"),
                           ("Sepal length", "SepalLengthCm"), ("Sepal width", "SepalWidthCm")])
    body, tip = TEXT[name]
    html(f"""
    <div class="guide">
      <div>{flower_svg(i, 230, stem=True)}</div>
      <div>
        <div class="guide-name" style="color:{s['vein']}">{s['name']}</div>
        <div class="plate-latin">{s['latin']} &middot; {s['common']}</div>
        <p>{body}</p>
        <p><b>Quick tell:</b> {tip}</p>
        <div class="chips">{chips}</div>
      </div>
    </div>
    """)
