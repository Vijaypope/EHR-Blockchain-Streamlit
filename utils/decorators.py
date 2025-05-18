import streamlit as st
import functools

def login_required(func):
    """
    Decorator to require login for accessing a page
    
    Args:
        func: The function to wrap
        
    Returns:
        function: Wrapped function that checks authentication
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if not st.session_state.get('authenticated', False):
            st.error("You need to login to access this page.")
            st.stop()  # Stop execution of the current Streamlit run
        return func(*args, **kwargs)
    return wrapper

def redirect_if_authenticated(func):
    """
    Decorator to redirect to dashboard if already authenticated
    
    Args:
        func: The function to wrap
        
    Returns:
        function: Wrapped function that checks authentication
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if st.session_state.get('authenticated', False):
            if st.session_state.user_type == 'patient':
                from pages.patient import show_patient_dashboard
                show_patient_dashboard(st.session_state.user_id)
            else:
                from pages.doctor import show_doctor_dashboard
                show_doctor_dashboard(st.session_state.user_id)
            st.stop()  # Stop execution of the current Streamlit run
        return func(*args, **kwargs)
    return wrapper

def doctor_required(func):
    """
    Decorator to require doctor role for accessing a page
    
    Args:
        func: The function to wrap
        
    Returns:
        function: Wrapped function that checks user type
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if not st.session_state.get('authenticated', False):
            st.error("You need to login to access this page.")
            st.stop()
        
        if st.session_state.get('user_type') != 'doctor':
            st.error("This page is only accessible to doctors.")
            st.stop()
            
        return func(*args, **kwargs)
    return wrapper

def patient_required(func):
    """
    Decorator to require patient role for accessing a page
    
    Args:
        func: The function to wrap
        
    Returns:
        function: Wrapped function that checks user type
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if not st.session_state.get('authenticated', False):
            st.error("You need to login to access this page.")
            st.stop()
        
        if st.session_state.get('user_type') != 'patient':
            st.error("This page is only accessible to patients.")
            st.stop()
            
        return func(*args, **kwargs)
    return wrapper
