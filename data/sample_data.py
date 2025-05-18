"""
Sample data for the EHR Chain application.
"""

# Sample patients data
PATIENTS = [
    {
        "id": "P001",
        "name": "John Smith",
        "age": 42,
        "gender": "Male",
        "blood_type": "A+",
        "allergies": ["Penicillin", "Peanuts"],
        "conditions": ["Hypertension", "Type 2 Diabetes"]
    },
    {
        "id": "P002",
        "name": "Sarah Johnson",
        "age": 35,
        "gender": "Female",
        "blood_type": "O-",
        "allergies": ["Sulfa drugs"],
        "conditions": ["Asthma"]
    },
    {
        "id": "P003",
        "name": "Robert Chen",
        "age": 68,
        "gender": "Male",
        "blood_type": "B+",
        "allergies": ["Latex"],
        "conditions": ["Osteoarthritis", "Coronary Artery Disease"]
    },
    {
        "id": "P004",
        "name": "Emily Williams",
        "age": 29,
        "gender": "Female",
        "blood_type": "AB+",
        "allergies": [],
        "conditions": ["Migraine"]
    }
]

# Sample doctors data
DOCTORS = [
    {
        "id": "D001",
        "name": "Dr. Sarah Johnson",
        "specialization": "Cardiologist",
        "hospital": "City General Hospital",
        "license": "MD12345",
        "patients": ["P001", "P003"]
    },
    {
        "id": "D002",
        "name": "Dr. Michael Lee",
        "specialization": "Pediatrician",
        "hospital": "Children's Medical Center",
        "license": "MD67890",
        "patients": ["P004"]
    },
    {
        "id": "D003",
        "name": "Dr. Rachel Kim",
        "specialization": "Neurologist",
        "hospital": "University Medical Center",
        "license": "MD24680",
        "patients": ["P002"]
    }
]

# Sample health records
HEALTH_RECORDS = [
    {
        "record_id": "R001",
        "patient_id": "P001",
        "doctor_id": "D001",
        "date": "2023-01-15",
        "diagnosis": "Hypertension",
        "notes": "Blood pressure remains high at 150/90. Increasing medication dosage.",
        "medications": ["Lisinopril 20mg", "Amlodipine 5mg"],
        "vital_signs": {
            "blood_pressure": "150/90",
            "heart_rate": 78,
            "temperature": 98.6,
            "respiratory_rate": 16,
            "oxygen_saturation": 97
        }
    },
    {
        "record_id": "R002",
        "patient_id": "P002",
        "doctor_id": "D003",
        "date": "2023-02-22",
        "diagnosis": "Acute asthma exacerbation",
        "notes": "Patient presented with wheezing and shortness of breath. Responding well to nebulizer treatment.",
        "medications": ["Albuterol nebulizer", "Prednisone 40mg taper"],
        "vital_signs": {
            "blood_pressure": "125/75",
            "heart_rate": 92,
            "temperature": 99.1,
            "respiratory_rate": 22,
            "oxygen_saturation": 94
        }
    },
    {
        "record_id": "R003",
        "patient_id": "P003",
        "doctor_id": "D001",
        "date": "2023-03-10",
        "diagnosis": "Stable coronary artery disease",
        "notes": "Regular check-up shows stable condition. EKG normal. Continuing current medication regimen.",
        "medications": ["Aspirin 81mg", "Atorvastatin 40mg", "Metoprolol 25mg"],
        "vital_signs": {
            "blood_pressure": "132/78",
            "heart_rate": 65,
            "temperature": 98.4,
            "respiratory_rate": 14,
            "oxygen_saturation": 96
        }
    },
    {
        "record_id": "R004",
        "patient_id": "P004",
        "doctor_id": "D002",
        "date": "2023-04-05",
        "diagnosis": "Migraine without aura",
        "notes": "Patient reports 3 episodes in the past month. Discussing preventative options.",
        "medications": ["Sumatriptan 50mg as needed", "Propranolol 40mg daily"],
        "vital_signs": {
            "blood_pressure": "118/72",
            "heart_rate": 68,
            "temperature": 98.2,
            "respiratory_rate": 16,
            "oxygen_saturation": 99
        }
    }
]

# Sample prescriptions data
PRESCRIPTIONS = [
    {
        "prescription_id": "Rx001",
        "patient_id": "P001",
        "doctor_id": "D001",
        "date_prescribed": "2023-01-15",
        "medications": [
            {
                "name": "Lisinopril",
                "dosage": "20mg",
                "frequency": "Once daily",
                "duration": "90 days"
            },
            {
                "name": "Amlodipine",
                "dosage": "5mg",
                "frequency": "Once daily",
                "duration": "90 days"
            }
        ],
        "notes": "Take with food in the morning."
    },
    {
        "prescription_id": "Rx002",
        "patient_id": "P002",
        "doctor_id": "D003",
        "date_prescribed": "2023-02-22",
        "medications": [
            {
                "name": "Albuterol",
                "dosage": "2.5mg",
                "frequency": "Every 4-6 hours as needed",
                "duration": "PRN"
            },
            {
                "name": "Prednisone",
                "dosage": "40mg tapering dose",
                "frequency": "See instructions",
                "duration": "5 days"
            }
        ],
        "notes": "Prednisone taper: 40mg for 2 days, then 20mg for 2 days, then 10mg for 1 day."
    }
]

# Sample lab results
LAB_RESULTS = [
    {
        "lab_id": "L001",
        "patient_id": "P001",
        "doctor_id": "D001",
        "date": "2023-01-12",
        "test_type": "Comprehensive Metabolic Panel",
        "results": {
            "glucose": "126 mg/dL",
            "creatinine": "0.9 mg/dL",
            "potassium": "4.2 mEq/L",
            "sodium": "140 mEq/L",
            "calcium": "9.5 mg/dL"
        },
        "notes": "Glucose levels are elevated, consistent with diabetes diagnosis."
    },
    {
        "lab_id": "L002",
        "patient_id": "P003",
        "doctor_id": "D001",
        "date": "2023-03-05",
        "test_type": "Lipid Panel",
        "results": {
            "total_cholesterol": "210 mg/dL",
            "ldl": "130 mg/dL",
            "hdl": "45 mg/dL",
            "triglycerides": "175 mg/dL"
        },
        "notes": "Borderline high cholesterol. Recommend dietary changes and follow-up in 3 months."
    }
]
