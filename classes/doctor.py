import pickle
import hashlib
import time
import uuid
from datetime import datetime
from typing import Dict, List, Any, Optional

class Doctor:
    """
    Doctor class to manage doctor information and actions in the EHR blockchain system.
    """
    def __init__(self, 
                 doctor_id: str = None, 
                 name: str = None, 
                 specialization: str = None, 
                 hospital: str = None, 
                 contact: str = None, 
                 email: str = None, 
                 password: str = None,
                 license_number: str = None):
        """
        Initialize a new Doctor.
        
        Args:
            doctor_id: Unique ID for the doctor, auto-generated if None
            name: Doctor's full name
            specialization: Doctor's specialization/department
            hospital: Hospital or clinic affiliation
            contact: Contact number
            email: Email address
            password: Password (will be hashed)
            license_number: Medical license number
        """
        self.doctor_id = doctor_id or str(uuid.uuid4())
        self.name = name
        self.specialization = specialization
        self.hospital = hospital
        self.contact = contact
        self.email = email
        self.password = self._hash_password(password) if password else None
        self.license_number = license_number
        self.patients: List[str] = []  # List of patient IDs under this doctor
        self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.last_login = None
        
    def _hash_password(self, password: str) -> str:
        """Hash a password for storing."""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def verify_password(self, password: str) -> bool:
        """Verify a stored password against the provided password."""
        return self._hash_password(password) == self.password
    
    def update_info(self, 
                    name: str = None, 
                    specialization: str = None, 
                    hospital: str = None, 
                    contact: str = None, 
                    email: str = None) -> None:
        """Update doctor information."""
        if name:
            self.name = name
        if specialization:
            self.specialization = specialization
        if hospital:
            self.hospital = hospital
        if contact:
            self.contact = contact
        if email:
            self.email = email
    
    def change_password(self, old_password: str, new_password: str) -> bool:
        """Change the doctor's password."""
        if self.verify_password(old_password):
            self.password = self._hash_password(new_password)
            return True
        return False
    
    def add_patient(self, patient_id: str) -> None:
        """Add a patient to the doctor's patient list."""
        if patient_id not in self.patients:
            self.patients.append(patient_id)
    
    def remove_patient(self, patient_id: str) -> bool:
        """Remove a patient from the doctor's patient list."""
        if patient_id in self.patients:
            self.patients.remove(patient_id)
            return True
        return False
    
    def update_last_login(self) -> None:
        """Update the doctor's last login timestamp."""
        self.last_login = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert doctor object to dictionary."""
        return {
            "doctor_id": self.doctor_id,
            "name": self.name,
            "specialization": self.specialization,
            "hospital": self.hospital,
            "contact": self.contact,
            "email": self.email,
            "password": self.password,
            "license_number": self.license_number,
            "patients": self.patients,
            "created_at": self.created_at,
            "last_login": self.last_login
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Doctor':
        """Create a Doctor object from a dictionary."""
        doctor = cls(
            doctor_id=data.get("doctor_id"),
            name=data.get("name"),
            specialization=data.get("specialization"),
            hospital=data.get("hospital"),
            contact=data.get("contact"),
            email=data.get("email"),
            license_number=data.get("license_number")
        )
        doctor.password = data.get("password")
        doctor.patients = data.get("patients", [])
        doctor.created_at = data.get("created_at")
        doctor.last_login = data.get("last_login")
        return doctor
    
    @staticmethod
    def load_doctors() -> Dict[str, 'Doctor']:
        """Load all doctors from the pickle file."""
        try:
            with open("data/doctors.pkl", "rb") as f:
                return pickle.load(f)
        except (FileNotFoundError, EOFError):
            return {}
    
    @staticmethod
    def save_doctors(doctors: Dict[str, 'Doctor']) -> None:
        """Save all doctors to the pickle file."""
        with open("data/doctors.pkl", "wb") as f:
            pickle.dump(doctors, f)
    
    def save(self) -> None:
        """Save the current doctor to the doctors.pkl file."""
        doctors = self.load_doctors()
        doctors[self.doctor_id] = self
        self.save_doctors(doctors)
    
    @classmethod
    def get_doctor_by_id(cls, doctor_id: str) -> Optional['Doctor']:
        """Get a doctor by ID."""
        doctors = cls.load_doctors()
        return doctors.get(doctor_id)
    
    @classmethod
    def get_doctor_by_email(cls, email: str) -> Optional['Doctor']:
        """Get a doctor by email."""
        doctors = cls.load_doctors()
        for doctor in doctors.values():
            if doctor.email == email:
                return doctor
        return Non
