import streamlit as st

st.title("User Login / Sign Up")
st.info("Login or create a new account")

# This is a placeholder example. Add Google Sheets integration here if needed.
username = st.text_input("Enter your username")
if st.button("Login"):
    if username:
        st.success(f"Welcome, {username}!")
    else:
        st.error("Please enter a username.")
