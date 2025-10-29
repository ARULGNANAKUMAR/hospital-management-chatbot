from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime, timedelta
import hashlib
import random
import json
from typing import Optional

app = FastAPI(title="Hospital Management System API")

# CORS - Un new frontend URL add pannu
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://arulgnanakumar.github.io",  # UN NEW FRONTEND URL
        "https://ehzaan-ahamed.github.io",   # Old URL (backup)
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:8000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# [REST OF THE BACKEND CODE SAME AS BEFORE - FULL CODE]
# In-memory database with more data
hospital_db = {
    "users": {
        "admin": [
            {"username": "arul", "password": hashlib.sha256("arul".encode()).hexdigest(), "name": "Arul Gnanakumar", "role": "admin", "email": "arul@hospital.com"}
        ],
        "doctor": [
            {"username": "doc_raj", "password": hashlib.sha256("doctor123".encode()).hexdigest(), "name": "Dr. Raj Kumar", "role": "doctor", "specialization": "Cardiology", "experience": "10 years"},
            {"username": "doc_priya", "password": hashlib.sha256("doctor123".encode()).hexdigest(), "name": "Dr. Priya Sharma", "role": "doctor", "specialization": "Neurology", "experience": "8 years"},
            {"username": "doc_amit", "password": hashlib.sha256("doctor123".encode()).hexdigest(), "name": "Dr. Amit Patel", "role": "doctor", "specialization": "Orthopedics", "experience": "12 years"}
        ],
        "nurse": [
            {"username": "nurse_priya", "password": hashlib.sha256("nurse123".encode()).hexdigest(), "name": "Nurse Priya", "role": "nurse", "department": "General Ward", "shift": "Morning"},
            {"username": "nurse_anita", "password": hashlib.sha256("nurse123".encode()).hexdigest(), "name": "Nurse Anita", "role": "nurse", "department": "ICU", "shift": "Night"},
            {"username": "nurse_ravi", "password": hashlib.sha256("nurse123".encode()).hexdigest(), "name": "Nurse Ravi", "role": "nurse", "department": "Emergency", "shift": "Evening"}
        ],
        "patient": [
            {"username": "patient_ram", "password": hashlib.sha256("patient123".encode()).hexdigest(), "name": "Ramesh Kumar", "role": "patient", "condition": "Hypertension", "age": 45},
            {"username": "patient_sita", "password": hashlib.sha256("patient123".encode()).hexdigest(), "name": "Sita Raman", "role": "patient", "condition": "Migraine", "age": 32},
            {"username": "patient_amit", "password": hashlib.sha256("patient123".encode()).hexdigest(), "name": "Amit Singh", "role": "patient", "condition": "Diabetes", "age": 55}
        ]
    },
    "patients": [
        {
            "patient_id": "PAT_001",
            "name": "Ramesh Kumar",
            "age": 45,
            "gender": "Male",
            "contact": "+91-9876543210",
            "condition": "Hypertension",
            "admission_date": "2024-01-15",
            "doctor": "Dr. Raj Kumar",
            "room": "101-A",
            "status": "Admitted"
        },
        {
            "patient_id": "PAT_002", 
            "name": "Sita Raman",
            "age": 32,
            "gender": "Female",
            "contact": "+91-9876543211",
            "condition": "Migraine",
            "admission_date": "2024-01-16",
            "doctor": "Dr. Priya Sharma",
            "room": "205-B",
            "status": "Admitted"
        },
        {
            "patient_id": "PAT_003",
            "name": "Amit Singh",
            "age": 55,
            "gender": "Male", 
            "contact": "+91-9876543212",
            "condition": "Diabetes",
            "admission_date": "2024-01-10",
            "doctor": "Dr. Amit Patel",
            "room": "301-C",
            "status": "Discharged"
        }
    ],
    "appointments": [
        {
            "appointment_id": "APT_001",
            "patient_name": "Ramesh Kumar",
            "doctor_name": "Dr. Raj Kumar",
            "date": "2024-01-20",
            "time": "10:00 AM",
            "department": "Cardiology",
            "status": "Confirmed"
        },
        {
            "appointment_id": "APT_002",
            "patient_name": "Sita Raman",
            "doctor_name": "Dr. Priya Sharma", 
            "date": "2024-01-21",
            "time": "11:00 AM",
            "department": "Neurology",
            "status": "Pending"
        }
    ],
    "prescriptions": [
        {
            "prescription_id": "PRES_001",
            "patient_id": "PAT_001",
            "patient_name": "Ramesh Kumar",
            "doctor_name": "Dr. Raj Kumar",
            "medicines": [
                {"name": "Aspirin", "dosage": "75mg", "frequency": "Once daily", "duration": "30 days"},
                {"name": "Atorvastatin", "dosage": "20mg", "frequency": "Once at night", "duration": "30 days"}
            ],
            "diagnosis": "Hypertension",
            "date": "2024-01-18"
        },
        {
            "prescription_id": "PRES_002",
            "patient_id": "PAT_002",
            "patient_name": "Sita Raman",
            "doctor_name": "Dr. Priya Sharma",
            "medicines": [
                {"name": "Paracetamol", "dosage": "500mg", "frequency": "When required", "duration": "7 days"}
            ],
            "diagnosis": "Migraine",
            "date": "2024-01-17"
        }
    ],
    "medical_records": [
        {
            "record_id": "MR_001",
            "patient_id": "PAT_001",
            "patient_name": "Ramesh Kumar",
            "doctor_name": "Dr. Raj Kumar",
            "visit_date": "2024-01-18",
            "symptoms": "High BP, Headache",
            "diagnosis": "Hypertension Stage 1",
            "treatment": "Medication and lifestyle changes",
            "next_appointment": "2024-02-18"
        }
    ]
}

