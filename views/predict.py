import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from irisgarden import pipeline as P
from irisgarden.flowers import SPECIES, flower_svg
from irisgarden.store import get_bundle, get_plot_data
from irisgarden.theme import COLORS, INK, html, page_header, show_chart, style_fig

bundle = get_bundle()
df = get_plot_data()

page_header("Identify a flower", "Slide the four measurements to match your iris. The answer updates as you move.")

KEYS = ["sepal_len", "sepal_wid", "petal_len", "petal_wid"]
LABELS = ["Sepal length (cm)", "Sepal width (cm)", "Petal length (cm)", "Petal width (cm)"]
LIMITS = [(4.0, 8.0), (2.0, 4.5), (1.0, 7.0), (0.1, 2.5)]
PRESETS = {"Setosa": (5.0, 3.4, 1.5, 0.2), "Versicolor": (5.9, 2.8, 4.3, 1.3), "Virginica": (6.6, 3.0, 5.6, 2.0)}

for k, v in zip(KEYS, PRESETS["Versicolor"]):
    st.session_state.setdefault(k, v)


def apply_preset(values):
    for k, v in zip(KEYS, values):
        st.session_state[k] = v


left, right = st.columns([1, 1.2], gap="large")

with left:
    st.markdown("#### Your measurements")
    for k, label, (lo, hi) in zip(KEYS, LABELS, LIMITS):
        st.slider(label, min_value=lo, max_value=hi, step=0.1, key=k)
    st.markdown("**Or start from a typical flower**")
    bcols = st.columns(3)
    for col, (name, vals) in zip(bcols, PRESETS.items()):
        with col:
            st.button(name, key=f"preset_{name}", on_click=apply_preset, args=(vals,))

values = [float(st.session_state[k]) for k in KEYS]
res = P.predict(bundle, values)
idx = res["pred"]
sp = SPECIES[idx]
conf = res["proba"][idx] * 100

with right:
    html(f"""
    <div class="result" style="background:linear-gradient(180deg,{sp['tint_a']},{sp['tint_b']})">
      {flower_svg(idx, 210)}
      <div class="result-name" style="color:{sp['vein']}">{sp['name']}</div>
      <div class="result-latin">{sp['latin']} &middot; {sp['common']}</div>
    </div>
    """)
    bars = "".join(
        f'<div class="bar-row"><span>{SPECIES[i]["name"]}</span><div class="track">'
        f'<div class="fill" style="width:{p*100:.0f}%;background:{SPECIES[i]["accent"]}"></div></div>'
        f'<b>{p*100:.0f}%</b></div>' for i, p in enumerate(res["proba"]))
    st.markdown("#### How sure is the model?")
    html(bars)
    if conf < 100:
        st.caption("Below 100% means the flower sits near the border between two species.")

st.markdown("#### Why this answer?")
st.caption("The decision tree asked these questions about your flower, in order.")
rules = ""
for s in res["steps"]:
    sign = "&le;" if s["left"] else "&gt;"
    rules += (f'<div class="rule" style="border-left-color:{sp["accent"]}"><b>{s["feature"]}</b> '
              f'is {s["value"]:.1f} cm, which is {sign} {s["threshold"]:.2f} cm</div>')
html(rules)

st.markdown("#### Where your flower sits")
c1, c2 = st.columns(2, gap="large")
with c1:
    fig = px.scatter(df, x="PetalLengthCm", y="PetalWidthCm", color="Species",
                     color_discrete_map=COLORS, opacity=0.75,
                     labels={"PetalLengthCm": "Petal length (cm)", "PetalWidthCm": "Petal width (cm)"})
    fig.add_trace(go.Scatter(x=[values[2]], y=[values[3]], mode="markers", name="Your flower",
                             marker=dict(size=18, symbol="star", color="#F4C03F", line=dict(width=2, color=INK))))
    show_chart(style_fig(fig, 380, "Petals"))
with c2:
    feats = P.FEATURES
    lo = df[feats].min()
    hi = df[feats].max()
    norm = lambda vals: [(v - lo[f]) / (hi[f] - lo[f]) for v, f in zip(vals, feats)]
    avg = df[df["Species"] == sp["name"]][feats].mean().tolist()
    theta = [P.SHORT[f] for f in feats]
    theta = theta + [theta[0]]
    mine = norm(values)
    typical = norm(avg)
    fig2 = go.Figure()
    fig2.add_trace(go.Scatterpolar(r=typical + [typical[0]], theta=theta, fill="toself",
                                   name=f"Average {sp['name']}", line=dict(color=sp["accent"]), opacity=0.45))
    fig2.add_trace(go.Scatterpolar(r=mine + [mine[0]], theta=theta, name="Your flower",
                                   line=dict(color=INK, width=3)))
    fig2.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 1], showticklabels=False)))
    show_chart(style_fig(fig2, 380, "Shape profile"))
