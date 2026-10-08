import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from irisgarden import pipeline as P
from irisgarden.store import get_bundle
from irisgarden.theme import COLORS, html, page_header, show_chart, style_fig

bundle = get_bundle()
m = bundle["metrics"]

page_header("Model performance", "How well the decision tree does on flowers it never saw during training.")

c = st.columns(4)
c[0].metric("Accuracy", f"{m['accuracy']*100:.1f}%")
c[1].metric("Precision", f"{m['precision']*100:.1f}%")
c[2].metric("Recall", f"{m['recall']*100:.1f}%")
c[3].metric("F1 score", f"{m['f1']*100:.1f}%")
st.caption(f"Measured on {m['n_test']} held-out flowers (20% of the data). One flower is about 3 percentage points, "
           "so small differences between models are not meaningful.")

left, right = st.columns(2, gap="large")
with left:
    cm = m["confusion"]
    fig = go.Figure(go.Heatmap(z=cm, x=P.CLASS_NAMES, y=P.CLASS_NAMES, text=cm, texttemplate="%{text}",
                               colorscale=[[0, "#F4F1FB"], [1, "#7A3FD1"]], showscale=False))
    fig.update_layout(xaxis_title="Predicted", yaxis_title="Actual", yaxis=dict(autorange="reversed"))
    show_chart(style_fig(fig, 380, "Confusion matrix"))
with right:
    imp = pd.DataFrame({"Feature": [P.SHORT[f] for f in P.FEATURES],
                        "Importance": [bundle["importances"][f] for f in P.FEATURES]}).sort_values("Importance")
    bar = px.bar(imp, x="Importance", y="Feature", orientation="h", color_discrete_sequence=["#7A3FD1"])
    show_chart(style_fig(bar, 380, "What the tree relies on"))

st.markdown("#### Per-species report")
rep = pd.DataFrame(m["report"]).T.loc[P.CLASS_NAMES, ["precision", "recall", "f1-score", "support"]]
rep["support"] = rep["support"].astype(int)
st.dataframe(rep.round(3))

st.markdown("#### The tree, in plain rules")
st.caption("Thresholds are converted back to centimetres.")
st.code(P.tree_rules(bundle), language="text")

st.markdown("#### Compared with the other models in the notebook")
comp = pd.DataFrame([
    ["Decision Tree (tuned)", 1.0000, 0.9535],
    ["Logistic Regression (tuned)", 0.9677, None],
    ["KNN (tuned)", 0.9677, None],
    ["Random Forest (tuned)", 0.9677, 0.9602],
    ["XGBoost (tuned)", 0.9355, 0.9469],
], columns=["Model", "Test accuracy", "5-fold CV accuracy"])
st.dataframe(comp, hide_index=True)
cmp_fig = px.bar(comp, x="Model", y="Test accuracy", color_discrete_sequence=["#D857A6"])
cmp_fig.update_yaxes(range=[0.8, 1.02])
show_chart(style_fig(cmp_fig, 340))
html('<div class="note">The tuned decision tree scores highest on the 31-flower test set. Cross-validation, which tests on '
     'more splits, shows the decision tree and random forest within about one point of each other, so both are excellent '
     'on this dataset. Figures in this table come from your notebook.</div>')
