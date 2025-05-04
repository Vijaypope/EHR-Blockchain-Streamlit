import streamlit as st
import json
import os

st.title("View Health Records")

def load_records():
    if os.path.exists("records.json"):
        with open("records.json", "r") as f:
            return json.load(f)
    return []

records = load_records()

if records:
    for r in records:
        st.markdown(f"**Patient:** {r['patient']}")
        st.markdown(f"**Record:** {r['record']}")
        st.markdown(f"**Hash:** `{r['hash']}`")
        st.markdown(f"**Timestamp:** {r['timestamp']}")
        st.markdown("---")
else:
    st.warning("No records found.")
