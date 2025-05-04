import streamlit as st

st.set_page_config(page_title="EHR Blockchain", layout="wide")

st.title("Electronic Health Record (EHR) using Blockchain")
st.markdown("""
Welcome to the decentralized EHR system.  
Use the sidebar to navigate between different pages:
- Register a new patient
- View all patients
- Add new health data
- View audit trail (blockchain)
""")
