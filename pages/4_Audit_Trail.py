import streamlit as st
from utils import get_chain

st.title("Blockchain Audit Trail")

chain = get_chain()

if not chain:
    st.warning("No blocks yet.")
else:
    for block in chain:
        st.code(f"""
Block #{block['index']}
Data: {block['data']}
Hash: {block['hash']}
Prev: {block['previous_hash']}
        """, language="text")