# Enhanced hospital data for AI responses
hospital_data = {
    "doctors": [
        {
            "name": "Dr. Raj Kumar",
            "specialization": "Cardiology", 
            "experience": "10 years",
            "qualification": "MD, DM Cardiology",
            "availability": ["Monday", "Wednesday", "Friday"],
            "contact": "doc.raj@hospital.com",
            "phone": "044-1234001",
            "consultation_fee": "₹500"
        },
        {
            "name": "Dr. Priya Sharma",
            "specialization": "Neurology",
            "experience": "8 years", 
            "qualification": "MD, DM Neurology",
            "availability": ["Tuesday", "Thursday", "Saturday"],
            "contact": "doc.priya@hospital.com",
            "phone": "044-1234002",
            "consultation_fee": "₹600"
        },
        {
            "name": "Dr. Amit Patel",
            "specialization": "Orthopedics",
            "experience": "12 years",
            "qualification": "MS Orthopedics", 
            "availability": ["Monday", "Tuesday", "Friday"],
            "contact": "doc.amit@hospital.com",
            "phone": "044-1234003",
            "consultation_fee": "₹700"
        },
        {
            "name": "Dr. Sunita Reddy",
            "specialization": "Pediatrics",
            "experience": "9 years",
            "qualification": "MD Pediatrics",
            "availability": ["Wednesday", "Thursday", "Saturday"],
            "contact": "doc.sunita@hospital.com",
            "phone": "044-1234004",
            "consultation_fee": "₹400"
        },
        {
            "name": "Dr. Ravi Shankar",
            "specialization": "General Medicine",
            "experience": "15 years",
            "qualification": "MD General Medicine",
            "availability": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
            "contact": "doc.ravi@hospital.com",
            "phone": "044-1234005",
            "consultation_fee": "₹300"
        }
    ],
    "departments": [
        {
            "name": "Cardiology",
            "description": "Heart and cardiovascular care",
            "services": ["Heart Checkup", "ECG", "Echo", "Angioplasty", "Bypass Surgery"],
            "head": "Dr. Raj Kumar",
            "contact": "044-1234001",
            "opd_timing": "9 AM - 1 PM"
        },
        {
            "name": "Neurology", 
            "description": "Brain and nervous system disorders",
            "services": ["Brain MRI", "EEG", "Stroke Treatment", "Epilepsy Care"],
            "head": "Dr. Priya Sharma",
            "contact": "044-1234002",
            "opd_timing": "10 AM - 2 PM"
        },
        {
            "name": "Orthopedics",
            "description": "Bone, joint and muscle care",
            "services": ["Joint Replacement", "Fracture Treatment", "Arthroscopy", "Physiotherapy"],
            "head": "Dr. Amit Patel", 
            "contact": "044-1234003",
            "opd_timing": "9 AM - 1 PM"
        },
        {
            "name": "Pediatrics",
            "description": "Child healthcare and development",
            "services": ["Child Healthcare", "Vaccination", "Growth Monitoring", "Neonatal Care"],
            "head": "Dr. Sunita Reddy",
            "contact": "044-1234004",
            "opd_timing": "10 AM - 2 PM"
        },
        {
            "name": "Emergency",
            "description": "24/7 emergency and trauma care",
            "services": ["Trauma Care", "Accident Treatment", "Critical Care", "Ambulance"],
            "head": "Dr. Emergency Incharge",
            "contact": "108 or 044-1234567",
            "opd_timing": "24/7"
        }
    ],
    "services": {
        "emergency": {
            "description": "24/7 Emergency and Trauma Care",
            "contact": "108 or 044-1234567",
            "features": ["Ambulance Service", "Trauma Center", "ICU", "Quick Response Team"],
            "timings": "24/7"
        },
        "opd": {
            "description": "Outpatient Department Services", 
            "timings": "8:00 AM - 8:00 PM",
            "features": ["Consultation", "Follow-up", "Prescription", "Referral"],
            "contact": "044-1234567"
        },
        "diagnostic": {
            "description": "Advanced Diagnostic Services",
            "timings": "6:00 AM - 10:00 PM", 
            "services": ["MRI", "CT Scan", "X-Ray", "Blood Tests", "Ultrasound", "ECG", "EEG"],
            "contact": "044-1234568"
        },
        "pharmacy": {
            "description": "24/7 Pharmacy Services",
            "timings": "7:00 AM - 11:00 PM",
            "features": ["All Medicines", "Generic Options", "Home Delivery", "Insurance Claim"],
            "contact": "044-1234569"
        },
        "ambulance": {
            "description": "Emergency Ambulance Service",
            "timings": "24/7",
            "features": ["Advanced Life Support", "Oxygen", "Ventilator", "Trained Paramedics"],
            "contact": "108 or 044-1234570"
        }
    },
    "appointment_slots": [
        {"time": "9:00 AM - 9:30 AM", "available": True, "doctor": "General"},
        {"time": "9:30 AM - 10:00 AM", "available": True, "doctor": "General"},
        {"time": "10:00 AM - 10:30 AM", "available": False, "doctor": "General"},
        {"time": "10:30 AM - 11:00 AM", "available": True, "doctor": "Specialist"},
        {"time": "11:00 AM - 11:30 AM", "available": True, "doctor": "Specialist"},
        {"time": "11:30 AM - 12:00 PM", "available": False, "doctor": "Specialist"},
        {"time": "2:00 PM - 2:30 PM", "available": True, "doctor": "General"},
        {"time": "2:30 PM - 3:00 PM", "available": True, "doctor": "General"},
        {"time": "3:00 PM - 3:30 PM", "available": True, "doctor": "Specialist"},
        {"time": "3:30 PM - 4:00 PM", "available": False, "doctor": "Specialist"},
        {"time": "4:00 PM - 4:30 PM", "available": True, "doctor": "General"},
        {"time": "4:30 PM - 5:00 PM", "available": True, "doctor": "General"}
    ],
    "facilities": [
        "300+ Bed Hospital",
        "50+ ICU Beds", 
        "24/7 Emergency",
        "Advanced Operation Theaters",
        "Modern Diagnostic Lab",
        "Pharmacy",
        "Ambulance Service",
        "Cafeteria",
        "Parking Facility",
        "Wi-Fi Connectivity"
    ]
}

