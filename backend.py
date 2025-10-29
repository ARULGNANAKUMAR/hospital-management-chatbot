#!/usr/bin/env python3
"""
🏥 Pure Python Hospital Management Backend
No external libraries needed - Built with Python Standard Library only
"""

import http.server
import socketserver
import json
import hashlib
import random
from datetime import datetime
from urllib.parse import urlparse, parse_qs
import threading

# Configuration
HOST = "0.0.0.0"
PORT = 8000

# In-memory database
hospital_db = {
    "users": {
        "admin": [
            {"username": "arul", "password": hashlib.sha256("arul".encode()).hexdigest(), "name": "Arul Gnanakumar", "role": "admin", "email": "arul@hospital.com"}
        ],
        "doctor": [
            {"username": "doc_raj", "password": hashlib.sha256("doctor123".encode()).hexdigest(), "name": "Dr. Raj Kumar", "role": "doctor", "specialization": "Cardiology", "experience": "10 years"},
            {"username": "doc_priya", "password": hashlib.sha256("doctor123".encode()).hexdigest(), "name": "Dr. Priya Sharma", "role": "doctor", "specialization": "Neurology", "experience": "8 years"}
        ],
        "nurse": [
            {"username": "nurse_priya", "password": hashlib.sha256("nurse123".encode()).hexdigest(), "name": "Nurse Priya", "role": "nurse", "department": "General Ward", "shift": "Morning"},
            {"username": "nurse_anita", "password": hashlib.sha256("nurse123".encode()).hexdigest(), "name": "Nurse Anita", "role": "nurse", "department": "ICU", "shift": "Night"}
        ],
        "patient": [
            {"username": "patient_ram", "password": hashlib.sha256("patient123".encode()).hexdigest(), "name": "Ramesh Kumar", "role": "patient", "condition": "Hypertension", "age": 45},
            {"username": "patient_sita", "password": hashlib.sha256("patient123".encode()).hexdigest(), "name": "Sita Raman", "role": "patient", "condition": "Migraine", "age": 32}
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
        }
    ]
}

# Hospital data for AI responses
hospital_data = {
    "doctors": [
        {
            "name": "Dr. Raj Kumar",
            "specialization": "Cardiology", 
            "experience": "10 years",
            "availability": ["Monday", "Wednesday", "Friday"],
            "contact": "044-1234001"
        },
        {
            "name": "Dr. Priya Sharma",
            "specialization": "Neurology",
            "experience": "8 years", 
            "availability": ["Tuesday", "Thursday", "Saturday"],
            "contact": "044-1234002"
        }
    ],
    "services": [
        "Emergency Care - 24/7",
        "OPD Consultation - 8AM-8PM", 
        "Pharmacy - 7AM-11PM",
        "Diagnostic Services",
        "Ambulance Service"
    ]
}

