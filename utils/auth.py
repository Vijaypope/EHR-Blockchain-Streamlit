import streamlit as st
import time
import os
from datetime import datetime

def login_user(user_id, user_type):
    """
    Log in a user by setting session state variables
    
    Args:
        user_id: The unique ID of the user
        user_type: The type of user ('patient' or 'doctor')
    """
    st.session_state.authenticated = True
    st.session_state.user_id = user_id
    st.session_state.user_type = user_type
    st.session_state.login_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Log the login event
    log_file = os.path.join("data", "login_history.txt")
    with open(log_file, "a") as f:
        f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')},{user_id},{user_type},login\n")

def logout_user():
    """Log out the current user by clearing session state variables"""
    # Log the logout event if user was authenticated
    if st.session_state.authenticated:
        log_file = os.path.join("data", "login_history.txt")
        with open(log_file, "a") as f:
            f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')},{st.session_state.user_id},{st.session_state.user_type},logout\n")
    
    # Clear session state
    st.session_state.authenticated = False
    st.session_state.user_id = None
    st.session_state.user_type = None
    if 'login_time' in st.session_state:
        del st.session_state.login_time

def is_authenticated():
    """Check if the user is authenticated"""
    return st.session_state.authenticated if 'authenticated' in st.session_state else False

def check_password(entered_password, stored_hash):
    """
    Check if the entered password matches the stored hash
    
    In a real application, this would use proper hashing like bcrypt.
    For simplicity, we're using a basic comparison.
    
    Args:
        entered_password: The password entered by the user
        stored_hash: The hashed password stored in the system
        
    Returns:
        bool: True if password matches, False otherwise
    """
    import hashlib
    # In a real app, use a proper password hashing library
    hashed_password = hashlib.sha256(entered_password.encode()).hexdigest()
    return hashed_password == stored_hash
