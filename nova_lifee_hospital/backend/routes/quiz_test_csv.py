

from backend.app import create_app
import os

app = create_app()

with app.app_context():
    from backend.models.models import db, Patient, User, Appointment
    from backend.routes.tasks import export_patient_report
    
    print("\n" + "="*60)
    print(" QUICK CSV EXPORT TEST")
    print("="*60 + "\n")
    
    
    patient = Patient.query.first()
    
    if not patient:
        print(" No patients found in database")
        print("Please register a patient first via frontend")
        exit()
    
    user = User.query.get(patient.user_id)
    
    print(f" Testing for:")
    print(f"   Patient ID: {patient.id}")
    print(f"   User ID: {user.id}")
    print(f"   Name: {user.name}")
    print(f"   Email: {user.email}")
    
    
    completed = Appointment.query.filter_by(
        patient_id=patient.id,
        status="Completed"
    ).count()
    
    print(f"\n📊 Completed Appointments: {completed}")
    
    if completed == 0:
        print("\n WARNING: No completed appointments!")
        print("Mark at least one appointment as 'Completed' first")
        print("\nSQL Command to fix:")
        print(f"UPDATE appointments SET status='Completed' WHERE patient_id={patient.id} LIMIT 1;")
    
    
    print(f"\n🔄 Generating CSV for Patient ID: {patient.id}...")
    
    result = export_patient_report(patient.id)
    
    if result.get("status") == "success":
        print(f"\n SUCCESS!")
        print(f"   Filename: {result['filename']}")
        print(f"   Appointments: {result['total_appointments']}")
        
        
        if os.path.exists(result['filename']):
            print(f"   File Size: {os.path.getsize(result['filename'])} bytes")
            print(f"   Location: {os.path.abspath(result['filename'])}")
            
            
            print("\n File Preview:")
            with open(result['filename'], 'r', encoding='utf-8') as f:
                for i, line in enumerate(f):
                    if i < 3:  # First 3 lines
                        print(f"   {line.strip()}")
            
            print(f"\nCSV FILE READY FOR DOWNLOAD!")
            print(f"\n🌐 Download URL:")
            print(f"   http://127.0.0.1:5000/api/patient/download-report/{user.id}")
            
        else:
            print(f"\n File not created!")
    else:
        print(f"\nFAILED!")
        print(f"   Message: {result.get('message')}")
    
    print("\n" + "="*60)
    print(" TEST COMPLETE")
    print("="*60 + "\n")