# Pydantic models
class LoginRequest(BaseModel):
    user_type: str
    username: str
    password: str

class ChatRequest(BaseModel):
    message: str
    user_id: Optional[str] = None
    user_role: Optional[str] = None

class AppointmentRequest(BaseModel):
    patient_name: str
    doctor_name: str
    preferred_date: str
    preferred_time: str
    department: str

class AddPatientRequest(BaseModel):
    name: str
    age: int
    gender: str
    contact: str
    condition: str

# Routes
@app.get("/")
async def root():
    return {
        "message": "🏥 Hospital Management System API",
        "status": "running", 
        "version": "2.0",
        "frontend_url": "https://arulgnanakumar.github.io/hospital-management-chatbot/",
        "endpoints": {
            "auth": ["POST /login"],
            "chat": ["POST /chat"], 
            "data": ["GET /doctors", "GET /departments", "GET /patients"],
            "appointments": ["GET /appointments/available", "POST /appointments/book"],
            "admin": ["GET /statistics", "POST /patients/add"]
        }
    }

@app.post("/login")
async def login(request: LoginRequest):
    """User login endpoint"""
    user_type = request.user_type.lower()
    username = request.username.lower()
    password_hash = hashlib.sha256(request.password.encode()).hexdigest()
    
    if user_type not in hospital_db["users"]:
        raise HTTPException(status_code=400, detail="Invalid user type")
    
    user = next((u for u in hospital_db["users"][user_type] if u["username"] == username and u["password"] == password_hash), None)
    
    if user:
        # Don't return password in response
        user_response = user.copy()
        user_response.pop("password", None)
        return {
            "success": True, 
            "user": user_response,
            "message": f"Welcome {user_response['name']}!"
        }
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")

