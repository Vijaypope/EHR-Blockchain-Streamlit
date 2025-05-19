import pickle
import os
import hashlib
import uuid
import logging
from datetime import datetime

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.path.join("logs", "ehr_system.log"), mode='a', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('ehr_doctor')

class DoctorError(Exception):
    """Base exception class for Doctor-related errors"""
    pass

class DoctorNotFoundError(DoctorError):
    """Exception raised when a doctor is not found"""
    pass

class DoctorAuthenticationError(DoctorError):
    """Exception raised when authentication fails"""
    pass

class DoctorDataError(DoctorError):
    """Exception raised when there's an issue with doctor data"""
    pass

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
    
    def __init__(self, name, email, specialization, hospital, license_number, contact, doctor_id=None):
        try:
            self.doctor_id = doctor_id if doctor_id else str(uuid.uuid4())
            self.name = name
            self.email = email
            self.specialization = specialization
            self.hospital = hospital
            self.license_number = license_number
            self.contact = contact
            self.password_hash = None
            self.patients = []  # List of patient IDs this doctor has access to
            self.created_at = datetime.now().isoformat()
            self.last_login = None
        except Exception as e:
            logger.error(f"Error initializing Doctor object: {str(e)}")
            raise DoctorDataError(f"Failed to initialize doctor: {str(e)}")

    def set_password(self, password):
        """
        Set the password hash for the doctor
        
        Args:
            password (str): Plain text password to hash
            
        Raises:
            DoctorDataError: If password hashing fails
        """
        try:
            if not password or not isinstance(password, str):
                raise ValueError("Password must be a non-empty string")
            
            # In a real application, use a proper password hashing library like bcrypt
            self.password_hash = hashlib.sha256(password.encode()).hexdigest()
            logger.debug(f"Password set for doctor {self.doctor_id}")
        except Exception as e:
            logger.error(f"Error setting password for doctor {self.doctor_id}: {str(e)}")
            raise DoctorDataError(f"Failed to set password: {str(e)}")
    
    def verify_password(self, password):
        """
        Verify if the provided password matches the stored hash
        
        Args:
            password (str): Password to verify
            
        Returns:
            bool: True if password matches, False otherwise
            
        Raises:
            DoctorAuthenticationError: If password verification fails
        """
        try:
            if not self.password_hash:
                logger.warning(f"Password verification attempted for doctor {self.doctor_id} with no password set")
                return False
                
            return hashlib.sha256(password.encode()).hexdigest() == self.password_hash
        except Exception as e:
            logger.error(f"Error verifying password for doctor {self.doctor_id}: {str(e)}")
            raise DoctorAuthenticationError(f"Failed to verify password: {str(e)}")
    
    def update_last_login(self):
        """
        Update the last login timestamp
        
        Raises:
            DoctorDataError: If updating last login fails
        """
        try:
            self.last_login = datetime.now().isoformat()
            self.save()
            logger.info(f"Updated last login for doctor {self.doctor_id}")
        except Exception as e:
            logger.error(f"Error updating last login for doctor {self.doctor_id}: {str(e)}")
            raise DoctorDataError(f"Failed to update last login: {str(e)}")
    
    def add_patient(self, patient_id):
        """
        Add a patient to the doctor's care
        
        Args:
            patient_id: ID of the patient to add
            
        Returns:
            bool: True if added, False if already in care
            
        Raises:
            DoctorDataError: If adding patient fails
        """
        try:
            if not patient_id:
                raise ValueError("Patient ID cannot be empty")
                
            if patient_id not in self.patients:
                self.patients.append(patient_id)
                self.save()
                logger.info(f"Added patient {patient_id} to doctor {self.doctor_id}")
                return True
            return False
        except Exception as e:
            logger.error(f"Error adding patient {patient_id} to doctor {self.doctor_id}: {str(e)}")
            raise DoctorDataError(f"Failed to add patient: {str(e)}")
    
    def remove_patient(self, patient_id):
        """
        Remove a patient from the doctor's care
        
        Args:
            patient_id: ID of the patient to remove
            
        Returns:
            bool: True if removed, False if not in care
            
        Raises:
            DoctorDataError: If removing patient fails
        """
        try:
            if patient_id in self.patients:
                self.patients.remove(patient_id)
                self.save()
                logger.info(f"Removed patient {patient_id} from doctor {self.doctor_id}")
                return True
            return False
        except Exception as e:
            logger.error(f"Error removing patient {patient_id} from doctor {self.doctor_id}: {str(e)}")
            raise DoctorDataError(f"Failed to remove patient: {str(e)}")
    
    def is_patient_under_care(self, patient_id):
        """
        Check if a patient is under this doctor's care
        
        Args:
            patient_id: ID of the patient to check
            
        Returns:
            bool: True if under care, False otherwise
        """
        try:
            return patient_id in self.patients
        except Exception as e:
            logger.error(f"Error checking if patient {patient_id} is under care of doctor {self.doctor_id}: {str(e)}")
            return False
    
    def to_dict(self):
        """
        Convert doctor object to dictionary for serialization
        
        Returns:
            dict: Doctor data as dictionary
            
        Raises:
            DoctorDataError: If conversion fails
        """
        try:
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
        except Exception as e:
            logger.error(f"Error converting doctor {self.doctor_id} to dictionary: {str(e)}")
            raise DoctorDataError(f"Failed to convert doctor to dictionary: {str(e)}")
    
    @classmethod
    def from_dict(cls, doctor_dict):
        """
        Create doctor object from dictionary
        
        Args:
            doctor_dict (dict): Doctor data as dictionary
            
        Returns:
            Doctor: New doctor object
            
        Raises:
            DoctorDataError: If conversion fails
        """
        try:
            if not isinstance(doctor_dict, dict):
                raise ValueError("Expected dictionary for doctor data")
                
            required_fields = ["name", "email", "specialization", "hospital", 
                              "license_number", "contact", "doctor_id"]
            
            for field in required_fields:
                if field not in doctor_dict:
                    raise ValueError(f"Missing required field: {field}")
            
            doctor = cls(
                doctor_dict["name"],
                doctor_dict["email"],
                doctor_dict["specialization"],
                doctor_dict["hospital"],
                doctor_dict["license_number"],
                doctor_dict["contact"],
                doctor_dict["doctor_id"]
            )
            
            doctor.password_hash = doctor_dict.get("password_hash")
            doctor.patients = doctor_dict.get("patients", [])
            doctor.created_at = doctor_dict.get("created_at", datetime.now().isoformat())
            doctor.last_login = doctor_dict.get("last_login")
            
            return doctor
        except Exception as e:
            logger.error(f"Error creating doctor from dictionary: {str(e)}")
            raise DoctorDataError(f"Failed to create doctor from dictionary: {str(e)}")
    
    def save(self):
        """
        Save doctor to file
        
        Raises:
            DoctorDataError: If saving fails
        """
        try:
            # Create data directory if it doesn't exist
            os.makedirs(os.path.dirname(self.doctors_file), exist_ok=True)
            
            # Create logs directory if it doesn't exist
            os.makedirs("logs", exist_ok=True)
            
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
                
            logger.info(f"Saved doctor {self.doctor_id} to file")
        except Exception as e:
            logger.error(f"Error saving doctor {self.doctor_id} to file: {str(e)}")
            raise DoctorDataError(f"Failed to save doctor: {str(e)}")
    
    @classmethod
    def load_doctors(cls):
        """
        Load all doctors from file
        
        Returns:
            list: List of Doctor objects
        """
        try:
            if not os.path.exists(cls.doctors_file):
                logger.info(f"Doctors file not found, creating new file at {cls.doctors_file}")
                return []
                
            if os.path.getsize(cls.doctors_file) == 0:
                logger.warning(f"Doctors file is empty at {cls.doctors_file}")
                return []
                
            with open(cls.doctors_file, "rb") as f:
                doctors = pickle.load(f)
                
            logger.info(f"Loaded {len(doctors)} doctors from file")
            return doctors
        except (FileNotFoundError, EOFError) as e:
            logger.warning(f"No doctors file found or file is empty: {str(e)}")
            return []
        except (pickle.UnpicklingError, AttributeError) as e:
            # If there's a problem with the pickle file, create a backup
            backup_path = f"{cls.doctors_file}.bak_{datetime.now().strftime('%Y%m%d%H%M%S')}"
            try:
                os.rename(cls.doctors_file, backup_path)
                logger.error(f"Corrupted doctors file backed up to {backup_path}: {str(e)}")
            except Exception as backup_error:
                logger.critical(f"Failed to backup corrupted doctors file: {str(backup_error)}")
            return []
        except Exception as e:
            logger.error(f"Error loading doctors from file: {str(e)}")
            return []
    
    @classmethod
    def get_doctor_by_id(cls, doctor_id):
        """
        Get a doctor by ID
        
        Args:
            doctor_id: ID of the doctor to find
            
        Returns:
            Doctor: Doctor object if found, None otherwise
            
        Raises:
            DoctorNotFoundError: If doctor is not found (optional)
        """
        if not doctor_id:
            logger.error("Doctor ID cannot be empty")
            return None
            
        try:
            doctors = cls.load_doctors()
            for doctor in doctors:
                if doctor.doctor_id == doctor_id:
                    return doctor
                    
            logger.warning(f"Doctor not found with ID: {doctor_id}")
            return None
        except Exception as e:
            logger.error(f"Error getting doctor by ID {doctor_id}: {str(e)}")
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
        if not email:
            logger.error("Email cannot be empty")
            return None
            
        try:
            doctors = cls.load_doctors()
            for doctor in doctors:
                if doctor.email == email:
                    return doctor
                    
            logger.warning(f"Doctor not found with email: {email}")
            return None
        except Exception as e:
            logger.error(f"Error getting doctor by email {email}: {str(e)}")
            return None
    
    @classmethod
    def delete_doctor(cls, doctor_id):
        """
        Delete a doctor by ID
        
        Args:
            doctor_id: ID of the doctor to delete
            
        Returns:
            bool: True if deleted, False if not found
            
        Raises:
            DoctorDataError: If deletion fails
        """
        if not doctor_id:
            logger.error("Doctor ID cannot be empty")
            return False
            
        try:
            doctors = cls.load_doctors()
            original_count = len(doctors)
            
            # Find doctor to delete
            doctor_index = None
            for i, doctor in enumerate(doctors):
                if doctor.doctor_id == doctor_id:
                    doctor_index = i
                    break
            
            if doctor_index is None:
                logger.warning(f"Doctor not found for deletion with ID: {doctor_id}")
                return False
            
            # Remove doctor and save the updated list
            del doctors[doctor_index]
            
            # Create a backup of the current file before writing
            if os.path.exists(cls.doctors_file):
                backup_path = f"{cls.doctors_file}.bak_{datetime.now().strftime('%Y%m%d%H%M%S')}"
                try:
                    import shutil
                    shutil.copy2(cls.doctors_file, backup_path)
                    logger.info(f"Created backup of doctors file at {backup_path}")
                except Exception as backup_error:
                    logger.warning(f"Failed to create backup before deletion: {str(backup_error)}")
            
            # Save the updated list
            with open(cls.doctors_file, "wb") as f:
                pickle.dump(doctors, f)
                
            logger.info(f"Deleted doctor with ID: {doctor_id}")
            return True
        except Exception as e:
            logger.error(f"Error deleting doctor with ID {doctor_id}: {str(e)}")
            raise DoctorDataError(f"Failed to delete doctor: {str(e)}")
