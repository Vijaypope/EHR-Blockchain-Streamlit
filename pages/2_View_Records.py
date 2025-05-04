import streamlit as st
from utils import get_all_patients

st.title("View All Patients")

patients = get_all_patients()

if not patients:
    st.warning("No patients registered yet.")
else:
    for p in patients:
        st.info(f"ID: {p['id']} | Name: {p['name']} | Age: {p['age']} | Gender: {p['gender']}")