@app.post("/chat")
async def chat_handler(request: ChatRequest):
    """Enhanced AI Chatbot endpoint with more intelligence"""
    user_message = request.message.lower()
    user_role = request.user_role
    
    # Enhanced response patterns with more data
    if any(word in user_message for word in ["hello", "hi", "hey", "good morning", "good afternoon"]):
        return {"response": "👋 Hello! I'm MediBot, your intelligent healthcare assistant. I can help with appointments, doctors, emergencies, medical information, and hospital services. How can I assist you today?"}
    
    elif any(word in user_message for word in ["appointment", "book", "schedule", "meet doctor"]):
        available_slots = [slot for slot in hospital_data["appointment_slots"] if slot["available"]]
        slots_text = "\n".join([f"• {slot['time']} ({slot['doctor']})" for slot in available_slots[:4]])
        
        response = f"""📅 **Appointment Booking**

Available slots for today:
{slots_text}

**Booking Methods:**
• 📞 Call: 044-1234567
• 🌐 Online: www.cityhospital.com/book  
• 📱 Mobile App: City Hospital App
• 🏥 Direct Walk-in

**Departments Available:**
• Cardiology - Dr. Raj Kumar
• Neurology - Dr. Priya Sharma  
• Orthopedics - Dr. Amit Patel
• Pediatrics - Dr. Sunita Reddy
• General Medicine - Dr. Ravi Shankar

Which department would you like to book?"""
        return {"response": response}
    
    elif any(word in user_message for word in ["doctor", "specialist", "cardiologist", "neurologist"]):
        doctors_text = "\n".join([
            f"• **{doc['name']}** - {doc['specialization']} ({doc['experience']}) - Available: {', '.join(doc['availability'])} - Fee: {doc['consultation_fee']}"
            for doc in hospital_data["doctors"]
        ])
        
        response = f"""👨‍⚕️ **Our Medical Experts**

{doctors_text}

**Contact for Appointments:**
📞 044-1234567
📧 appointments@hospital.com

Which specialist would you like to consult?"""
        return {"response": response}
    
    elif any(word in user_message for word in ["emergency", "urgent", "accident", "heart attack", "stroke"]):
        response = """🚨 **EMERGENCY SERVICES - 24/7**

**IMMEDIATE ACTION REQUIRED!**

**Emergency Contacts:**
• 🚑 Ambulance: 108 or 044-1234570
• 🏥 Emergency Ward: 044-1234567
• 💓 Cardiac Emergency: 044-1234569
• 🧠 Neuro Emergency: 044-1234571

**Emergency Services:**
• Trauma Care Center
• Cardiac Emergency Unit  
• Stroke Unit
• ICU & Critical Care
• Emergency Surgery
• Ambulance with ALS

**⚠️ If this is a life-threatening emergency, please proceed directly to the emergency ward or call ambulance immediately!**"""
        return {"response": response}
    
    elif any(word in user_message for word in ["department", "specialty"]):
        depts_text = "\n".join([
            f"• **{dept['name']}** - {dept['description']} (OPD: {dept['opd_timing']}) - Contact: {dept['contact']}"
            for dept in hospital_data["departments"]
        ])
        
        return {"response": f"🏥 **Hospital Departments**\n\n{depts_text}"}
    
    elif any(word in user_message for word in ["service", "facility", "treatment"]):
        facilities_text = "\n".join([f"• {facility}" for facility in hospital_data["facilities"]])
        services_text = "\n".join([f"• **{key.title()}**: {value['description']} (Contact: {value['contact']})" for key, value in hospital_data["services"].items()])
        
        response = f"""🏥 **Hospital Services & Facilities**

**Medical Services:**
{services_text}

**Hospital Facilities:**
{facilities_text}

Which service are you interested in?"""
        return {"response": response}
    
    elif any(word in user_message for word in ["time", "timing", "open", "close"]):
        response = """⏰ **Hospital Timings**

**Emergency Services:** 24/7
**OPD Consultation:** 8:00 AM - 8:00 PM
**Specialist Consultation:** 9:00 AM - 5:00 PM
**Pharmacy:** 7:00 AM - 11:00 PM  
**Diagnostic Services:** 6:00 AM - 10:00 PM
**Visiting Hours:** 4:00 PM - 7:00 PM
**Ambulance:** 24/7

**We're always here for emergencies!**"""
        return {"response": response}
    
    elif any(word in user_message for word in ["location", "address", "where"]):
        response = """📍 **Hospital Location**

**City Multi-Speciality Hospital**
No. 123, Medical College Road
Anna Nagar, Chennai - 600040
Tamil Nadu, India

**Landmarks:**
• 🚇 Near Central Metro Station (5 mins walk)
• 🛍️ Opposite City Mall
• 🚓 Next to Police Station

**Transport:**
• Metro: Central Station (Exit 3)
• Bus: Routes 23C, 45D, 78A
• Parking: Available for 200+ vehicles

**Google Maps:** https://maps.app.goo.gl/hospitalchennai"""
        return {"response": response}
    
    elif any(word in user_message for word in ["contact", "phone", "number", "email"]):
        response = """📞 **Contact Information**

**General Enquiries:**
• 📞 Main Line: 044-1234567
• 📠 Fax: 044-1234560
• 📧 Email: info@cityhospital.com
• 🌐 Website: www.cityhospital.com

**Emergency & Special Services:**
• 🚑 Ambulance: 108 or 044-1234570
• 🏥 Emergency: 044-1234567
• 💓 Cardiac: 044-1234569
• 🧠 Neurology: 044-1234571
• 🦴 Ortho: 044-1234572
• 👶 Pediatrics: 044-1234573

**We're available 24/7 for emergencies!**"""
        return {"response": response}
    
    elif any(word in user_message for word in ["medicine", "pharmacy", "drug"]):
        response = """💊 **Pharmacy Services**

**Main Pharmacy:**
• Timings: 7:00 AM - 11:00 PM
• Contact: 044-1234569
• Location: Ground Floor, Main Building

**Services:**
• All medicines available
• Generic medicine options
• Prescription drugs
• Medical equipment
• Home delivery
• Insurance claims processing

**Emergency Pharmacy:** 24/7 (Near Emergency Ward)"""
        return {"response": response}

    elif any(word in user_message for word in ["covid", "corona", "vaccine"]):
        response = """🦠 **COVID-19 Services**

**Testing & Vaccination:**
• COVID Testing: 24/7
• RT-PCR Results: 6-8 hours
• Rapid Antigen: 30 minutes
• Vaccination Center: 9 AM - 5 PM

**COVID Care:**
• Isolation Wards
• ICU Beds with Ventilators
• Oxygen Support
• Teleconsultation
• Home Care Services

**Stay Safe! Get Vaccinated! 💉**"""
        return {"response": response}

    # Role-specific intelligent responses
    if user_role == "admin":
        if any(word in user_message for word in ["add", "create", "new", "register"]):
            return {"response": "⚙️ **Admin Panel Features**\n\nAs Administrator, you can:\n• Add new staff members\n• Manage patient records\n• Generate reports\n• View hospital statistics\n• Manage appointments\n• System configuration\n\nUse the admin dashboard for complete hospital management."}
    
    elif user_role == "doctor":
        if any(word in user_message for word in ["patient", "case", "treatment", "prescription"]):
            return {"response": f"👨‍⚕️ **Doctor Dashboard**\n\nAs {request.user_id}, you can:\n• View patient medical records\n• Write digital prescriptions\n• Schedule surgeries and procedures\n• Check lab test results\n• Consult with other specialists\n• Update treatment plans\n\nAccess your doctor portal for comprehensive patient management."}
    
    elif user_role == "nurse":
        if any(word in user_message for word in ["patient", "care", "medication", "vital"]):
            return {"response": f"👩‍⚕️ **Nursing Services**\n\nAs {request.user_id}, your responsibilities:\n• Monitor patient vital signs\n• Administer medications\n• Assist in medical procedures\n• Patient care coordination\n• Emergency response\n• Health education\n• Maintain patient charts\n\nCheck the nursing station for current patient assignments."}
    
    elif user_role == "patient":
        if any(word in user_message for word in ["my", "report", "test", "prescription", "bill"]):
            return {"response": f"👤 **Patient Services**\n\nDear {request.user_id}, you can access:\n• Your medical reports and history\n• Prescription details\n• Appointment history\n• Lab test results\n• Discharge summaries\n• Bill payments\n• Health records download\n\nVisit patient portal or contact helpdesk for assistance."}

    # Default intelligent responses
    default_responses = [
        "I'm here to assist with all hospital services including appointments, doctor information, emergency care, medical queries, and healthcare guidance. What specific information do you need?",
        "I can help you with appointment scheduling, specialist doctor details, emergency services, hospital facilities, medical information, and patient care. How can I assist you today?",
        "As your healthcare assistant, I provide comprehensive information about medical services, doctor consultations, appointment booking, emergency care, hospital facilities, and health guidance. What would you like to know?",
        "I specialize in hospital information, medical services, doctor appointments, emergency guidance, patient support, and healthcare facilities. What do you need assistance with?",
        "Welcome to our advanced healthcare system! I can help with medical appointments, specialist doctors, emergency services, hospital information, and healthcare support. How may I assist you?"
    ]
    
    return {"response": random.choice(default_responses)}

