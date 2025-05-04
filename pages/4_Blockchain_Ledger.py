import streamlit as st
import json
import os
from datetime import datetime
import hashlib

st.title("Blockchain Ledger (Simulated)")

def load_chain():
    if os.path.exists("chain.json"):
        with open("chain.json", "r") as f:
            return json.load(f)
    return []

def compute_hash(data):
    return hashlib.sha256(data.encode()).hexdigest()

chain = load_chain()

if not chain:
    st.warning("No blockchain data found.")
else:
    for block in chain:
        st.markdown(f"**Block #{block['index']}**")
        st.json(block)
        st.markdown("---")
