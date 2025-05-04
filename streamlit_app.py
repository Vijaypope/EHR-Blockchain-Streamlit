import streamlit as st
from streamlit_lottie import st_lottie
import json

st.set_page_config(page_title="EHR using Blockchain", layout="centered", page_icon="🩺")

def load_lottiefile(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)

st.title("EHR using Blockchain")
st.subheader("Welcome to the future of health record security.")
st.info("Use the sidebar to navigate between pages.")

lottie = load_lottiefile("lottie/ehr.json")  # Optional animation
st_lottie(lottie, speed=1, width=500)
