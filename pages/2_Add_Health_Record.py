import streamlit as st
import json
import hashlib
import os
from datetime import datetime

st.title("Add Health Record")

def load_records():
    if os.path.exists("records.json"):
        with open("records.json", "r") as f:
            return json.load(f)
    return []

def save_records(data):
    with open("records.json", "w") as f:
        json.dump(data, f, indent=4)

def compute_hash(content):
    return hashlib.sha256(content.encode()).hexdigest()

patient = st.text_input("Patient Name")
record = st.text_area("Health Record Description")

if st.button("Submit Record"):
    if patient and record:
        records = load_records()
        record_hash = compute_hash(record)
        records.append({
            "patient": patient,
            "record": record,
            "hash": record_hash,
            "timestamp": datetime.now().isoformat()
        })
        save_records(records)
        st.success("Health record added and hashed!")
    else:
        st.error("Please complete both fields.")
