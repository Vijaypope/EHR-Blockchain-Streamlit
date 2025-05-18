"""
Authentication utilities for the EHR Chain application.
"""

# Demo credentials (in a real app, these would be stored securely, e.g., in a database with hashing)
DEMO_CREDENTIALS = {
    'doctor': {
        'username': 'doctor',
        'password': 'doctor123',
        'name': 'Dr. Sarah Johnson',
        'specialization': 'Cardiologist',
        'hospital': 'City General Hospital',
        'license': 'MD12345'
    },
    'patient': {
        'username': 'patient',
        'password': 'patient123',
        'name': 'John Smith',
        'age': 42,
        'blood_type': 'A+',
        'address': '123 Health Street, Medical City',
        'insurance': 'Health Assured Inc.'
    }
}

def check_credentials(username, password, user_type):
    """
    Verify user credentials.
    
    Args:
        username (str): The username to check
        password (str): The password to verify
        user_type (str): Either 'doctor' or 'patient'
        
    Returns:
        bool: True if credentials are valid, False otherwise
    """
    # Check if the user exists and the password matches
    if user_type in DEMO_CREDENTIALS:
        user = DEMO_CREDENTIALS[user_type]
        return username == user['username'] and password == user['password']
    return False

def get_user_data(username, user_type):
    """
    Get user data for the specified username and user type.
    
    Args:
        username (str): The username to look up
        user_type (str): Either 'doctor' or 'patient'
        
    Returns:
        dict: User data if found, None otherwise
    """
    if user_type in DEMO_CREDENTIALS and username == DEMO_CREDENTIALS[user_type]['username']:
        return DEMO_CREDENTIALS[user_type]
    return None
