#tasks.py

from datetime import datetime, date
from backend.models.models import db, Appointment, Patient, Doctor, User
import csv
import os
from backend.routes.celery_app import celery
from flask_mail import Message
from flask import current_app



@celery.task(bind=True)
def export_patient_report(self, patient_id):
    
    try:
        patient = Patient.query.get(patient_id)

        if not patient:
            print(f" EXPORT ERROR → Patient not found: {patient_id}")
            return {"status": "error", "message": "Patient not found"}

        user = User.query.get(patient.user_id)

        appointments = Appointment.query.filter_by(
            patient_id=patient.id,
            status="Completed"
        ).all()

        if not appointments:
            return {"status": "warning", "message": "No completed appointments found"}

        if not os.path.exists("reports"):
            os.makedirs("reports")

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"reports/patient_{patient.id}_report_{timestamp}.csv"

        with open(filename, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow([
                "Patient ID", "Patient Name", "Doctor Name",
                "Doctor Specialization", "Appointment Date",
                "Appointment Time", "Diagnosis", "Prescription"
            ])

            for a in appointments:
                doctor = Doctor.query.get(a.doctor_id)
                doctor_user = User.query.get(doctor.user_id) if doctor else None

                writer.writerow([
                    patient.user_id,
                    user.name,
                    doctor_user.name if doctor_user else "N/A",
                    doctor.specialization if doctor else "N/A",
                    a.date,
                    a.time,
                    a.diagnosis or "N/A",
                    a.prescription or "N/A"
                ])

        print(f"✅ CSV EXPORT COMPLETED → {filename}")

        
        try:
            msg = Message(
                subject="📊 Your Treatment Report is Ready - Nova Life Hospital",
                recipients=[user.email]
            )

            msg.body = f"""
Hello {user.name},

Great news! Your treatment report has been generated successfully.

Report Details:
📋 Total Appointments: {len(appointments)}
📅 Generated On: {datetime.now().strftime("%B %d, %Y at %I:%M %p")}

You can download your report from your dashboard!

This report includes:
✅ All your completed appointments
✅ Doctor details and specializations
✅ Diagnosis and prescriptions
✅ Treatment history

Thank you for choosing Nova Life Hospital!

Best regards,
Nova Life Hospital Team

---
This is automated reminder.Please do not reply to this mail.
            """

            current_app.extensions['mail'].send(msg)
            print(f"✅ Report notification email sent to {user.email}")

        except Exception as email_error:
            print(f"⚠️ Email notification failed: {str(email_error)}")
            
        
        return {
            "status": "success",
            "filename": filename,
            "total_appointments": len(appointments)
        }

    except Exception as e:
        print(f"❌ EXPORT ERROR: {str(e)}")
        return {"status": "error", "message": str(e)}





@celery.task(bind=True)
def daily_appointment_reminder(self):
    try:
        today = str(date.today())

        appointments = Appointment.query.filter_by(
            date=today,
            status="Booked"
        ).all()

        if not appointments:
            print("No appointments today")
            return {"status": "info", "message": "No appointments today"}

        sent = 0

        for a in appointments:
            patient = Patient.query.get(a.patient_id)
            if not patient:
                continue

            user = User.query.get(patient.user_id)
            if not user or not user.email:
                continue

            doctor = Doctor.query.get(a.doctor_id)
            doctor_user = User.query.get(doctor.user_id) if doctor else None

            msg = Message(
                subject=" Appointment Reminder - Nova Life Hospital",
                recipients=[user.email]
            )

            msg.body = f"""
Hello {user.name},

This is a reminder for your appointment today.

Date: {a.date}
Time: {a.time}
Doctor: {doctor_user.name if doctor_user else 'N/A'}

Important: Please arrive 15 minutes early to complete any necessary paperwork.

- Nova Life Hospital
"""

            current_app.extensions['mail'].send(msg)
            sent += 1
            print(f"✅ Reminder sent to {user.email}")

        return {"status": "success", "sent": sent}

    except Exception as e:
        print(f" DAILY REMINDER ERROR: {str(e)}")
        return {"status": "error", "message": str(e)}




from flask import render_template

@celery.task(bind=True)
def monthly_doctor_report(self):
    """
    Monthly activity report for doctors with HTML email
    """
    try:
        today = date.today()
        month = 1
        year = 2026
        
        
        month_names = ["January", "February", "March", "April", "May", "June",
                      "July", "August", "September", "October", "November", "December"]
        month_name = month_names[month - 1]

        doctors = Doctor.query.all()
        sent = 0

        for doctor in doctors:
            # Get all appointments for this doctor
            apps = Appointment.query.filter_by(
                doctor_id=doctor.id,
                status="Completed"
            ).all()
            
            # Filter for last month
            monthly_apps = []
            for a in apps:
                try:
                    d = datetime.strptime(a.date, "%Y-%m-%d")
                    if d.month == month and d.year == year:
                        monthly_apps.append(a)
                except:
                    continue

            if not monthly_apps:
                print(f"⚠️ No appointments for Dr. {doctor.user.name} in {month_name}")
                continue

            # Prepare appointment data with patient names
            appointment_data = []
            unique_patients = set()
            diagnoses_count = 0
            prescriptions_count = 0
            
            for apt in monthly_apps:
                patient = Patient.query.get(apt.patient_id)
                patient_user = User.query.get(patient.user_id) if patient else None
                
                if patient_user:
                    unique_patients.add(patient_user.name)
                
                if apt.diagnosis:
                    diagnoses_count += 1
                if apt.prescription:
                    prescriptions_count += 1
                
                appointment_data.append({
                    'date': apt.date,
                    'time': apt.time,
                    'patient_name': patient_user.name if patient_user else 'Unknown',
                    'status': apt.status,
                    'diagnosis': apt.diagnosis or 'Not recorded',
                    'prescription': apt.prescription or 'Not recorded'
                })

            user = User.query.get(doctor.user_id)
            if not user or not user.email:
                continue

            
            html_body = render_template(
                'monthly_doctor_report.html',
                doctor_name=user.name,
                month_name=month_name,
                year=year,
                total_appointments=len(monthly_apps),
                unique_patients=len(unique_patients),
                total_diagnoses=diagnoses_count,
                total_prescriptions=prescriptions_count,
                appointments=appointment_data
            )

            
            msg = Message(
                subject=f"📊 Monthly Activity Report - {month_name} {year} - Nova Life Hospital",
                recipients=[user.email],
                html=html_body
            )

            current_app.extensions['mail'].send(msg)
            sent += 1
            print(f"✅ Monthly report sent to Dr. {user.name} ({user.email})")

        return {"status": "success", "sent": sent}

    except Exception as e:
        print(f"❌ MONTHLY REPORT ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return {"status": "error", "message": str(e)}



@celery.task
def test_email_task():
    try:
        msg = Message(
            subject="TEST EMAIL - HMS Backend",
            recipients=["afroz.sum17@gmail.com"],
            body="correct "
        )

        current_app.extensions['mail'].send(msg)

        print(" Test email sent successfully")
        return {"status": "success"}

    except Exception as e:
        print(f" Test email failed: {str(e)}")
        return {"status": "error", "message": str(e)}
