import pickle
import os
import hashlib
import uuid
from datetime import datetime
import json

class Patient:
    """
    A class representing a patient in the EHR system
    
    Attributes:
        patient_id (str): Unique identifier for the patient
        name (str): Full name of the patient
        email (str): Email address of the patient
        password_hash (str): Hashed password for authentication
        date_of_birth (str): Patient's date of birth
        gender (str): Patient's gender
        blood_group (str): Patient's blood group
        contact (str): Contact information (phone number)
        address (str): Patient's address
        medical_history (list): List of medical history records
        current_medications (list): List of current medications
        allergies (list): List of known allergies
        emergency_contact (dict): Emergency contact information
        insurance_info (dict): Insurance information
        created_at (str): Account creation timestamp
        last_login (str): Last login timestamp
    """
    
    patients_file = os.path.join("data", "patients.pkl")
    
    def __init__(self, name, email, date_of_birth, gender, blood_group, contact, address):
        """
        Initialize a new patient
        
        Args:
            name (str): Full name of the patient
            email (str): Email address of the patient
            date_of_birth (str): Patient's date of birth
            gender (str): Patient's gender
            blood_group (str): Patient's blood group
            contact (str): Contact information
            address (str): Patient's address
        """
        self.patient_id = str(uuid.uuid4())
        self.name = name
        self.email = email
        self.password_hash = None  # Will be set using set_password method
        self.date_of_birth = date_of_birth
        self.gender = gender
        self.blood_group = blood_group
        self.contact = contact
        self.address = address
        self.medical_history = []
        self.current_medications = []
        self.allergies = []
        self.emergency_contact = {}
        self.insurance_info = {}
        self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.last_login = None
        self.authorized_doctors = []  # List of doctor IDs authorized to access records
    
    def set_password(self, password):
        """
        Set the password hash for the patient
        
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
    
    def add_medical_history(self, record):
        """
        Add a medical history record
        
        Args:
            record (dict): Medical history record to add
        """
        self.medical_history.append(record)
        self.save()
    
    def add_medication(self, medication):
        """
        Add a medication to current medications
        
        Args:
            medication (dict): Medication info to add
        """
        self.current_medications.append(medication)
        self.save()
    
    def remove_medication(self, medication_id):
        """
        Remove a medication from current medications
        
        Args:
            medication_id: ID of the medication to remove
            
        Returns:
            bool: True if removed successfully, False otherwise
        """
        for i, med in enumerate(self.current_medications):
            if med.get("id") == medication_id:
                del self.current_medications[i]
                self.save()
                return True
        return False
    
    def add_allergy(self, allergy):
        """
        Add an allergy
        
        Args:
            allergy (dict): Allergy information to add
        """
        self.allergies.append(allergy)
        self.save()
    
    def set_emergency_contact(self, name, relationship, contact):
        """
        Set emergency contact information
        
        Args:
            name (str): Name of emergency contact
            relationship (str): Relationship to patient
            contact (str): Contact information
        """
        self.emergency_contact = {
            "name": name,
            "relationship": relationship,
            "contact": contact
        }
        self.save()
    
    def set_insurance_info(self, provider, policy_number, coverage_details):
        """
        Set insurance information
        
        Args:
            provider (str): Insurance provider name
            policy_number (str): Insurance policy number
            coverage_details (dict): Coverage details
        """
        self.insurance_info = {
            "provider": provider,
            "policy_number": policy_number,
            "coverage_details": coverage_details
        }
        self.save()
    
    def authorize_doctor(self, doctor_id):
        """
        Authorize a doctor to access medical records
        
        Args:
            doctor_id: ID of the doctor to authorize
            
        Returns:
            bool: True if authorized, False if already authorized
        """
        if doctor_id not in self.authorized_doctors:
            self.authorized_doctors.append(doctor_id)
            self.save()
            return True
        return False
    
    def revoke_doctor_authorization(self, doctor_id):
        """
        Revoke a doctor's authorization to medical records
        
        Args:
            doctor_id: ID of the doctor to revoke
            
        Returns:
            bool: True if revoked, False if not authorized
        """
        if doctor_id in self.authorized_doctors:
            self.authorized_doctors.remove(doctor_id)
            self.save()
            return True
        return False
    
    def is_doctor_authorized(self, doctor_id):
        """
        Check if a doctor is authorized to access records
        
        Args:
            doctor_id: ID of the doctor to check
            
        Returns:
            bool: True if authorized, False otherwise
        """
        return doctor_id in self.authorized_doctors
    
    def to_dict(self):
        """
        Convert patient object to dictionary for serialization
        
        Returns:
            dict: Patient data as dictionary
        """
        return {
            "patient_id": self.patient_id,
            "name": self.name,
            "email": self.email,
            "password_hash": self.password_hash,
            "date_of_birth": self.date_of_birth,
            "gender": self.gender,
            "blood_group": self.blood_group,
            "contact": self.contact,
            "address": self.address,
            "medical_history": self.medical_history,
            "current_medications": self.current_medications,
            "allergies": self.allergies,
            "emergency_contact": self.emergency_contact,
            "insurance_info": self.insurance_info,
            "created_at": self.created_at,
            "last_login": self.last_login,
            "authorized_doctors": self.authorized_doctors
        }
    
    @classmethod
    def from_dict(cls, patient_dict):
        """
        Create patient object from dictionary
        
        Args:
            patient_dict (dict): Patient data as dictionary
            
        Returns:
            Patient: New patient object
        """
        patient = cls(
            patient_dict["name"],
            patient_dict["email"],
            patient_dict["date_of_birth"],
            patient_dict["gender"],
            patient_dict["blood_group"],
            patient_dict["contact"],
            patient_dict["address"]
        )
        
        patient.patient_id = patient_dict["patient_id"]
        patient.password_hash = patient_dict["password_hash"]
        patient.medical_history = patient_dict["medical_history"]
        patient.current_medications = patient_dict["current_medications"]
        patient.allergies = patient_dict["allergies"]
        patient.emergency_contact = patient_dict["emergency_contact"]
        patient.insurance_info = patient_dict["insurance_info"]
        patient.created_at = patient_dict["created_at"]
        patient.last_login = patient_dict["last_login"]
        patient.authorized_doctors = patient_dict.get("authorized_doctors", [])
        
        return patient
    
    def save(self):
        """Save patient to file"""
        # Create data directory if it doesn't exist
        os.makedirs(os.path.dirname(self.patients_file), exist_ok=True)
        
        # Load existing patients
        patients = self.load_patients()
        
        # Update or add this patient
        found = False
        for i, patient in enumerate(patients):
            if patient.patient_id == self.patient_id:
                patients[i] = self
                found = True
                break
        
        if not found:
            patients.append(self)
        
        # Save all patients back to file
        with open(self.patients_file, "wb") as f:
            pickle.dump(patients, f)
    
    @classmethod
    def load_patients(cls):
        """
        Load all patients from file
        
        Returns:
            list: List of Patient objects
        """
        try:
            with open(cls.patients_file, "rb") as f:
                return pickle.load(f)
        except (FileNotFoundError, EOFError):
            return []
    
    @classmethod
    def get_patient_by_id(cls, patient_id):
        """
        Get a patient by ID
        
        Args:
            patient_id: ID of the patient to find
            
        Returns:
            Patient: Patient object if found, None otherwise
        """
        patients = cls.load_patients()
        for patient in patients:
            if patient.patient_id == patient_id:
                return patient
        return None
    
    @classmethod
    def get_patient_by_email(cls, email):
        """
        Get a patient by email
        
        Args:
            email: Email of the patient to find
            
        Returns:
            Patient: Patient object if found, None otherwise
        """
        patients = cls.load_patients()
        for patient in patients:
            if patient.email == email:
                return patient
        return None
    
    @classmethod
    def delete_patient(cls, patient_id):
        """
        Delete a patient by ID
        
        Args:
            patient_id: ID of the patient to delete
            
        Returns:
            bool: True if deleted, False if not found
        """
        patients = cls.load_patients()
        for i, patient in enumerate(patients):
            if patient.patient_id == patient_id:
                del patients[i]
                with open(cls.patients_file, "wb") as f:
                    pickle.dump(patients, f)
                return True
        return False
