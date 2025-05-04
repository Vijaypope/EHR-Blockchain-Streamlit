import streamlit as st
from utils import add_patient, add_block
from streamlit_lottie import st_lottie
import requests

# Load Lottie animation
def load_lottie(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

lottie_url = "https://assets1.lottiefiles.com/packages/lf20_myejiggj.json"
lottie_json = load_lottie(lottie_url)

# Page animation style
st.markdown("""
<style>
@keyframes fadeIn {
  from {opacity: 0; transform: translateY(20px);}
  to {opacity: 1; transform: translateY(0);}
}
.fade-in {
  animation: fadeIn 1s ease-out;
}
</style>
<div class="fade-in">
    <h2 style="color: teal;">Register New Patient</h2>
</div>
""", unsafe_allow_html=True)

# Show animation
if lottie_json:
    st_lottie(lottie_json, height=150, speed=1)

# Form
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