@app.get("/doctors")
async def get_doctors():
    """Get all doctors information"""
    return {"doctors": hospital_data["doctors"]}

@app.get("/departments")
async def get_departments():
    """Get all departments"""
    return {"departments": hospital_data["departments"]}

@app.get("/services")
async def get_services():
    """Get all services"""
    return {"services": hospital_data["services"]}

@app.get("/appointments/available")
async def get_available_appointments():
    """Get available appointment slots"""
    available = [slot for slot in hospital_data["appointment_slots"] if slot["available"]]
    return {"available_slots": available, "total_slots": len(available)}

@app.get("/patients")
async def get_patients():
    """Get all patients"""
    return {
        "patients": hospital_db["patients"],
        "total_patients": len(hospital_db["patients"]),
        "admitted_patients": len([p for p in hospital_db["patients"] if p["status"] == "Admitted"])
    }

@app.get("/prescriptions")
async def get_prescriptions():
    """Get all prescriptions"""
    return {"prescriptions": hospital_db["prescriptions"]}

@app.post("/appointments/book")
async def book_appointment(request: AppointmentRequest):
    """Book a new appointment"""
    appointment_id = f"APT_{len(hospital_db['appointments']) + 1:03d}"
    
    new_appointment = {
        "appointment_id": appointment_id,
        "patient_name": request.patient_name,
        "doctor_name": request.doctor_name,
        "department": request.department,
        "date": request.preferred_date,
        "time": request.preferred_time,
        "status": "Confirmed",
        "booked_at": datetime.now().isoformat()
    }
    
    hospital_db["appointments"].append(new_appointment)
    
    return {
        "success": True,
        "appointment_id": appointment_id,
        "message": "Appointment booked successfully!",
        "details": new_appointment
    }

