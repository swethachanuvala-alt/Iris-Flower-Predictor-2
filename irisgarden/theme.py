"""Look and feel: colours, CSS and small HTML helpers."""
from __future__ import annotations

import streamlit as st

from irisgarden.flowers import SPECIES, flower_svg

INK = "#1E1B4B"
COLORS = {"Setosa": "#5B7BFF", "Versicolor": "#D857A6", "Virginica": "#7A3FD1"}

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,700&family=Nunito+Sans:wght@400;600;700&display=swap');
html, body, .stApp { font-family: 'Nunito Sans', 'Segoe UI', sans-serif; color: #1E1B4B; }
.stApp {
  background:
    radial-gradient(900px 520px at 92% -8%, #E4D8FB 0%, rgba(228,216,251,0) 62%),
    radial-gradient(800px 480px at -8% 18%, #DCE6FF 0%, rgba(220,230,255,0) 58%),
    #F7F3FE;
}
#MainMenu, footer { visibility: hidden; }
.block-container { padding-top: 2.2rem; max-width: 1180px; }
h1, h2, h3, h4 { font-family: 'Fraunces', Georgia, serif !important; color: #1E1B4B; letter-spacing: -0.01em; }
[data-testid="stSidebar"] { background: linear-gradient(180deg, #EFE8FC 0%, #E2E9FF 100%); border-right: 1px solid #D9CFF3; }
.stButton > button { border-radius: 999px; border: 1px solid #C9B8F0; background: #fff; color: #3B2A7A; font-weight: 700; }
.stButton > button:hover { border-color: #7A3FD1; color: #7A3FD1; }
[data-testid="stMetric"] { background: #fff; border: 1px solid #E4DAF7; border-radius: 14px; padding: 12px 16px; }
.stTabs [data-baseweb="tab"] { font-weight: 700; }

.brand { display: flex; align-items: center; gap: 10px; padding: 4px 4px 14px 4px; }
.brand-name { font-family: 'Fraunces', Georgia, serif; font-size: 1.35rem; font-weight: 700; line-height: 1.1; }
.brand-sub { font-size: .8rem; color: #5B4F8F; }
.side-foot { font-size: .8rem; color: #5B4F8F; padding-top: 10px; }

.page-title { font-family: 'Fraunces', Georgia, serif; font-size: clamp(1.9rem, 3.6vw, 2.8rem); font-weight: 700; line-height: 1.1; }
.page-sub { color: #4C4579; font-size: 1.05rem; margin-top: 6px; max-width: 62ch; }
.tri-rule { display: flex; height: 5px; width: 120px; margin: 14px 0 22px 0; border-radius: 99px; overflow: hidden; }
.tri-rule i { flex: 1; }

.hero { display: grid; grid-template-columns: 1.05fr .95fr; align-items: center; gap: 10px; border-radius: 30px; overflow: hidden;
  background: linear-gradient(135deg, #17133F 0%, #2B1B66 55%, #4A2A8E 100%); padding: 38px 38px 8px 44px; margin-bottom: 18px; }
.hero-title { font-family: 'Fraunces', Georgia, serif; font-weight: 700; color: #fff; font-size: clamp(2.2rem, 4.6vw, 3.7rem); line-height: 1.04; }
.hero-sub { color: #D5CCF5; font-size: 1.1rem; margin: 16px 0 10px 0; max-width: 40ch; line-height: 1.5; }
.hero-note { color: #A99DDB; font-size: .92rem; padding-bottom: 28px; }
.hero-art svg { width: 100%; height: auto; display: block; }
@media (max-width: 820px) { .hero { grid-template-columns: 1fr; padding: 28px 22px 0 22px; } }

.plate { border-radius: 999px 999px 22px 22px; padding: 30px 18px 20px 18px; text-align: center; border: 1px solid rgba(30,27,75,.08); }
.plate-name { font-family: 'Fraunces', Georgia, serif; font-size: 1.55rem; font-weight: 700; margin-top: 2px; }
.plate-latin { font-style: italic; color: #4C4579; font-size: .95rem; }
.plate-facts { display: flex; justify-content: center; gap: 18px; margin-top: 12px; font-size: .9rem; color: #3C3568; }
.plate-facts b { display: block; font-size: 1.05rem; color: #1E1B4B; }

.steps { display: grid; grid-template-columns: repeat(3, 1fr); gap: 22px; margin: 6px 0 10px 0; }
.step { border-top: 3px solid #7A3FD1; padding-top: 12px; }
.step-n { font-family: 'Fraunces', Georgia, serif; font-size: 1.5rem; font-weight: 700; color: #7A3FD1; }
.step-t { font-weight: 700; font-size: 1.05rem; margin: 2px 0 4px 0; }
.step-d { color: #4C4579; font-size: .95rem; line-height: 1.5; }
@media (max-width: 820px) { .steps { grid-template-columns: 1fr; } }

.result { border-radius: 999px 999px 26px 26px; text-align: center; padding: 26px 20px 22px 20px; border: 1px solid rgba(30,27,75,.08); }
.result-name { font-family: 'Fraunces', Georgia, serif; font-size: 2.1rem; font-weight: 700; line-height: 1.1; }
.result-latin { font-style: italic; color: #4C4579; }
.bar-row { display: flex; align-items: center; gap: 10px; margin: 9px 0; font-size: .95rem; }
.bar-row span { width: 90px; font-weight: 700; }
.bar-row b { width: 48px; text-align: right; }
.track { flex: 1; height: 12px; border-radius: 99px; background: #E6DEF7; overflow: hidden; }
.fill { height: 100%; border-radius: 99px; }
.rule { padding: 9px 14px; margin: 8px 0; border-left: 4px solid #7A3FD1; background: rgba(255,255,255,.75); border-radius: 0 12px 12px 0; font-size: .95rem; }
.note { background: rgba(255,255,255,.7); border: 1px dashed #BBA8EC; border-radius: 14px; padding: 12px 16px; color: #3C3568; font-size: .95rem; }
.guide { display: grid; grid-template-columns: 240px 1fr; gap: 28px; align-items: center; padding: 18px 8px; }
.guide-name { font-family: 'Fraunces', Georgia, serif; font-size: 1.9rem; font-weight: 700; }
.guide p { margin: 6px 0; line-height: 1.55; }
.chips { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 10px; }
.chip { background: #fff; border: 1px solid #DDD1F5; border-radius: 99px; padding: 4px 12px; font-size: .88rem; }
@media (max-width: 820px) { .guide { grid-template-columns: 1fr; } }
</style>
"""


def html(s: str) -> None:
    """Render raw HTML (whitespace collapsed so Markdown never breaks it)."""
    st.markdown(" ".join(s.split()), unsafe_allow_html=True)


def inject_css() -> None:
    html(CSS)


def sidebar_brand() -> None:
    with st.sidebar:
        html(f'<div class="brand">{flower_svg(1, 44)}<div><div class="brand-name">Iris Garden</div>'
             f'<div class="brand-sub">Flower species predictor</div></div></div>')
        html('<div class="side-foot">Decision Tree &middot; scikit-learn<br>Setosa &middot; Versicolor &middot; Virginica</div>')


def page_header(title: str, subtitle: str) -> None:
    rule = "".join(f'<i style="background:{c}"></i>' for c in COLORS.values())
    html(f'<div class="page-title">{title}</div><div class="page-sub">{subtitle}</div>'
         f'<div class="tri-rule">{rule}</div>')


def style_fig(fig, height=380, title=None):
    layout = dict(font=dict(family="Nunito Sans, Segoe UI, sans-serif", color=INK),
                  paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(255,255,255,0.65)",
                  margin=dict(l=10, r=10, t=50 if title else 20, b=10), height=height,
                  legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0))
    if title:
        layout["title"] = dict(text=title, x=0.0)
    fig.update_layout(**layout)
    return fig


def show_chart(fig) -> None:
    """Full-width chart (stretches by default in Streamlit 1.50+)."""
    st.plotly_chart(fig)


def plate(idx: int, size: int = 190, extra: str = "") -> str:
    s = SPECIES[idx]
    return (f'<div class="plate" style="background:linear-gradient(180deg,{s["tint_a"]},{s["tint_b"]})">'
            f'{flower_svg(idx, size)}<div class="plate-name" style="color:{s["vein"]}">{s["name"]}</div>'
            f'<div class="plate-latin">{s["latin"]} &middot; {s["common"]}</div>{extra}</div>')
