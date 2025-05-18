import pickle
import os
import hashlib
import uuid
from datetime import datetime

class Doctor:
    """
    A class representing a doctor in the EHR system
    
    Attributes:
        doctor_id (str): Unique identifier for the doctor
        name (str): Full name of the doctor
        email (str): Email address of the doctor
        password_hash (str): Hashed password for authentication
        specialization (str): Medical specialization
        hospital (str): Hospital or clinic affiliation
        license_number (str): Medical license number
        contact (str): Contact information
        patients (list): List of patient IDs under care
        created_at (str): Account creation timestamp
        last_login (str): Last login timestamp
    """
    
    doctors_file = os.path.join("data", "doctors.pkl")
    
    def __init__(self, name, email, specialization, hospital, license_number, contact):
        """
        Initialize a new doctor
        
        Args:
            name (str): Full name of the doctor
            email (str): Email address of the doctor
            specialization (str): Medical specialization
            hospital (str): Hospital or clinic affiliation
            license_number (str): Medical license number
            contact (str): Contact information
        """
        self.doctor_id = str(uuid.uuid4())
        self.name = name
        self.email = email
        self.password_hash = None  # Will be set using set_password method
        self.specialization = specialization
        self.hospital = hospital
        self.license_number = license_number
        self.contact = contact
        self.patients = []  # List of patient IDs under care
        self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.last_login = None
    
    def set_password(self, password):
        """
        Set the password hash for the doctor
        
        Args:
            password (str): Plain text password to hash
        """
        # In a real application, use a proper password hashing library like bcrypt
        self.password_hash = hashlib.sha256(password.encode()).hexdigest()
    
    def verify_password(self, password):
        """
        Verify if the provided password matches the stored hash
        
        Args:
            password (str): Password to verify
            
        Returns:
            bool: True if password matches, False otherwise
        """
        return hashlib.sha256(password.encode()).hexdigest() == self.password_hash
    
    def update_last_login(self):
        """Update the last login timestamp"""
        self.last_login = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.save()
    
    def add_patient(self, patient_id):
        """
        Add a patient to the doctor's care
        
        Args:
            patient_id: ID of the patient to add
            
        Returns:
            bool: True if added, False if already in care
        """
        if patient_id not in self.patients:
            self.patients.append(patient_id)
            self.save()
            return True
        return False
    
    def remove_patient(self, patient_id):
        """
        Remove a patient from the doctor's care
        
        Args:
            patient_id: ID of the patient to remove
            
        Returns:
            bool: True if removed, False if not in care
        """
        if patient_id in self.patients:
            self.patients.remove(patient_id)
            self.save()
            return True
        return False
    
    def is_patient_under_care(self, patient_id):
        """
        Check if a patient is under this doctor's care
        
        Args:
            patient_id: ID of the patient to check
            
        Returns:
            bool: True if under care, False otherwise
        """
        return patient_id in self.patients
    
    def to_dict(self):
        """
        Convert doctor object to dictionary for serialization
        
        Returns:
            dict: Doctor data as dictionary
        """
        return {
            "doctor_id": self.doctor_id,
            "name": self.name,
            "email": self.email,
            "password_hash": self.password_hash,
            "specialization": self.specialization,
            "hospital": self.hospital,
            "license_number": self.license_number,
            "contact": self.contact,
            "patients": self.patients,
            "created_at": self.created_at,
            "last_login": self.last_login
        }
    
    @classmethod
    def from_dict(cls, doctor_dict):
        """
        Create doctor object from dictionary
        
        Args:
            doctor_dict (dict): Doctor data as dictionary
            
        Returns:
            Doctor: New doctor object
        """
        doctor = cls(
            doctor_dict["name"],
            doctor_dict["email"],
            doctor_dict["specialization"],
            doctor_dict["hospital"],
            doctor_dict["license_number"],
            doctor_dict["contact"]
        )
        
        doctor.doctor_id = doctor_dict["doctor_id"]
        doctor.password_hash = doctor_dict["password_hash"]
        doctor.patients = doctor_dict["patients"]
        doctor.created_at = doctor_dict["created_at"]
        doctor.last_login = doctor_dict["last_login"]
        
        return doctor
    
    def save(self):
        """Save doctor to file"""
        # Create data directory if it doesn't exist
        os.makedirs(os.path.dirname(self.doctors_file), exist_ok=True)
        
        # Load existing doctors
        doctors = self.load_doctors()
        
        # Update or add this doctor
        found = False
        for i, doctor in enumerate(doctors):
            if doctor.doctor_id == self.doctor_id:
                doctors[i] = self
                found = True
                break
        
        if not found:
            doctors.append(self)
        
        # Save all doctors back to file
        with open(self.doctors_file, "wb") as f:
            pickle.dump(doctors, f)
    
    @classmethod
    def load_doctors(cls):
        """
        Load all doctors from file
        
        Returns:
            list: List of Doctor objects
        """
        try:
            with open(cls.doctors_file, "rb") as f:
                return pickle.load(f)
        except (FileNotFoundError, EOFError):
            return []
    
    @classmethod
    def get_doctor_by_id(cls, doctor_id):
        """
        Get a doctor by ID
        
        Args:
            doctor_id: ID of the doctor to find
            
        Returns:
            Doctor: Doctor object if found, None otherwise
        """
        doctors = cls.load_doctors()
        for doctor in doctors:
            if doctor.doctor_id == doctor_id:
                return doctor
        return None
    
    @classmethod
    def get_doctor_by_email(cls, email):
        """
        Get a doctor by email
        
        Args:
            email: Email of the doctor to find
            
        Returns:
            Doctor: Doctor object if found, None otherwise
        """
        doctors = cls.load_doctors()
        for doctor in doctors:
            if doctor.email == email:
                return doctor
        return None
    
    @classmethod
    def delete_doctor(cls, doctor_id):
        """
        Delete a doctor by ID
        
        Args:
            doctor_id: ID of the doctor to delete
            
        Returns:
            bool: True if deleted, False if not found
        """
        doctors = cls.load_doctors()
        for i, doctor in enumerate(doctors):
            if doctor.doctor_id == doctor_id:
                del doctors[i]
                with open(cls.doctors_file, "wb") as f:
                    pickle.dump(doctors, f)
                return True
        return False