class HospitalAPIHandler(http.server.BaseHTTPRequestHandler):
    
    def do_OPTIONS(self):
        """Handle CORS preflight requests"""
        self.send_response(200)
        self.send_cors_headers()
        self.end_headers()
    
    def send_cors_headers(self):
        """Add CORS headers to response"""
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.send_header('Content-Type', 'application/json')
    
    def do_GET(self):
        """Handle GET requests"""
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        
        if path == '/':
            response = self.handle_root()
        elif path == '/doctors':
            response = self.handle_get_doctors()
        elif path == '/services':
            response = self.handle_get_services()
        elif path == '/patients':
            response = self.handle_get_patients()
        elif path == '/health':
            response = self.handle_health_check()
        else:
            response = self.error_response("Endpoint not found", 404)
        
        self.send_json_response(response)
    
    def do_POST(self):
        """Handle POST requests"""
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        
        # Get request body
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length).decode('utf-8')
        
        try:
            data = json.loads(post_data) if post_data else {}
        except:
            data = {}
        
        if path == '/login':
            response = self.handle_login(data)
        elif path == '/chat':
            response = self.handle_chat(data)
        elif path == '/appointments/book':
            response = self.handle_book_appointment(data)
        else:
            response = self.error_response("Endpoint not found", 404)
        
        self.send_json_response(response)
    
    def send_json_response(self, response):
        """Send JSON response with CORS headers"""
        status_code = response.get('status_code', 200)
        self.send_response(status_code)
        self.send_cors_headers()
        self.end_headers()
        
        response_data = {k: v for k, v in response.items() if k != 'status_code'}
        self.wfile.write(json.dumps(response_data).encode('utf-8'))
    
    def handle_root(self):
        """Root endpoint - API information"""
        return {
            "message": "🏥 Hospital Management System API",
            "status": "running",
            "version": "1.0",
            "technology": "Pure Python (No External Libraries)",
            "endpoints": {
                "GET": ["/", "/doctors", "/services", "/patients", "/health"],
                "POST": ["/login", "/chat", "/appointments/book"]
            }
        }
    
    def handle_health_check(self):
        """Health check endpoint"""
        return {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "server": "Pure Python HTTP Server"
        }
    
    def handle_get_doctors(self):
        """Get all doctors"""
        return {
            "doctors": hospital_data["doctors"],
            "count": len(hospital_data["doctors"])
        }
    
    def handle_get_services(self):
        """Get all services"""
        return {
            "services": hospital_data["services"],
            "emergency_contact": "108 or 044-1234567"
        }
    
    def handle_get_patients(self):
        """Get all patients"""
        return {
            "patients": hospital_db["patients"],
            "total_patients": len(hospital_db["patients"]),
            "admitted_patients": len([p for p in hospital_db["patients"] if p["status"] == "Admitted"])
        }
    
    def handle_login(self, data):
        """Handle user login"""
        user_type = data.get('user_type', '').lower()
        username = data.get('username', '').lower()
        password = data.get('password', '')
        
        if not user_type or not username or not password:
            return self.error_response("Missing required fields", 400)
        
        if user_type not in hospital_db["users"]:
            return self.error_response("Invalid user type", 400)
        
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        user = next((u for u in hospital_db["users"][user_type] 
                    if u["username"] == username and u["password"] == password_hash), None)
        
        if user:
            # Remove password from response
            user_response = user.copy()
            user_response.pop("password")
            return {
                "success": True,
                "user": user_response,
                "message": f"Welcome {user_response['name']}!"
            }
        else:
            return self.error_response("Invalid credentials", 401)
    
    def handle_chat(self, data):
        """AI Chatbot endpoint"""
        message = data.get('message', '').lower()
        user_role = data.get('user_role')
        
        # Enhanced AI responses
        if not message:
            return self.error_response("Message is required", 400)
        
        response = self.generate_ai_response(message, user_role)
        return {"response": response}
    
    def generate_ai_response(self, message, user_role):
        """Generate intelligent AI responses"""
        # Greetings
        if any(word in message for word in ["hello", "hi", "hey"]):
            return "👋 Hello! I'm MediBot, your healthcare assistant. How can I help you today?"
        
        # Appointments
        elif any(word in message for word in ["appointment", "book", "schedule"]):
            return """📅 **Appointment Booking**

Available today:
• 9:00 AM - 9:30 AM
• 10:30 AM - 11:00 AM  
• 2:00 PM - 2:30 PM

Call: 044-1234567
Online: www.hospital.com

Which department do you need?"""
        
        # Doctors
        elif any(word in message for word in ["doctor", "specialist"]):
            doctors_text = "\n".join([
                f"• {doc['name']} - {doc['specialization']} (Available: {', '.join(doc['availability'])})"
                for doc in hospital_data["doctors"]
            ])
            return f"""👨‍⚕️ **Our Medical Team**

{doctors_text}

Contact: 044-1234567"""
        
        # Emergency
        elif any(word in message for word in ["emergency", "urgent", "accident"]):
            return """🚨 **EMERGENCY SERVICES**

Emergency Hotline: 108 or 044-1234567
Ambulance: 24/7 available
Emergency Ward: Always open

⚠️ For immediate care, proceed to emergency ward!"""
        
        # Location
        elif any(word in message for word in ["location", "address", "where"]):
            return """📍 **Hospital Location**

City Multi-Speciality Hospital
No. 123, Medical College Road
Chennai - 600040

Near Central Metro Station"""
        
        # Timings
        elif any(word in message for word in ["time", "timing", "open"]):
            return """⏰ **Hospital Timings**

Emergency: 24/7
OPD: 8:00 AM - 8:00 PM  
Pharmacy: 7:00 AM - 11:00 PM
Visiting: 4:00 PM - 7:00 PM"""
        
        # Role-specific responses
        if user_role == "admin":
            return "⚙️ **Admin Panel** - You can manage staff, patients, and view statistics."
        elif user_role == "doctor":
            return "👨‍⚕️ **Doctor Dashboard** - Access patient records and medical data."
        elif user_role == "nurse":
            return "👩‍⚕️ **Nursing Station** - Monitor patients and provide care."
        elif user_role == "patient":
            return "👤 **Patient Services** - View your medical information and appointments."
        
        # Default response
        return "I can help with appointments, doctors, emergencies, hospital services, and medical information. What do you need assistance with?"
    
    def handle_book_appointment(self, data):
        """Book new appointment"""
        required_fields = ['patient_name', 'doctor_name', 'preferred_date', 'preferred_time']
        if not all(field in data for field in required_fields):
            return self.error_response("Missing required fields", 400)
        
        appointment_id = f"APT_{len(hospital_db['appointments']) + 1:03d}"
        new_appointment = {
            "appointment_id": appointment_id,
            "patient_name": data['patient_name'],
            "doctor_name": data['doctor_name'],
            "date": data['preferred_date'],
            "time": data['preferred_time'],
            "status": "Confirmed",
            "booked_at": datetime.now().isoformat()
        }
        
        hospital_db["appointments"].append(new_appointment)
        
        return {
            "success": True,
            "appointment_id": appointment_id,
            "message": "Appointment booked successfully!",
            "appointment": new_appointment
        }
    
    def error_response(self, message, status_code=400):
        """Generate error response"""
        return {
            "success": False,
            "error": message,
            "status_code": status_code
        }
    
    def log_message(self, format, *args):
        """Custom log message format"""
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {format % args}")

def start_server():
    """Start the HTTP server"""
    with socketserver.TCPServer((HOST, PORT), HospitalAPIHandler) as httpd:
        print("🚀 Pure Python Hospital Server Started!")
        print(f"📍 Server running on http://{HOST}:{PORT}")
        print(f"🌐 Frontend: https://arulgnanakumar.github.io/hospital-management-chatbot/")
        print("\n🔑 Demo Logins:")
        print("   • Admin: arul / arul")
        print("   • Doctor: doc_raj / doctor123") 
        print("   • Nurse: nurse_priya / nurse123")
        print("   • Patient: patient_ram / patient123")
        print("\n📡 Ready to accept requests...")
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n🛑 Server stopped!")

if __name__ == "__main__":
    start_server()
