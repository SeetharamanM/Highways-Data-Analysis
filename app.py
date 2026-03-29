"""
Landing page: Data Analysis app. Links to data file pages.
"""
import streamlit as st

st.set_page_config(page_title="Data Analysis", layout="wide")

st.title("Data Analysis")

st.markdown("Choose a data file to view and analyse.")

# Links to data file pages
st.page_link("pages/1_restoration_tender.py", label="Restoration Tender", icon="📄")
st.page_link("pages/2_ku_estimate_details.py", label="KU Estimate Details", icon="📄")
st.page_link("pages/3_cridp_2026_27_proposal.py", label="CRIDP 2026-27 Proposal", icon="📄")
st.page_link("pages/4_sh_junction_details.py", label="SH Junction Details", icon="📄")
st.page_link("pages/5_vnbr_15_1.py", label="VNBR 15-1 Land Acquisition", icon="📄")
st.page_link("pages/6_sh154_accident_spot.py", label="SH-154 Accident Spot Estimate", icon="📄")
