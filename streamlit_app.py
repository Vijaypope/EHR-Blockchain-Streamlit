import streamlit as st
import pickle
import sys
import os
import time
import traceback
import logging
from PIL import Image
import base64
import io
import re

# Configure logging
logging.basicConfig(
    filename='ehr_system.log',
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Add app directory to path
try:
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
except Exception as e:
    st.error(f"Critical error setting up application path: {str(e)}")
    logger.critical(f"Path setup error: {str(e)}")
    sys.exit(1)

# Import modules with error handling
try:
    from utils.auth import check_password, login_user, logout_user, is_authenticated
    from utils.blockchain import Blockchain
    from utils.animations import loading_animation
    from utils.decorators import login_required, redirect_if_authenticated
    from pages.doctor import show_doctor_dashboard
    from pages.patient import show_patient_dashboard
    from classes.patient import Patient
    from classes.doctor import Doctor
except ImportError as e:
    st.error(f"Failed to import required modules: {str(e)}")
    logger.critical(f"Import error: {str(e)}")
    st.stop()

# Set page config with error handling
try:
    st.set_page_config(
        page_title="EHR Blockchain System",
        page_icon="🏥",
        layout="wide",
        initial_sidebar_state="expanded"
    )
except Exception as e:
    # If set_page_config fails, log it but continue (non-critical)
    logger.error(f"Page config error: {str(e)}")

# Initialize directory structure if it doesn't exist
try:
    os.makedirs("data", exist_ok=True)
    os.makedirs("logs", exist_ok=True)
except PermissionError:
    st.error("Permission denied when creating application directories. Please check permissions.")
    logger.critical("Permission denied when creating application directories")
    st.stop()
except Exception as e:
    st.error(f"Failed to create required directories: {str(e)}")
    logger.critical(f"Directory creation error: {str(e)}")
    st.stop()

def safe_load_pickle(file_path, default_value):
    """Safely load a pickle file with comprehensive error handling."""
    try:
        if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
            with open(file_path, "rb") as f:
                return pickle.load(f)
        else:
            logger.warning(f"File not found or empty: {file_path}, using default value")
            return default_value
    except pickle.UnpicklingError:
        logger.error(f"Unpickling error for {file_path}, creating backup and using default")
        # Create backup of corrupted file
        if os.path.exists(file_path):
            backup_path = f"{file_path}.{int(time.time())}.bak"
            try:
                os.rename(file_path, backup_path)
                logger.info(f"Corrupted file backed up to {backup_path}")
            except Exception as e:
                logger.error(f"Failed to create backup of corrupted file: {str(e)}")
        return default_value
    except PermissionError:
        logger.error(f"Permission denied when accessing {file_path}")
        st.error(f"Permission denied when accessing data files. Please check permissions.")
        return default_value
    except Exception as e:
        logger.error(f"Error loading {file_path}: {str(e)}")
        return default_value

def safe_save_pickle(data, file_path):
    """Safely save data to a pickle file with error handling."""
    try:
        # Create a temporary file first
        temp_file = f"{file_path}.temp"
        with open(temp_file, "wb") as f:
            pickle.dump(data, f)
        
        # If successful, replace the original file
        if os.path.exists(file_path):
            os.replace(temp_file, file_path)
        else:
            os.rename(temp_file, file_path)
        return True
    except PermissionError:
        logger.error(f"Permission denied when saving to {file_path}")
        st.error("Permission denied when saving data. Please check permissions.")
        return False
    except Exception as e:
        logger.error(f"Failed to save data to {file_path}: {str(e)}")
        if os.path.exists(temp_file):
            try:
                os.remove(temp_file)
            except:
                pass
        return False

def initialize_session_state():
    """Initialize session state variables for the application with error handling."""
    try:
        # Initialize user authentication state
        if 'authenticated' not in st.session_state:
            st.session_state.authenticated = False
        
        if 'current_user' not in st.session_state:
            st.session_state.current_user = None
        
        if 'current_role' not in st.session_state:
            st.session_state.current_role = None
        
        # Initialize blockchain
        if 'blockchain' not in st.session_state:
            # Load the blockchain from pickle file with error handling
            blockchain = safe_load_pickle("data/blockchain.pkl", Blockchain())
            
            # Verify blockchain integrity
            try:
                if not blockchain.is_chain_valid():
                    logger.warning("Blockchain validation failed, creating new blockchain")
                    st.warning("Blockchain data may have been tampered with. Creating a new secure blockchain.")
                    blockchain = Blockchain()
            except AttributeError:
                # If blockchain is corrupted and doesn't have the method
                logger.error("Corrupted blockchain object detected")
                blockchain = Blockchain()
                
            st.session_state.blockchain = blockchain
            # Save the blockchain
            safe_save_pickle(blockchain, "data/blockchain.pkl")
        
        # Initialize other session state variables
        if 'page' not in st.session_state:
            st.session_state.page = 'welcome'
        
        # Initialize users with safe loading
        if 'users' not in st.session_state:
            default_users = {
                "doctor1": {"password": "doc123", "role": "doctor", "name": "Dr. Smith"},
                "patient1": {"password": "pat123", "role": "patient", "name": "John Doe"},
                "admin": {"password": "admin123", "role": "admin", "name": "Admin User"}
            }
            st.session_state.users = safe_load_pickle("data/users.pkl", default_users)
            # Save users if default was used
            if st.session_state.users == default_users:
                safe_save_pickle(default_users, "data/users.pkl")
    
    except Exception as e:
        logger.critical(f"Session state initialization error: {str(e)}")
        st.error(f"An unexpected error occurred while initializing the application. Please contact support.")
        # In a production system, you might want to include a support identifier for this error
        st.stop()

def validate_email(email):
    """Validate email format."""
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return re.match(pattern, email) is not None

def validate_password(password):
    """Validate password strength."""
    # At least 8 characters, 1 uppercase, 1 lowercase, 1 number
    if len(password) < 8:
        return False, "Password must be at least 8 characters"
    if not any(c.isupper() for c in password):
        return False, "Password must contain at least one uppercase letter"
    if not any(c.islower() for c in password):
        return False, "Password must contain at least one lowercase letter"
    if not any(c.isdigit() for c in password):
        return False, "Password must contain at least one number"
    return True, ""

def validate_phone(phone):
    """Validate phone number format."""
    pattern = r"^\+?[0-9]{10,15}$"
    return re.match(pattern, phone) is not None

def show_login_form():
    """Display the login form with input validation."""
    st.subheader("Login")
    
    # Select user type
    user_type = st.selectbox("Login as", ["Patient", "Doctor"])
    
    # Email and password inputs with validation
    email = st.text_input("Email Address", key="login_email")
    password = st.text_input("Password", type="password", key="login_password")
    
    login_clicked = st.button("Login")
    
    if login_clicked:
        # Input validation
        if not email or not password:
            st.error("Please enter both email and password")
            return
            
        if not validate_email(email):
            st.error("Please enter a valid email address")
            return
        
        # Show loading animation
        with st.spinner("Logging in..."):
            try:
                time.sleep(1)  # Simulate network delay
                
                # Handle different user types
                if user_type.lower() == "patient":
                    try:
                        patient = Patient.get_patient_by_email(email)
                        if patient and patient.verify_password(password):
                            # Login successful
                            login_user(patient.patient_id, "patient")
                            st.success("Login successful!")
                            # Log successful login
                            logger.info(f"Patient login successful for {email}")
                            st.rerun()
                        else:
                            st.error("Invalid email or password")
                            # Log failed login attempt
                            logger.warning(f"Failed patient login attempt for {email}")
                    except Exception as e:
                        st.error("An error occurred during login. Please try again.")
                        logger.error(f"Patient login error: {str(e)}")
                
                else:  # Doctor login
                    try:
                        doctor = Doctor.get_doctor_by_email(email)
                        if doctor and doctor.verify_password(password):
                            # Login successful
                            login_user(doctor.doctor_id, "doctor")
                            st.success("Login successful!")
                            # Log successful login
                            logger.info(f"Doctor login successful for {email}")
                            st.rerun()
                        else:
                            st.error("Invalid email or password")
                            # Log failed login attempt
                            logger.warning(f"Failed doctor login attempt for {email}")
                    except Exception as e:
                        st.error("An error occurred during login. Please try again.")
                        logger.error(f"Doctor login error: {str(e)}")
            
            except Exception as e:
                st.error("An unexpected error occurred. Please try again later.")
                logger.error(f"Login process error: {str(e)}")

def show_register_form():
    """Display registration form with comprehensive validation."""
    st.subheader("Register")
    
    # Select user type
    user_type = st.selectbox("Register as", ["Patient", "Doctor"])
    
    # Common fields with validation
    name = st.text_input("Full Name", key="reg_name")
    email = st.text_input("Email Address", key="reg_email")
    password = st.text_input("Password", type="password", key="reg_password",
                           help="At least 8 characters with uppercase, lowercase, and numbers")
    confirm_password = st.text_input("Confirm Password", type="password", key="confirm_password")
    
    # Type-specific fields
    if user_type == "Patient":
        try:
            date_of_birth = st.date_input("Date of Birth")
            gender = st.selectbox("Gender", ["Male", "Female", "Other"])
            blood_group = st.selectbox("Blood Group", ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"])
            contact = st.text_input("Contact Number")
            address = st.text_area("Address")
            
            register_clicked = st.button("Register")
            
            if register_clicked:
                # Validate input fields
                if not name or not email or not password or not contact or not address:
                    st.error("All fields are required")
                    return
                
                if not validate_email(email):
                    st.error("Please enter a valid email address")
                    return
                
                if password != confirm_password:
                    st.error("Passwords don't match!")
                    return
                
                is_valid_password, password_error = validate_password(password)
                if not is_valid_password:
                    st.error(password_error)
                    return
                
                if not validate_phone(contact):
                    st.error("Please enter a valid phone number")
                    return
                
                # Show registration process
                with st.spinner("Creating your account..."):
                    try:
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
                            
                            if patient.save():
                                # Add genesis block to patient's medical records if it's the first patient
                                if not os.path.exists("data/blockchain.pkl"):
                                    try:
                                        blockchain = Blockchain()
                                        blockchain.add_genesis_block()
                                        safe_save_pickle(blockchain, "data/blockchain.pkl")
                                    except Exception as e:
                                        logger.error(f"Failed to create genesis block: {str(e)}")
                                
                                st.success("Registration successful! Please login.")
                                logger.info(f"New patient registered: {email}")
                            else:
                                st.error("Failed to save patient data. Please try again.")
                                logger.error(f"Failed to save patient data for {email}")
                        except Exception as e:
                            st.error(f"Registration failed: {str(e)}")
                            logger.error(f"Patient registration error: {str(e)}")
                    except Exception as e:
                        st.error("An unexpected error occurred. Please try again later.")
                        logger.error(f"Patient registration process error: {str(e)}")
        except Exception as e:
            st.error("An error occurred in the registration form. Please refresh the page and try again.")
            logger.error(f"Patient registration form error: {str(e)}")
    
    else:  # Doctor registration
        try:
            specialization = st.text_input("Specialization")
            hospital = st.text_input("Hospital/Clinic")
            license_number = st.text_input("Medical License Number")
            contact = st.text_input("Contact Number")
            
            register_clicked = st.button("Register")
            
            if register_clicked:
                # Validate input fields
                if not name or not email or not password or not specialization or not license_number or not contact:
                    st.error("All fields are required")
                    return
                
                if not validate_email(email):
                    st.error("Please enter a valid email address")
                    return
                
                if password != confirm_password:
                    st.error("Passwords don't match!")
                    return
                
                is_valid_password, password_error = validate_password(password)
                if not is_valid_password:
                    st.error(password_error)
                    return
                
                if not validate_phone(contact):
                    st.error("Please enter a valid phone number")
                    return
                
                # Show registration process
                with st.spinner("Creating your account..."):
                    try:
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
                            
                            if doctor.save():
                                st.success("Registration successful! Please login.")
                                logger.info(f"New doctor registered: {email}")
                            else:
                                st.error("Failed to save doctor data. Please try again.")
                                logger.error(f"Failed to save doctor data for {email}")
                        except Exception as e:
                            st.error(f"Registration failed: {str(e)}")
                            logger.error(f"Doctor registration error: {str(e)}")
                    except Exception as e:
                        st.error("An unexpected error occurred. Please try again later.")
                        logger.error(f"Doctor registration process error: {str(e)}")
        except Exception as e:
            st.error("An error occurred in the registration form. Please refresh the page and try again.")
            logger.error(f"Doctor registration form error: {str(e)}")

def welcome_page():
    """Display the welcome page with login and registration options with error handling."""
    try:
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
            try:
                login_tab, register_tab = st.tabs(["Login", "Register"])
                
                with login_tab:
                    show_login_form()
                    
                with register_tab:
                    show_register_form()
            except Exception as e:
                st.error("An error occurred in the authentication forms. Please refresh the page.")
                logger.error(f"Authentication tabs error: {str(e)}")
        
        with col2:
            try:
                # Display blockchain visual - with fallback option
                try:
                    st.image("https://miro.medium.com/max/1400/1*BYVJQCqx7DisAI8HYv8bJw.png", 
                            use_column_width=True,
                            caption="Blockchain-based EHR System")
                except Exception:
                    # If image loading fails, show a placeholder message
                    st.info("Blockchain visualization loading failed. Using text-based description instead.")
                    st.markdown("""
                    ```
                    [Block 1] <- [Block 2] <- [Block 3] <- ... <- [Current Block]
                    ```
                    """)
                
                # Display system statistics with error handling
                st.subheader("System Statistics")
                
                # Try to load blockchain
                try:
                    blockchain = safe_load_pickle("data/blockchain.pkl", Blockchain())
                    blockchain_exists = True
                except Exception:
                    blockchain_exists = False
                    blockchain = Blockchain()
                
                # Try to load patients data
                try:
                    patients = Patient.load_patients()
                    patients_count = len(patients)
                except Exception:
                    patients_count = 0
                    
                # Try to load doctors data
                try:
                    doctors = Doctor.load_doctors()
                    doctors_count = len(doctors)
                except Exception:
                    doctors_count = 0
                
                # Display stats in columns with error handling
                try:
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
                except Exception as e:
                    st.error("Failed to display system statistics")
                    logger.error(f"Statistics display error: {str(e)}")
                
                # Display blockchain info
                with st.expander("About Blockchain Technology"):
                    st.write("""
                    **Blockchain** ensures your medical records remain:
                    
                    * **Immutable** - Once data is recorded, it cannot be altered
                    * **Transparent** - All changes are visible in the chain
                    * **Secure** - Encrypted and distributed across multiple nodes
                    * **Private** - Access controlled by patients
                    """)
            except Exception as e:
                st.error("Error loading welcome page content. Please refresh.")
                logger.error(f"Welcome page content error: {str(e)}")
    
    except Exception as e:
        st.error("Critical error loading the welcome page. Please contact support.")
        logger.critical(f"Welcome page error: {str(e)}")

def main():
    """Main function to run the Streamlit app with comprehensive error handling."""
    try:
        # Initialize session state
        initialize_session_state()
        
        # Check authentication status
        if is_authenticated():
            try:
                # Show appropriate dashboard based on user type
                if st.session_state.user_type == "patient":
                    show_patient_dashboard(st.session_state.user_id)
                else:  # doctor
                    show_doctor_dashboard(st.session_state.user_id)
            except Exception as e:
                st.error("An error occurred while loading your dashboard. Please try logging in again.")
                logout_user()  # Force logout on error
                logger.error(f"Dashboard loading error: {str(e)}")
                st.rerun()
        else:
            # Show welcome page with login/register options
            welcome_page()
    
    except Exception as e:
        error_msg = str(e)
        error_trace = traceback.format_exc()
        logger.critical(f"Application crash: {error_msg}\n{error_trace}")
        
        # Display user-friendly error message
        st.error("Sorry, the application encountered a critical error. Our team has been notified.")
        
        # Add details in an expander for technical users
        with st.expander("Technical Details"):
            st.code(error_trace)
            st.info("This information has been logged. Please contact support with the time of this error.")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        # Last resort error handling for truly unexpected errors
        st.error("Critical application error. Please restart the application.")
        logger.critical(f"Unhandled exception in main thread: {str(e)}\n{traceback.format_exc()}")
