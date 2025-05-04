import streamlit as st
from utils import get_chain
from streamlit_lottie import st_lottie
import requests

# Lottie animation loader
def load_lottie(url):
    r = requests.get(url)
    return r.json() if r.status_code == 200 else None

lottie_json = load_lottie("https://assets5.lottiefiles.com/packages/lf20_FM0xHZ.json")  # blockchain visual

# CSS animation
st.markdown("""
<style>
@keyframes popIn {
  from {opacity: 0; transform: scale(0.95);}
  to {opacity: 1; transform: scale(1);}
}
.pop-in {
  animation: popIn 0.6s ease-in-out;
}
</style>
<div class="pop-in">
    <h2 style="color: navy;">Blockchain Audit Trail</h2>
</div>
""", unsafe_allow_html=True)

# Show Lottie animation
if lottie_json:
    st_lottie(lottie_json, height=150, speed=1)

# Show blockchain blocks
chain = get_chain()

if not chain:
    st.warning("Blockchain is empty.")
else:
    for block in chain:
        st.code(f"""
Block #{block['index']}
Timestamp: {block['timestamp']}
Data: {block['data']}
Hash: {block['hash']}
Previous Hash: {block['previous_hash']}
        """, language="text")
