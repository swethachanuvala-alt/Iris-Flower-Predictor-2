import plotly.express as px
import streamlit as st

from irisgarden import pipeline as P
from irisgarden.store import get_plot_data
from irisgarden.theme import COLORS, page_header, show_chart, style_fig

df = get_plot_data()
FEATS = P.FEATURES
NICE = {f: P.SHORT[f] + " (cm)" for f in FEATS}

page_header("Explore the data", "150 irises, 50 of each species, measured in centimetres.")

tab1, tab2, tab3, tab4 = st.tabs(["Scatter", "Distributions", "Relationships", "Raw data"])

with tab1:
    c1, c2 = st.columns(2)
    with c1:
        x = st.selectbox("Horizontal axis", FEATS, index=2, format_func=lambda f: NICE[f])
    with c2:
        y = st.selectbox("Vertical axis", FEATS, index=3, format_func=lambda f: NICE[f])
    fig = px.scatter(df, x=x, y=y, color="Species", color_discrete_map=COLORS, opacity=0.8,
                     labels=NICE)
    fig.update_traces(marker=dict(size=10, line=dict(width=1, color="white")))
    show_chart(style_fig(fig, 460))
    st.caption("Setosa separates cleanly on petal size. Versicolor and Virginica overlap a little.")

with tab2:
    f = st.selectbox("Measurement", FEATS, index=2, format_func=lambda f: NICE[f], key="dist_feat")
    c1, c2 = st.columns(2, gap="large")
    with c1:
        h = px.histogram(df, x=f, color="Species", color_discrete_map=COLORS, barmode="overlay",
                         opacity=0.7, nbins=20, labels=NICE)
        show_chart(style_fig(h, 400, "Histogram"))
    with c2:
        b = px.box(df, x="Species", y=f, color="Species", color_discrete_map=COLORS, labels=NICE)
        b.update_layout(showlegend=False)
        show_chart(style_fig(b, 400, "Spread by species"))

with tab3:
    c1, c2 = st.columns([1, 1.3], gap="large")
    with c1:
        corr = df[FEATS].corr()
        names = [P.SHORT[f] for f in FEATS]
        heat = px.imshow(corr.values, x=names, y=names, text_auto=".2f", zmin=-1, zmax=1,
                         color_continuous_scale=["#5B7BFF", "#F7F3FE", "#D857A6"])
        show_chart(style_fig(heat, 420, "Correlation"))
    with c2:
        cube = px.scatter_3d(df, x="PetalLengthCm", y="PetalWidthCm", z="SepalLengthCm",
                             color="Species", color_discrete_map=COLORS, opacity=0.85, labels=NICE)
        cube.update_traces(marker=dict(size=4))
        show_chart(style_fig(cube, 420, "Three measurements at once"))

with tab4:
    chosen = st.multiselect("Species", ["Setosa", "Versicolor", "Virginica"],
                            default=["Setosa", "Versicolor", "Virginica"])
    view = df[df["Species"].isin(chosen)]
    st.dataframe(view, hide_index=True)
    st.download_button("Download this table as CSV", view.to_csv(index=False).encode("utf-8"),
                       file_name="iris_selection.csv", mime="text/csv")
    st.markdown("**Averages**")
    st.dataframe(view.groupby("Species")[FEATS].mean().round(2))
