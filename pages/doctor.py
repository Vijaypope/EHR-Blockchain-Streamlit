"""
Doctor dashboard page for the EHR Chain application.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from data.sample_data import PATIENTS, HEALTH_RECORDS, PRESCRIPTIONS, LAB_RESULTS
from utils.auth import get_user_data
from utils.blockchain import Block

def show_doctor_dashboard():
    """Display the doctor dashboard."""
    
    # Get current user data
    user_data = st.session_state.get('user_data', {})
    username = user_data.get('username', '')
    doctor_data = get_user_data(username, 'doctor')
    
    # Main heading
    st.title(f"Welcome, {doctor_data['name']}")
    st.write(f"**Specialization:** {doctor_data['specialization']} | **Hospital:** {doctor_data['hospital']}")
    
    # Create tabs for different sections
    tabs = st.tabs(["Patients", "Health Records", "Blockchain", "Add Record"])
    
    # Patients tab
    with tabs[0]:
        show_patients_tab()
    
    # Health Records tab  
    with tabs[1]:
        show_health_records_tab()
    
    # Blockchain tab
    with tabs[2]:
        show_blockchain_tab()
    
    # Add Record tab
    with tabs[3]:
        show_add_record_tab()

def show_patients_tab():
    """Display the patients tab content."""
    st.header("My Patients")
    
    # Convert sample patients data to a DataFrame
    patients_df = pd.DataFrame(PATIENTS)
    
    # Add a "View Details" button column
    patients_df['Action'] = ['View Details' for _ in range(len(patients_df))]
    
    # Display the patients table
    selected_indices = st.dataframe(
        patients_df[['id', 'name', 'age', 'gender', 'blood_type', 'Action']],
        column_config={
            "Action": st.column_config.ButtonColumn()
        },
        hide_index=True
    )
    
    # Handle button clicks
    if selected_indices:
        row_index = selected_indices.last_clicked_row_id
        if row_index is not None:
            patient_id = patients_df.iloc[row_index]['id']
            st.session_state['selected_patient'] = patient_id
            
            # Find the selected patient
            patient = next((p for p in PATIENTS if p['id'] == patient_id), None)
            
            if patient:
                st.subheader(f"Patient Details: {patient['name']}")
                
                # Display patient information in columns
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**ID:** {patient['id']}")
                    st.write(f"**Age:** {patient['age']}")
                    st.write(f"**Gender:** {patient['gender']}")
                
                with col2:
                    st.write(f"**Blood Type:** {patient['blood_type']}")
                    st.write(f"**Allergies:** {', '.join(patient['allergies']) if patient['allergies'] else 'None'}")
                    st.write(f"**Conditions:** {', '.join(patient['conditions'])}")
                
                # Get patient records
                patient_records = [r for r in HEALTH_RECORDS if r['patient_id'] == patient_id]
                if patient_records:
                    st.subheader("Recent Health Records")
                    records_df = pd.DataFrame(patient_records)
                    st.dataframe(records_df[['date', 'diagnosis', 'notes']], hide_index=True)
                
                # Get patient prescriptions
                patient_prescriptions = [p for p in PRESCRIPTIONS if p['patient_id'] == patient_id]
                if patient_prescriptions:
                    st.subheader("Active Prescriptions")
                    for prescription in patient_prescriptions:
                        st.write(f"**Date:** {prescription['date_prescribed']}")
                        for med in prescription['medications']:
                            st.write(f"- {med['name']} {med['dosage']}, {med['frequency']}, {med['duration']}")
                        st.write(f"**Notes:** {prescription['notes']}")
                        st.divider()
                
                # Get patient lab results
                patient_labs = [l for l in LAB_RESULTS if l['patient_id'] == patient_id]
                if patient_labs:
                    st.subheader("Lab Results")
                    for lab in patient_labs:
                        st.write(f"**Date:** {lab['date']} | **Test:** {lab['test_type']}")
                        for test, result in lab['results'].items():
                            st.write(f"- {test.replace('_', ' ').title()}: {result}")
                        st.write(f"**Notes:** {lab['notes']}")
                        st.divider()

def show_health_records_tab():
    """Display the health records tab content."""
    st.header("All Health Records")
    
    # Convert sample health records to a DataFrame
    records_df = pd.DataFrame(HEALTH_RECORDS)
    
    # Map patient IDs to patient names
    patient_map = {p['id']: p['name'] for p in PATIENTS}
    records_df['patient_name'] = records_df['patient_id'].map(patient_map)
    
    # Display the records table
    st.dataframe(
        records_df[['record_id', 'patient_name', 'date', 'diagnosis']],
        hide_index=True
    )
    
    # Basic analytics
    st.subheader("Health Records Analytics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Count records by diagnosis
        diagnosis_counts = records_df['diagnosis'].value_counts().reset_index()
        diagnosis_counts.columns = ['Diagnosis', 'Count']
        
        fig = px.pie(
            diagnosis_counts,
            names='Diagnosis',
            values='Count',
            title='Diagnosis Distribution',
            color_discrete_sequence=px.colors.sequential.RdBu
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # Records over time
        records_df['date'] = pd.to_datetime(records_df['date'])
        records_over_time = records_df.groupby(records_df['date'].dt.to_period("M")).size().reset_index(name='count')
        records_over_time['date'] = records_over_time['date'].dt.to_timestamp()

        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(
            x=records_over_time['date'],
            y=records_over_time['count'],
            mode='lines+markers',
            name='Records'
        ))
        fig2.update_layout(title='Records Over Time', xaxis_title='Date', yaxis_title='Number of Records')
        st.plotly_chart(fig2, use_container_width=True)
