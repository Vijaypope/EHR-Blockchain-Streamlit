import streamlit as st
import pandas as pd
from datetime import datetime
import random
import uuid

# Sample patient data for demo purposes
def generate_sample_patients(num=10):
    patients = []
    for i in range(num):
        patient_id = str(uuid.uuid4())[:8]
        patient = {
            'id': patient_id,
            'name': f"Patient {i+1}",
            'age': random.randint(18, 80),
            'gender': random.choice(['Male', 'Female']),
            'blood_type': random.choice(['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']),
            'Action': 'View'
        }
        patients.append(patient)
    return pd.DataFrame(patients)

# Sample medical records for demo purposes
def generate_sample_records(num=5):
    records = []
    for i in range(num):
        record = {
            'id': str(uuid.uuid4())[:8],
            'patient_name': f"Patient {random.randint(1, 10)}",
            'date': (datetime.now().date().replace(day=random.randint(1, 28))).strftime('%Y-%m-%d'),
            'diagnosis': random.choice(['Hypertension', 'Diabetes', 'Asthma', 'Influenza', 'COVID-19']),
            'treatment': random.choice(['Medication', 'Surgery', 'Therapy', 'Monitoring', 'Referral']),
            'doctor': f"Dr. {random.choice(['Smith', 'Johnson', 'Williams', 'Brown', 'Jones'])}"
        }
        records.append(record)
    return pd.DataFrame(records)

# Function to display patients tab
def show_patients_tab():
    st.header("Patient Management")
    
    # Generate sample patient data
    patients_df = generate_sample_patients()
    
    # Search and filter
    col1, col2 = st.columns([3, 1])
    with col1:
        search_term = st.text_input("Search patients", "")
    with col2:
        st.write(" ")
        st.write(" ")
        add_patient_button = st.button("Add New Patient")
    
    # Filter patients based on search term
    if search_term:
        filtered_df = patients_df[patients_df['name'].str.contains(search_term, case=False) | 
                               patients_df['id'].str.contains(search_term, case=False)]
    else:
        filtered_df = patients_df
    
    # Display patient list with action buttons
    st.subheader("Patient List")
    
    # Using a workaround for ButtonColumn since it's not available in Streamlit 1.28.0
    # Display the dataframe
    st.dataframe(
        filtered_df[['id', 'name', 'age', 'gender', 'blood_type']],
        hide_index=True
    )
    
    # Add separate selection for patient details
    selected_patient_id = st.selectbox(
        "Select patient to view details:",
        options=filtered_df['id'].tolist(),
        format_func=lambda x: f"{x} - {filtered_df[filtered_df['id']==x]['name'].values[0]}"
    )
    
    if selected_patient_id and st.button("View Patient Details"):
        # Get the selected patient
        selected_patient = filtered_df[filtered_df['id'] == selected_patient_id].iloc[0]
        
        # Display patient details
        st.subheader(f"Patient Details: {selected_patient['name']}")
        
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"**ID:** {selected_patient['id']}")
            st.write(f"**Name:** {selected_patient['name']}")
            st.write(f"**Age:** {selected_patient['age']}")
        
        with col2:
            st.write(f"**Gender:** {selected_patient['gender']}")
            st.write(f"**Blood Type:** {selected_patient['blood_type']}")
        
        # Medical records for this patient
        st.subheader("Medical Records")
        
        # Generate some random records for this patient
        records = pd.DataFrame([
            {"date": "2023-09-15", "diagnosis": "Annual checkup", "doctor": "Dr. Smith", "notes": "Patient is in good health"},
            {"date": "2023-06-02", "diagnosis": "Flu", "doctor": "Dr. Johnson", "notes": "Prescribed Oseltamivir"}
        ])
        
        st.dataframe(records, hide_index=True)

# Function to display health records tab
def show_health_records_tab():
    st.header("Health Records")
    
    # Generate sample health records
    records_df = generate_sample_records()
    
    # Search and filter
    search_term = st.text_input("Search records", "")
    
    # Filter records based on search term
    if search_term:
        filtered_df = records_df[records_df['patient_name'].str.contains(search_term, case=False) | 
                              records_df['diagnosis'].str.contains(search_term, case=False) |
                              records_df['doctor'].str.contains(search_term, case=False)]
    else:
        filtered_df = records_df
        
    # Add new record button
    if st.button("Add New Record"):
        st.session_state['show_add_record_form'] = True
    
    # Display records
    st.dataframe(filtered_df, hide_index=True)
    
    # Add record form (conditionally shown)
    if st.session_state.get('show_add_record_form', False):
        st.subheader("Add New Health Record")
        
        # Form for adding new record
        with st.form("add_record_form"):
            # Patient selection (should be linked to patient database in real app)
            patient_name = st.selectbox("Patient", ["Patient " + str(i) for i in range(1, 11)])
            date = st.date_input("Date")
            diagnosis = st.text_input("Diagnosis")
            treatment = st.text_input("Treatment")
            doctor = st.text_input("Doctor", value=f"Dr. {random.choice(['Smith', 'Johnson', 'Williams'])}")
            
            # Submit button
            submitted = st.form_submit_button("Save Record")
            if submitted:
                st.success("Record saved successfully!")
                st.session_state['show_add_record_form'] = False
                st.experimental_rerun()  # TODO: Replace with st.rerun() in newer versions

# Function to display blockchain tab
def show_blockchain_tab():
    st.header("Blockchain Explorer")
    
    # Display blockchain info
    st.subheader("Blockchain Information")
    
    # If blockchain is available in session state
    if 'blockchain' in st.session_state:
        blockchain = st.session_state['blockchain']
        
        # Display blockchain stats
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Blocks", len(blockchain.chain))
        with col2:
            st.metric("Last Updated", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        with col3:
            st.metric("Status", "Healthy")
        
        # Display blocks
        st.subheader("Blocks")
        for i, block in enumerate(blockchain.chain):
            with st.expander(f"Block #{i} - {block.timestamp}"):
                st.write(f"**Previous Hash:** {block.previous_hash}")
                st.write(f"**Hash:** {block.hash}")
                st.write(f"**Timestamp:** {block.timestamp}")
                st.write(f"**Data:** {block.data}")
    else:
        st.warning("Blockchain not initialized or available.")

# Main function to display doctor dashboard
def show_doctor_dashboard():
    st.title("Doctor Dashboard")
    
    # Initialize session state for add record form
    if 'show_add_record_form' not in st.session_state:
        st.session_state['show_add_record_form'] = False
    
    # Create tabs
    tabs = st.tabs(["Patients", "Health Records", "Blockchain"])
    
    # Patients tab
    with tabs[0]:
        show_patients_tab()
    
    # Health Records tab
    with tabs[1]:
        show_health_records_tab()
    
    # Blockchain tab
    with tabs[2]:
        show_blockchain_tab()

if __name__ == "__main__":
    # This allows testing this module independently
    st.set_page_config(page_title="EHR Chain - Doctor Dashboard", layout="wide")
    show_doctor_dashboard()
