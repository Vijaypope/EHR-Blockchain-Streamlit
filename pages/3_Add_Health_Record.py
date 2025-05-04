import streamlit as st
from utils import read_json, write_json, get_all_patients, add_block
from streamlit_lottie import st_lottie
import requests
import time

# Load Lottie animation
def load_lottie(url):
    r = requests.get(url)
    return r.json() if r.status_code == 200 else None

lottie_json = load_lottie("https://assets4.lottiefiles.com/packages/lf20_9oozxhbn.json")  # health folder

# CSS Animation
st.markdown("""
<style>
@keyframes dropFade {
  from {opacity: 0; transform: translateY(-10px);}
  to {opacity: 1; transform: translateY(0);}
}
.drop-fade {
  animation: dropFade 0.8s ease-in-out;
}
</style>
<div class="drop-fade">
    <h2 style="color: darkred;">Add Health Record</h2>
</div>
""", unsafe_allow_html=True)

# Show Lottie
if lottie_json:
    st_lottie(lottie_json, height=160, speed=1)

# Get patient list
patients = get_all_patients()
patient_options = [f"{p['id']} - {p['name']}" for p in patients]

if not patient_options:
    st.warning("No patients available. Please register a patient first.")
else:
    selected = st.selectbox("Select Patient", patient_options)
    patient_id = selected.split(" - ")[0]

    diagnosis = st.text_area("Diagnosis")
    treatment = st.text_area("Treatment")

    if st.button("Save Record"):
        if diagnosis.strip() == "" or treatment.strip() == "":
            st.error("Please fill out all fields.")
        else:
            records = read_json("records.json")
            new_record = {
                "patient_id": patient_id,
                "diagnosis": diagnosis,
                "treatment": treatment,
                "timestamp": time.ctime()
            }
            records.append(new_record)
            write_json("record.json",records)
          add_block(f"Added health record for patient{patient_id}")
      st_success("Health Record added and secured on blockchain!")
