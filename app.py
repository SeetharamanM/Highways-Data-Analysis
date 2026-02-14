"""
Landing page: Data Analysis app. Links to data file pages.
"""
import streamlit as st

st.set_page_config(page_title="Data Analysis", layout="wide")

st.title("Data Analysis")

st.markdown("Choose a data file to view and analyse.")

# Link to the restoration tender data page
st.page_link("pages/1_restoration_tender.py", label="Restoration Tender", icon="📄")
