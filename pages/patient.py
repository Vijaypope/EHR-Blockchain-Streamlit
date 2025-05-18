import streamlit as st
import pandas as pd
import hashlib
import json
from datetime import datetime
import uuid
import os
import pickle

class Patient:
    def __init__(self):
        self.patient_data_file = "data/patients.pkl"
        self.ensure_data_directory()
        self.load_patient_data()
    
    def ensure_data_directory(self):
        """Ensure the data directory exists"""
        os.makedirs("data", exist_ok=True)
    
    def load_patient_data(self):
        """Load patient data from pickle file or create new dataframe if file doesn't exist"""
        try:
            with open(self.patient_data_file, 'rb') as file:
                self.patients_df = pickle.load(file)
        except (FileNotFoundError, EOFError):
            # Create empty DataFrame with specified columns
            self.patients_df = pd.DataFrame(
                columns=['patient_id', 'full_name', 'date_of_birth', 'gender', 
                         'contact_number', 'email', 'address', 'blood_group', 
                         'allergies', 'medical_history', 'registration_date', 
                         'emergency_contact', 'insurance_details', 'hash']
            )
    
    def save_patient_data(self):
        """Save patient data to pickle file"""
        with open(self.patient_data_file, 'wb') as file:
            pickle.dump(self.patients_df, file)
    
    def generate_patient_id(self):
        """Generate a unique patient ID"""
        return str(uuid.uuid4())[:8].upper()
    
    def compute_hash(self, patient_data):
        """Compute SHA-256 hash of patient data"""
        data_string = json.dumps(patient_data, sort_keys=True)
        return hashlib.sha256(data_string.encode()).hexdigest()
    
    def add_patient(self, patient_data):
        """Add a new patient to the system"""
        patient_id = self.generate_patient_id()
        patient_data['patient_id'] = patient_id
        patient_data['registration_date'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Compute hash of patient data for integrity
        hash_value = self.compute_hash(patient_data)
        patient_data['hash'] = hash_value
        
        # Add to DataFrame
        self.patients_df = pd.concat([self.patients_df, pd.DataFrame([patient_data])], ignore_index=True)
        self.save_patient_data()
        return patient_id
    
    def get_patient(self, patient_id):
        """Get patient data by ID"""
        patient = self.patients_df[self.patients_df['patient_id'] == patient_id]
        if len(patient) > 0:
            return patient.iloc[0].to_dict()
        return None
    
    def update_patient(self, patient_id, updated_data):
        """Update patient information"""
        idx = self.patients_df[self.patients_df['patient_id'] == patient_id].index
        if len(idx) > 0:
            for key, value in updated_data.items():
                if key in self.patients_df.columns and key not in ['patient_id', 'registration_date', 'hash']:
                    self.patients_df.loc[idx[0], key] = value
            
            # Update hash
            patient_data = self.get_patient(patient_id)
            hash_value = self.compute_hash(patient_data)
            self.patients_df.loc[idx[0], 'hash'] = hash_value
            
            self.save_patient_data()
            return True
        return False
    
    def delete_patient(self, patient_id):
        """Delete a patient from the system"""
        idx = self.patients_df[self.patients_df['patient_id'] == patient_id].index
        if len(idx) > 0:
            self.patients_df = self.patients_df.drop(idx[0])
            self.save_patient_data()
            return True
        return False
    
    def get_all_patients(self):
        """Get all patients data"""
        return self.patients_df

# Patient Dashboard Functions
def show_patient_dashboard():
    st.title("Patient Dashboard")
    
    # Initialize patient manager
    patient_manager = Patient()
    
    # Get current user's patient ID
    # For demo, we're using the username as patient ID
    current_patient_id = st.session_state['user_data']['username']
    
    # Fetch patient data
    patient_data = patient_manager.get_patient(current_patient_id)
    
    # If patient doesn't exist, create a demo profile
    if patient_data is None:
        patient_data = {
            'patient_id': current_patient_id,
            'full_name': 'Demo Patient',
            'date_of_birth': '1990-01-01',
            'gender': 'Not specified',
            'contact_number': '+1234567890',
            'email': 'demo@example.com',
            'address': '123 Health Street',
            'blood_group': 'O+',
            'allergies': 'None',
            'medical_history': 'No major illness',
            'registration_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'emergency_contact': 'Emergency Contact: +1987654320',
            'insurance_details': 'Insurance ID: INS123456'
        }
        # Compute hash
        hash_value = patient_manager.compute_hash(patient_data)
        patient_data['hash'] = hash_value
        
        # Add to DataFrame (for demo purposes)
        if current_patient_id not in patient_manager.patients_df['patient_id'].values:
            patient_manager.patients_df = pd.concat([patient_manager.patients_df, pd.DataFrame([patient_data])], ignore_index=True)
            patient_manager.save_patient_data()
    
    # Create tabs for different sections
    tab1, tab2, tab3 = st.tabs(["My Profile", "Medical Records", "Health Data"])
    
    with tab1:
        st.header("Patient Profile")
        
        # Display patient information
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Personal Information")
            st.write(f"**ID:** {patient_data['patient_id']}")
            st.write(f"**Name:** {patient_data['full_name']}")
            st.write(f"**Date of Birth:** {patient_data['date_of_birth']}")
            st.write(f"**Gender:** {patient_data['gender']}")
            st.write(f"**Blood Group:** {patient_data['blood_group']}")
            
        with col2:
            st.subheader("Contact Information")
            st.write(f"**Phone:** {patient_data['contact_number']}")
            st.write(f"**Email:** {patient_data['email']}")
            st.write(f"**Address:** {patient_data['address']}")
            st.write(f"**Emergency Contact:** {patient_data['emergency_contact']}")
        
        with st.expander("Medical Information"):
            st.write(f"**Allergies:** {patient_data['allergies']}")
            st.write(f"**Medical History:** {patient_data['medical_history']}")
            st.write(f"**Insurance Details:** {patient_data['insurance_details']}")
        
        with st.expander("Block Verification"):
            st.write("Your health record is secured with blockchain technology.")
            st.write(f"**Record Hash:** {patient_data['hash'][:15]}...{patient_data['hash'][-15:]}")
            if st.button("Verify Record Integrity"):
                # Re-compute hash and verify
                current_hash = patient_data['hash']
                verification_data = patient_data.copy()
                del verification_data['hash']  # Remove hash for verification
                computed_hash = patient_manager.compute_hash(verification_data)
                
                if computed_hash == current_hash:
                    st.success("✅ Record integrity verified successfully!")
                else:
                    st.error("⚠️ Record integrity verification failed!")
    
    with tab2:
        st.header("Medical Records")
        
        # Demo data for medical records
        records = [
            {"date": "2023-09-15", "doctor": "Dr. Smith", "diagnosis": "Annual checkup", "prescription": "Vitamin D supplements"},
            {"date": "2023-06-02", "doctor": "Dr. Johnson", "diagnosis": "Flu", "prescription": "Oseltamivir 75mg"}
        ]
        
        for i, record in enumerate(records):
            with st.expander(f"Visit: {record['date']} - {record['diagnosis']}"):
                st.write(f"**Date:** {record['date']}")
                st.write(f"**Doctor:** {record['doctor']}")
                st.write(f"**Diagnosis:** {record['diagnosis']}")
                st.write(f"**Prescription:** {record['prescription']}")
                st.write("---")
                
                # Option to download record
                if st.button("Download Record", key=f"download_{i}"):
                    st.info("Download functionality would be implemented here.")
    
    with tab3:
        st.header("Health Metrics")
        
        # Create some demo health data
        dates = pd.date_range(start='1/1/2023', periods=10, freq='M')
        blood_pressure = [f"{120+i}/{80+i//2}" for i in range(10)]
        weight = [70 + round(i/5, 1) for i in range(10)]
        blood_sugar = [95 + i for i in range(10)]
        
        health_data = pd.DataFrame({
            'Date': dates,
            'Blood Pressure': blood_pressure,
            'Weight (kg)': weight,
            'Blood Sugar (mg/dL)': blood_sugar
        })
        
        # Display the health metrics
        st.subheader("Health Metrics Over Time")
        st.dataframe(health_data)
        
        # Simple visualization
        st.subheader("Weight Trend")
        st.line_chart(health_data.set_index('Date')['Weight (kg)'])
        
        st.subheader("Blood Sugar Trend")
        st.line_chart(health_data.set_index('Date')['Blood Sugar (mg/dL)'])

if __name__ == "__main__":
    # This will only run if the script is executed directly, not when imported
    st.title("Patient Module Test Page")
    show_patient_dashboard()
