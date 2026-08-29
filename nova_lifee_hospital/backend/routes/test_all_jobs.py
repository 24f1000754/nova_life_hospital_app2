

import os
import sys
from datetime import date, datetime, timedelta


from backend.app import create_app
app = create_app()

with app.app_context():
    from backend.models.models import db, User, Patient, Doctor, Appointment
    from backend.routes.tasks import export_patient_report, daily_appointment_reminder, monthly_doctor_report
    
    print("\n" + "="*60)
    print(" TESTING HMS BACKEND JOBS")
    print("="*60 + "\n")
    
    
    print(" TEST 1: Database Check")
    print("-" * 60)
    
    users_count = User.query.count()
    patients_count = Patient.query.count()
    doctors_count = Doctor.query.count()
    appointments_count = Appointment.query.count()
    
    print(f" Users: {users_count}")
    print(f" Patients: {patients_count}")
    print(f"Doctors: {doctors_count}")
    print(f" Appointments: {appointments_count}")
    
    if appointments_count == 0:
        print("\n WARNING: No appointments found!")
        print("Please create test data first:")
        print("1. Register a patient")
        print("2. Create a doctor (admin panel)")
        print("3. Book an appointment")
        print("4. Mark appointment as 'Completed'\n")
    
   
    print("\n📊 TEST 2: CSV Export (User-Triggered Job)")
    print("-" * 60)
    
    first_patient = Patient.query.first()
    
    if first_patient:
        print(f"Testing export for Patient ID: {first_patient.id}")
        print(f"Patient Name: {first_patient.user.name}")
        
        
        result = export_patient_report(first_patient.id)
        
        if result.get("status") == "success":
            print(f" CSV Export: SUCCESS")
            print(f"   Filename: {result['filename']}")
            print(f"   Appointments: {result['total_appointments']}")
            
           
            if os.path.exists(result['filename']):
                print(f"   File exists: YES ")
            else:
                print(f"   File exists: NO ")
        else:
            print(f" CSV Export: FAILED")
            print(f"   Message: {result.get('message')}")
    else:
        print(" No patients found in database")
    
    
    print("\n📊 TEST 3: Daily Reminder (Scheduled Job)")
    print("-" * 60)
    
    today_str = str(date.today())
    today_appointments = Appointment.query.filter_by(
        date=today_str,
        status="Booked"
    ).all()
    
    print(f"Today's date: {today_str}")
    print(f"Today's booked appointments: {len(today_appointments)}")
    
    if len(today_appointments) == 0:
        print("\n No appointments for today - creating test appointment...")
        
       
        if first_patient and Doctor.query.first():
            test_appt = Appointment(
                doctor_id=Doctor.query.first().id,
                patient_id=first_patient.id,
                date=today_str,
                time="10:00",
                status="Booked"
            )
            db.session.add(test_appt)
            db.session.commit()
            print(" Test appointment created for today")
            
            
            print("\n🔄 Running daily reminder task...")
            result = daily_appointment_reminder()
            
            if result.get("status") == "success":
                print(f" Daily Reminder: SUCCESS")
                print(f"   Emails sent: {result['sent']}")
                print(f"   Failed: {result['failed']}")
            else:
                print(f"❌ Daily Reminder: FAILED")
                print(f"   Message: {result.get('message')}")
        else:
            print("❌ Cannot create test appointment - missing doctor or patient")
    else:
        print(f"\n {len(today_appointments)} appointments scheduled for today")
        print("   Run: daily_appointment_reminder.delay() to send emails")
    
   
    print("\nTEST 4: Monthly Report (Scheduled Job)")
    print("-" * 60)
    
    current_month = date.today().month
    all_doctors = Doctor.query.all()
    
    print(f"Current month: {current_month}")
    print(f"Total doctors: {len(all_doctors)}")
    
    if len(all_doctors) > 0:
        doctor_with_appointments = 0
        
        for d in all_doctors:
            apps = Appointment.query.filter_by(doctor_id=d.id).count()
            if apps > 0:
                doctor_with_appointments += 1
        
        print(f"Doctors with appointments: {doctor_with_appointments}")
        
        if doctor_with_appointments > 0:
            print("\n🔄 Running monthly report task...")
            result = monthly_doctor_report()
            
            if result.get("status") == "success":
                print(f" Monthly Report: SUCCESS")
                print(f"   Reports sent: {result['sent']}")
                print(f"   Skipped: {result['skipped']}")
            else:
                print(f"❌ Monthly Report: FAILED")
                print(f"   Message: {result.get('message')}")
        else:
            print("\n No doctors have appointments - skipping report test")
    else:
        print("❌ No doctors found in database")
    
    
    print("\n TEST 5: Celery & Redis Connection")
    print("-" * 60)
    
    try:
        from backend.routes.celery_app import celery
        
        
        inspect = celery.control.inspect()
        active = inspect.active()
        
        if active:
            print(" Celery Worker: RUNNING")
            print(f"   Workers: {list(active.keys())}")
        else:
            print("Celery Worker: NOT RUNNING")
            print("   Start with: celery -A celery_app.celery worker --loglevel=info --pool=solo")
        
        
        from backend.routes.cache import r
        r.ping()
        print(" Redis: CONNECTED")
        
    except Exception as e:
        print(f" Connection Error: {str(e)}")
    
    
    print("\n" + "="*60)
    print("📋 TEST SUMMARY")
    print("="*60)
    
    print("\n TO RUN TASKS MANUALLY:")
    print("   from tasks import export_patient_report")
    print("   export_patient_report.delay(1)")
    print()
    print("   from tasks import daily_appointment_reminder")
    print("   daily_appointment_reminder.delay()")
    print()
    print("   from tasks import monthly_doctor_report")
    print("   monthly_doctor_report.delay()")
    
    print("\n TO RUN SCHEDULED TASKS:")
    print("   Terminal 1: python app.py")
    print("   Terminal 2: celery -A celery_app.celery worker --loglevel=info --pool=solo")
    print("   Terminal 3: celery -A celery_app.celery beat --loglevel=info")
    
    print("\nTO DOWNLOAD CSV:")
    print("   API: GET http://127.0.0.1:5000/api/patient/download-report/1")
    print("   Or use Patient Dashboard export button")
    
    print("\n" + "="*60)
    print(" TESTING COMPLETE")
    print("="*60 + "\n")