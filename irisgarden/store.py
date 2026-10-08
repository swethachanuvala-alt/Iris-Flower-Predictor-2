"""Cached loaders shared by every page."""
import streamlit as st

from irisgarden import pipeline as P


@st.cache_resource(show_spinner="Opening the garden...")
def get_bundle():
    return P.get_bundle()


@st.cache_data(show_spinner=False)
def get_plot_data():
    return P.load_plot_frame()
