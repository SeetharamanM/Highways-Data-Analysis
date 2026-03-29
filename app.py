"""
Landing page: Data Analysis app. Links to data file pages.
"""
import streamlit as st
from pathlib import Path

st.set_page_config(page_title="Data Analysis", layout="wide")

st.title("Data Analysis")

st.markdown("Choose a data file to view and analyse.")

# Get current page from query params
try:
    current_page = st.query_params.get("page", "")
except:
    current_page = ""

# Helper function to create page link or bold text
def nav_item(page_path, label, icon="📄"):
    page_name = Path(page_path).name
    if current_page and page_name in current_page:
        st.sidebar.markdown(f"**{icon} {label}**")
    else:
        st.page_link(page_path, label=label, icon=icon)

# Links to data file pages in sidebar with collapsible categories
with st.sidebar.expander("**CRIDP 2025-26**", expanded=True):
    nav_item("pages/2_ku_estimate_details.py", "KU Estimate Details")
    nav_item("pages/4_sh_junction_details.py", "SH Junction Details")

with st.sidebar.expander("**Restoration**", expanded=True):
    nav_item("pages/1_restoration_tender.py", "Restoration Tender")

with st.sidebar.expander("**Road Safety**", expanded=True):
    nav_item("pages/6_sh154_accident_spot.py", "SH-154 Accident Spot Estimate")

with st.sidebar.expander("**CRIDP 2026-27**", expanded=True):
    nav_item("pages/3_cridp_2026_27_proposal.py", "CRIDP 2026-27 Proposal")

with st.sidebar.expander("**VNBR**", expanded=True):
    nav_item("pages/5_vnbr_15_1.py", "VNBR 15-1 Land Acquisition")
    nav_item("pages/7_final_award_ward_10.py", "Final Award Table - Ward 10")
