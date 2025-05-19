import streamlit as st
import pickle
import sys
import os
import time
from PIL import Image
import base64
import io

# Add app directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import modules
from utils.auth import check_password, login_user, logout_user, is_authenticated
from utils.blockchain import Blockchain
from utils.animations import loading_animation
from utils.decorators import login_required, redirect_if_authenticated
from pages.doctor import show_doctor_dashboard
from pages.patient import show_patient_dashboard
from classes.patient import Patient
from classes.doctor import Doctor

# Set page config
st.set_page_config(
    page_title="EHR Blockchain System",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize directory structure if it doesn't exist
os.makedirs("data", exist_ok=True)

def initialize_session_state():
    """Initialize session state variables for the application."""
    # Initialize user authentication state
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    
    if 'current_user' not in st.session_state:
        st.session_state.current_user = None
    
    if 'current_role' not in st.session_state:
        st.session_state.current_role = None
    
    # Initialize blockchain
    if 'blockchain' not in st.session_state:
        # First try to load the blockchain from pickle file
        try:
            import os
            
            # Make sure the data directory exists
            os.makedirs("data", exist_ok=True)
            
            # Check if file exists and has content
            if os.path.exists("data/blockchain.pkl") and os.path.getsize("data/blockchain.pkl") > 0:
                with open("data/blockchain.pkl", "rb") as f:
                    try:
                        st.session_state.blockchain = pickle.load(f)
                    except Exception as e:
                        st.warning(f"Error loading blockchain data: {e}. Creating a new blockchain.")
                        st.session_state.blockchain = Blockchain()
                        # Backup the corrupted file
                        if os.path.exists("data/blockchain.pkl"):
                            os.rename("data/blockchain.pkl", "data/blockchain.pkl.bak")
                        # Create a new pickle file
                        with open("data/blockchain.pkl", "wb") as f:
                            pickle.dump(st.session_state.blockchain, f)
            else:
                # Create a new blockchain if file doesn't exist or is empty
                st.session_state.blockchain = Blockchain()
                with open("data/blockchain.pkl", "wb") as f:
                    pickle.dump(st.session_state.blockchain, f)
        except Exception as e:
            st.error(f"Critical error initializing blockchain: {e}")
            st.session_state.blockchain = Blockchain()
    
    # Initialize other session state variables as needed
    if 'page' not in st.session_state:
        st.session_state.page = 'welcome'
    
    if 'users' not in st.session_state:
        try:
            with open("data/users.pkl", "rb") as f:
                st.session_state.users = pickle.load(f)
        except (FileNotFoundError, EOFError, pickle.UnpicklingError):
            # Default users with roles (doctor, patient, admin)
            st.session_state.users = {
                "doctor1": {"password": "doc123", "role": "doctor", "name": "Dr. Smith"},
                "patient1": {"password": "pat123", "role": "patient", "name": "John Doe"},
                "admin": {"password": "admin123", "role": "admin", "name": "Admin User"}
            }
            with open("data/users.pkl", "wb") as f:
                pickle.dump(st.session_state.users, f)

def show_login_form():
    """Display the login form."""
    st.subheader("Login")
    
    # Select user type
    user_type = st.selectbox("Login as", ["Patient", "Doctor"])
    
    # Email and password inputs
    email = st.text_input("Email Address", key="login_email")
    password = st.text_input("Password", type="password", key="login_password")
    
    if st.button("Login"):
        if not email or not password:
            st.error("Please enter both email and password")
            return
            
        # Show loading animation
        with st.spinner("Logging in..."):
            time.sleep(1)  # Simulate network delay
            
            # Handle different user types
            if user_type.lower() == "patient":
                patient = Patient.get_patient_by_email(email)
                if patient and patient.verify_password(password):
                    # Login successful
                    login_user(patient.patient_id, "patient")
                    st.success("Login successful!")
                    st.rerun()
                else:
                    st.error("Invalid email or password")
            else:  # Doctor login
                doctor = Doctor.get_doctor_by_email(email)
                if doctor and doctor.verify_password(password):
                    # Login successful
                    login_user(doctor.doctor_id, "doctor")
                    st.success("Login successful!")
                    st.rerun()
                else:
                    st.error("Invalid email or password")

def show_register_form():
    """Display registration form."""
    st.subheader("Register")
    
    # Select user type
    user_type = st.selectbox("Register as", ["Patient", "Doctor"])
    
    # Common fields
    name = st.text_input("Full Name", key="reg_name")
    email = st.text_input("Email Address", key="reg_email")
    password = st.text_input("Password", type="password", key="reg_password")
    confirm_password = st.text_input("Confirm Password", type="password", key="confirm_password")
    
    # Type-specific fields
    if user_type == "Patient":
        date_of_birth = st.date_input("Date of Birth")
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        blood_group = st.selectbox("Blood Group", ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"])
        contact = st.text_input("Contact Number")
        address = st.text_area("Address")
        
        if st.button("Register"):
            if password != confirm_password:
                st.error("Passwords don't match!")
                return
                
            # Show registration process
            with st.spinner("Creating your account..."):
                time.sleep(1)  # Simulate network delay
                
                # Check if email already exists
                existing_patient = Patient.get_patient_by_email(email)
                if existing_patient:
                    st.error("Email already registered!")
                    return
                
                # Create new patient
                try:
                    patient = Patient(
                        name=name,
                        email=email,
                        date_of_birth=str(date_of_birth),
                        gender=gender,
                        blood_group=blood_group,
                        contact=contact,
                        address=address
                    )
                    patient.set_password(password)
                    patient.save()
                    
                    # Add genesis block to patient's medical records if it's the first patient
                    if not os.path.exists("data/blockchain.pkl"):
                        blockchain = Blockchain()
                        blockchain.add_genesis_block()
                        with open("data/blockchain.pkl", "wb") as f:
                            pickle.dump(blockchain, f)
                    
                    st.success("Registration successful! Please login.")
                except Exception as e:
                    st.error(f"Registration failed: {str(e)}")
    
    else:  # Doctor registration
        specialization = st.text_input("Specialization")
        hospital = st.text_input("Hospital/Clinic")
        license_number = st.text_input("Medical License Number")
        contact = st.text_input("Contact Number")
        
        if st.button("Register"):
            if password != confirm_password:
                st.error("Passwords don't match!")
                return
                
            # Show registration process
            with st.spinner("Creating your account..."):
                time.sleep(1)  # Simulate network delay
                
                # Check if email already exists
                existing_doctor = Doctor.get_doctor_by_email(email)
                if existing_doctor:
                    st.error("Email already registered!")
                    return
                
                # Create new doctor
                try:
                    doctor = Doctor(
                        name=name,
                        email=email,
                        specialization=specialization,
                        hospital=hospital,
                        license_number=license_number,
                        contact=contact
                    )
                    doctor.set_password(password)
                    doctor.save()
                    
                    st.success("Registration successful! Please login.")
                except Exception as e:
                    st.error(f"Registration failed: {str(e)}")

def welcome_page():
    """Display the welcome page with login and registration options."""
    
    # Create columns for layout
    col1, col2 = st.columns([2, 3])
    
    with col1:
        st.title("EHR Blockchain")
        st.subheader("Secure Electronic Health Records")
        
        # Add some explanation about the system
        st.write("""
        Welcome to the EHR Blockchain system, a secure and transparent 
        platform for managing electronic health records using blockchain technology.
        
        **Key Features:**
        - Immutable medical records
        - Secure patient-doctor data sharing
        - Transparent audit trail
        - Patient-controlled access
        """)
        
        # Display login/register tabs
        login_tab, register_tab = st.tabs(["Login", "Register"])
        
        with login_tab:
            show_login_form()
            
        with register_tab:
            show_register_form()
    
    with col2:
        # Display some blockchain visual
        st.image("https://miro.medium.com/max/1400/1*BYVJQCqx7DisAI8HYv8bJw.png", 
                 use_column_width=True,
                 caption="Blockchain-based EHR System")
        
        # Display some stats or info
        st.subheader("System Statistics")
        
        # Try to load blockchain
        try:
            with open("data/blockchain.pkl", "rb") as f:
                blockchain = pickle.load(f)
            blockchain_exists = True
        except (FileNotFoundError, EOFError):
            blockchain_exists = False
            blockchain = Blockchain()
        
        # Try to load patients data
        try:
            patients = Patient.load_patients()
            patients_count = len(patients)
        except:
            patients_count = 0
            
        # Try to load doctors data
        try:
            doctors = Doctor.load_doctors()
            doctors_count = len(doctors)
        except:
            doctors_count = 0
        
        # Display stats in columns
        stat_col1, stat_col2, stat_col3 = st.columns(3)
        
        with stat_col1:
            if blockchain_exists:
                st.metric("Blockchain Blocks", len(blockchain.chain))
            else:
                st.metric("Blockchain Blocks", 1)  # Genesis block
                
        with stat_col2:
            st.metric("Registered Patients", patients_count)
            
        with stat_col3:
            st.metric("Registered Doctors", doctors_count)
            
        # Display blockchain info
        with st.expander("About Blockchain Technology"):
            st.write("""
            **Blockchain** ensures your medical records remain:
            
            * **Immutable** - Once data is recorded, it cannot be altered
            * **Transparent** - All changes are visible in the chain
            * **Secure** - Encrypted and distributed across multiple nodes
            * **Private** - Access controlled by patients
            """)

def main():
    """Main function to run the Streamlit app."""
    # Initialize session state
    initialize_session_state()
    
    # Check authentication status
    if is_authenticated():
        # Show appropriate dashboard based on user type
        if st.session_state.user_type == "patient":
            show_patient_dashboard(st.session_state.user_id)
        else:  # doctor
            show_doctor_dashboard(st.session_state.user_id)
    else:
        # Show welcome page with login/register options
        welcome_page()

if __name__ == "__main__":
    main()
