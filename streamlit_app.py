import streamlit as st
import pandas as pd
from utils.auth import check_credentials
from utils.blockchain import Block, Blockchain
from pages.doctor import show_doctor_dashboard
from pages.patient import show_patient_dashboard
import time

# Set page configuration
st.set_page_config(
    page_title="EHR Chain - Blockchain Health Records",
    page_icon="🔗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state variables if they don't exist
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False
if 'user_type' not in st.session_state:
    st.session_state['user_type'] = None
if 'user_data' not in st.session_state:
    st.session_state['user_data'] = None
if 'blockchain' not in st.session_state:
    # Initialize blockchain with a genesis block
    st.session_state['blockchain'] = Blockchain()

# Custom CSS for styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #4F46E5;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #6B7280;
        text-align: center;
        margin-bottom: 2rem;
    }
    .login-container {
        max-width: 500px;
        margin: 0 auto;
        padding: 2rem;
        background-color: #F3F4F6;
        border-radius: 0.5rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .stButton > button {
        width: 100%;
        background-color: #4F46E5;
        color: white;
        border: none;
        padding: 0.75rem 1.5rem;
        font-size: 1rem;
        border-radius: 0.375rem;
    }
    .stButton > button:hover {
        background-color: #4338CA;
    }
    .login-options {
        display: flex;
        justify-content: space-between;
        margin-bottom: 1rem;
    }
    .toggle {
        cursor: pointer;
    }
    .footer {
        margin-top: 2rem;
        text-align: center;
        color: #6B7280;
        font-size: 0.875rem;
    }
</style>
""", unsafe_allow_html=True)

def login_page():
    # Header
    st.markdown('<h1 class="main-header">EHR Chain</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Secure blockchain-based health records</p>', unsafe_allow_html=True)
    
    # Login container
    with st.container():
        st.markdown('<div class="login-container">', unsafe_allow_html=True)
        
        # Doctor/Patient selector
        login_as = st.radio(
            "Login as:",
            ("Doctor", "Patient"),
            horizontal=True
        )
        
        # Username and password fields
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        
        # Login button
        if st.button("Login"):
            with st.spinner("Logging in..."):
                time.sleep(1)  # Simulate login process
                if check_credentials(username, password, login_as.lower()):
                    st.session_state['authenticated'] = True
                    st.session_state['user_type'] = login_as.lower()
                    st.session_state['user_data'] = {
                        'username': username,
                        'role': login_as
                    }
                    st.success(f"Login successful as {login_as}!")
                    st.experimental_rerun()
                else:
                    st.error("Invalid username or password. Please try again.")
        
        # Demo credentials
        with st.expander("Demo Credentials"):
            st.markdown("""
            **Doctor:**
            - Username: `doctor`
            - Password: `doctor123`
            
            **Patient:**
            - Username: `patient`
            - Password: `patient123`
            """)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Footer
    st.markdown('<div class="footer">University Project by Riyaz and Vijay</div>', unsafe_allow_html=True)

def logout():
    st.session_state['authenticated'] = False
    st.session_state['user_type'] = None
    st.session_state['user_data'] = None
    st.success("Logged out successfully!")
    st.experimental_rerun()

# Main app logic
def main():
    if not st.session_state['authenticated']:
        login_page()
    else:
        # Sidebar with logout button
        with st.sidebar:
            st.write(f"Logged in as: **{st.session_state['user_data']['username']}** ({st.session_state['user_data']['role']})")
            if st.button("Logout"):
                logout()
        
        # Display appropriate dashboard based on user type
        if st.session_state['user_type'] == 'doctor':
            show_doctor_dashboard()
        elif st.session_state['user_type'] == 'patient':
            show_patient_dashboard()

if __name__ == "__main__":
    main()
