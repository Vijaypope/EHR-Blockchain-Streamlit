import streamlit as st
from utils import get_all_patients
from streamlit_lottie import st_lottie
import requests

# Lottie animation loader
def load_lottie(url):
    r = requests.get(url)
    return r.json() if r.status_code == 200 else None

# Load animation
lottie_json = load_lottie("https://assets10.lottiefiles.com/packages/lf20_dyqqcazd.json")  # file animation

# CSS animation
st.markdown("""
<style>
@keyframes slideFadeIn {
  from {opacity: 0; transform: translateX(-20px);}
  to {opacity: 1; transform: translateX(0);}
}
.slide-fade {
  animation: slideFadeIn 0.8s ease-out;
}
</style>
<div class="slide-fade">
    <h2 style="color: darkgreen;">View Registered Patients</h2>
</div>
""", unsafe_allow_html=True)

# Show Lottie
if lottie_json:
    st_lottie(lottie_json, height=150, speed=1)

# Show patient records
patients = get_all_patients()

if not patients:
    st.warning("No patients registered yet.")
else:
    for p in patients:
        st.info(f"ID: {p['id']} | Name: {p['name']} | Age: {p['age']} | Gender: {p['gender']}")
