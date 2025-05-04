import streamlit as st
from utils import add_patient, add_block

st.title("Register Patient")

id = st.text_input("Patient ID")
name = st.text_input("Name")
age = st.number_input("Age", min_value=0)
gender = st.selectbox("Gender", ["Male", "Female", "Other"])

if st.button("Register"):
    success = add_patient(id, name, age, gender)
    if success:
        add_block(f"Registered patient {id}")
        st.success("Patient registered successfully!")
    else:
        st.error("Patient ID already exists.")
