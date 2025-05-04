import streamlit as st
from utils import read_json, get_all_patients
from streamlit_lottie import st_lottie
import requests

# Load Lottie animation
def load_lottie(url):
    r = requests.get(url)
    return r.json() if r.status_code == 200 else None

lottie_json = load_lottie("https://assets4.lottiefiles.com/packages/lf20_a6mcrviy.json")  # doctor icon

# CSS animation
st.markdown("""
<style>
@keyframes bounceIn {
  from {opacity: 0; transform: scale(0.95);}
  to {opacity: 1; transform: scale(1);}
}
.bounce-in {
  animation: bounceIn 0.8s ease-in-out;
}
</style>
<div class="bounce-in">
    <h2 style="color: darkblue;">View Health Records</h2>
</div>
""", unsafe_allow_html=True)

# Show animation
if lottie_json:
    st_lottie(lottie_json, height=150, speed=1)

# Load data
records = read_json("records.json")
patients = get_all_patients()
id_to_name = {p['id']: p['name'] for p in patients}

if not records:
    st.warning("No health records found.")
else:
    for record in records:
        name = id_to_name.get(record["patient_id"], "Unknown Patient")
        st.info(f"""
Patient: {name} (ID: {record['patient_id']})  
Diagnosis: {record['diagnosis']}  
Treatment: {record['treatment']}  
Time: {record['timestamp']}
        """)