@app.post("/patients/add")
async def add_patient(request: AddPatientRequest):
    """Add new patient (Admin function)"""
    patient_id = f"PAT_{len(hospital_db['patients']) + 1:03d}"
    
    new_patient = {
        "patient_id": patient_id,
        "name": request.name,
        "age": request.age,
        "gender": request.gender,
        "contact": request.contact,
        "condition": request.condition,
        "admission_date": datetime.now().strftime("%Y-%m-%d"),
        "status": "Admitted",
        "room": "To be assigned"
    }
    
    hospital_db["patients"].append(new_patient)
    
    return {
        "success": True,
        "patient_id": patient_id,
        "message": "Patient added successfully!",
        "patient": new_patient
    }

@app.get("/statistics")
async def get_statistics():
    """Get comprehensive hospital statistics"""
    stats = {
        "total_patients": len(hospital_db["patients"]),
        "total_doctors": len(hospital_db["users"]["doctor"]),
        "total_nurses": len(hospital_db["users"]["nurse"]),
        "total_appointments": len(hospital_db["appointments"]),
        "admitted_patients": len([p for p in hospital_db["patients"] if p["status"] == "Admitted"]),
        "discharged_patients": len([p for p in hospital_db["patients"] if p["status"] == "Discharged"]),
        "today_appointments": len([a for a in hospital_db["appointments"] if a.get("date") == datetime.now().strftime("%Y-%m-%d")]),
        "total_prescriptions": len(hospital_db["prescriptions"]),
        "hospital_capacity": {
            "total_beds": 300,
            "occupied_beds": len([p for p in hospital_db["patients"] if p["status"] == "Admitted"]),
            "available_beds": 300 - len([p for p in hospital_db["patients"] if p["status"] == "Admitted"])
        }
    }
    return {"statistics": stats}

@app.get("/facilities")
async def get_facilities():
    """Get hospital facilities"""
    return {"facilities": hospital_data["facilities"]}

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting Hospital Management System API...")
    print("📍 Frontend URL: https://arulgnanakumar.github.io/hospital-management-chatbot/")
    print("📝 Available endpoints:")
    print("   • GET  / - API information")
    print("   • POST /login - User login") 
    print("   • POST /chat - AI Chatbot")
    print("   • GET  /doctors - Doctors list")
    print("   • GET  /departments - Departments list")
    print("   • GET  /patients - Patients list")
    print("   • POST /appointments/book - Book appointment")
    print("   • GET  /statistics - Hospital stats")
    print("\n🔑 Demo Logins:")
    print("   • Admin: arul / arul")
    print("   • Doctor: doc_raj / doctor123")
    print("   • Nurse: nurse_priya / nurse123") 
    print("   • Patient: patient_ram / patient123")
    print("\n🔥 Server running on: http://localhost:8000")
    
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)