import streamlit as st
import hashlib

st.title("Verify Health Record Hash")

record = st.text_area("Paste Health Record Text")
input_hash = st.text_input("Paste Expected Hash")

if st.button("Verify"):
    calculated_hash = hashlib.sha256(record.encode()).hexdigest()
    if calculated_hash == input_hash:
        st.success("Hash MATCHES. Record is valid.")
    else:
        st.error("Hash MISMATCH. Record may be tampered.")
