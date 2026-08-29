#appointment.py

from flask import Blueprint, request, jsonify, send_file
from backend.models.models import db, Appointment, DoctorAvailability, Doctor, Patient, User
from backend.routes.tasks import export_patient_report
from datetime import datetime, timedelta
import os
import glob

appointment_bp = Blueprint("appointment", __name__)




@appointment_bp.route("/api/doctor/add-availability", methods=["POST"])
def add_availability():
    
    data = request.get_json()

    doctor_id = data.get("doctor_id")
    date = data.get("date")
    time = data.get("time")

    if not all([doctor_id, date, time]):
        return jsonify({"error": "All fields required"}), 400

    slot_exists = DoctorAvailability.query.filter_by(
        doctor_id=doctor_id,
        date=date,
        time=time
    ).first()

    if slot_exists:
        return jsonify({"error": "Slot already exists"}), 409

    slot = DoctorAvailability(
        doctor_id=doctor_id,
        date=date,
        time=time
    )

    db.session.add(slot)
    db.session.commit()

    return jsonify({"message": "Availability slot added successfully"})


#book appointment routes

@appointment_bp.route("/api/patient/book-appointment", methods=["POST"])
def book_appointment():
    
    try:
        data = request.get_json()

        doctor_id = data.get("doctor_id")
        user_id = data.get("patient_id")
        slot_id = data.get("slot_id")

        if not all([doctor_id, user_id, slot_id]):
            return jsonify({"error": "All fields required"}), 400

        slot = DoctorAvailability.query.get(slot_id)
        if not slot or slot.is_booked:
            return jsonify({"error": "Slot not available"}), 409

        patient = Patient.query.filter_by(user_id=user_id).first()
        if not patient:
            return jsonify({"error": "Patient profile not found"}), 404

        appointment = Appointment(
            doctor_id=doctor_id,
            patient_id=patient.id,
            date=slot.date,
            time=slot.time,
            status="Booked"
        )

        slot.is_booked = True

        db.session.add(appointment)
        db.session.commit()

        return jsonify({"message": "Appointment booked successfully"})

    except Exception as e:
        print("BOOKING ERROR:", e)
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

#patient appoint
@appointment_bp.route("/api/patient/appointments/<int:user_id>", methods=["GET"])
def patient_appointments(user_id):
    
    
    patient = Patient.query.filter_by(user_id=user_id).first()
    if not patient:
        return jsonify({"data": []})

    appointments = Appointment.query.filter_by(patient_id=patient.id).all()

    data = []
    for a in appointments:
        doctor = Doctor.query.get(a.doctor_id)
        user = User.query.get(doctor.user_id) if doctor else None

        data.append({
            "id": a.id,
            "doctor": user.name if user else "Unknown",
            "specialization": doctor.specialization if doctor else "N/A",
            "date": a.date,
            "time": a.time,
            "status": a.status
        })


    return jsonify({"data": data})


#get treatments details

@appointment_bp.route("/api/patient/treatment-details/<int:appointment_id>", methods=["GET"])
def get_treatment_details(appointment_id):
    
    try:
        
        appointment = Appointment.query.get(appointment_id)
        
        if not appointment:
            return jsonify({"error": "Appointment not found"}), 404
        
        
        doctor = Doctor.query.get(appointment.doctor_id)
        doctor_user = User.query.get(doctor.user_id) if doctor else None
        
        
        treatment_data = {
            "appointment_id": appointment.id,
            "doctor": doctor_user.name if doctor_user else "Unknown",
            "specialization": doctor.specialization if doctor else "N/A",
            "date": appointment.date,
            "time": appointment.time,
            "status": appointment.status,
            "diagnosis": appointment.diagnosis or "Not provided yet",
            "prescription": appointment.prescription or "Not provided yet",
            "created_at": appointment.created_at.strftime("%Y-%m-%d %H:%M") if appointment.created_at else None
        }
        
        return jsonify(treatment_data)
        
    except Exception as e:
        print(f" TREATMENT DETAILS ERROR: {str(e)}")
        return jsonify({"error": str(e)}), 500

#get available slots
@appointment_bp.route("/api/patient/available-slots/<int:doctor_id>", methods=["GET"])
def get_available_slots(doctor_id):
    
    today = datetime.today().date()
    end_date = today + timedelta(days=7)

    slots = DoctorAvailability.query.filter(
        DoctorAvailability.doctor_id == doctor_id,
        DoctorAvailability.is_booked == False,
        DoctorAvailability.date >= str(today),
        DoctorAvailability.date <= str(end_date)
    ).all()

    data = []
    for s in slots:
        data.append({
            "id": s.id,
            "date": s.date,
            "time": s.time
        })

    return jsonify({"data": data})

#cancel appoint

@appointment_bp.route("/api/patient/cancel-appointment", methods=["PUT"])
def cancel_appointment():
    
    data = request.get_json()
    appointment_id = data.get("appointment_id")

    appointment = Appointment.query.get(appointment_id)
    if not appointment:
        return jsonify({"error": "Appointment not found"}), 404

    appointment.status = "Cancelled"

    slot = DoctorAvailability.query.filter_by(
        doctor_id=appointment.doctor_id,
        date=appointment.date,
        time=appointment.time
    ).first()

    if slot:
        slot.is_booked = False

    db.session.commit()
    return jsonify({"message": "Appointment cancelled successfully"})

#patient can reshedule thier appoint

@appointment_bp.route("/api/patient/reschedule", methods=["PUT"])
def reschedule():
    
    data = request.get_json()

    appt = Appointment.query.get(data.get("appointment_id"))
    if not appt:
        return jsonify({"error": "Appointment not found"}), 404

    old_slot = DoctorAvailability.query.filter_by(
        doctor_id=appt.doctor_id,
        date=appt.date,
        time=appt.time
    ).first()
    
    if old_slot:
        old_slot.is_booked = False

    appt.date = data.get("date")
    appt.time = data.get("time")
    
    db.session.commit()

    return jsonify({"message": "Appointment rescheduled successfully"})


#csv export
@appointment_bp.route("/api/patient/export-report", methods=["POST"])
def export_report():
    
    try:
        data = request.get_json()
        user_id = data.get("patient_id")

        if not user_id:
            return jsonify({"error": "Patient ID required"}), 400

        patient = Patient.query.filter_by(user_id=user_id).first()
        
        if not patient:
            return jsonify({"error": "Patient not found"}), 404

        print(f"🔄 Starting export for Patient ID: {patient.id}, User ID: {user_id}")

        task = export_patient_report.delay(patient.id)

        return jsonify({
            "message": "Report generation started",
            "task_id": task.id,
            "patient_id": patient.id
        })

    except Exception as e:
        print(f" EXPORT ERROR: {str(e)}")
        return jsonify({"error": str(e)}), 500

#download report
@appointment_bp.route("/api/patient/download-report/<int:user_id>", methods=["GET"])
def download_report(user_id):
    
    try:
        patient = Patient.query.filter_by(user_id=user_id).first()
        
        if not patient:
            return jsonify({"error": "Patient not found"}), 404

        patient_id = patient.id
        
        print(f" Download request for Patient ID: {patient_id}, User ID: {user_id}")

        reports_dir = "reports"
        
        if not os.path.exists(reports_dir):
            print(f" Reports folder not found: {reports_dir}")
            return jsonify({
                "error": "No reports folder found. Please generate report first."
            }), 404

        pattern = os.path.join(reports_dir, f"patient_{patient_id}_report_*.csv")
        patient_files = glob.glob(pattern)

        print(f" Looking for files matching: {pattern}")
        print(f" Found files: {patient_files}")

        if not patient_files:
            return jsonify({
                "error": "Report not found. Please click 'Generate Report' first and wait 5 seconds."
            }), 404

        latest_file = sorted(patient_files)[-1]
        
        print(f" Sending file: {latest_file}")

        return send_file(
            latest_file,
            mimetype='text/csv',
            as_attachment=True,
            download_name=f"treatment_report_patient_{patient_id}.csv"
        )

    except Exception as e:
        print(f"❌ DOWNLOAD ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": f"Download failed: {str(e)}"}), 500


#admin routes here

@appointment_bp.route("/api/appointment/update-status", methods=["PUT"])
def update_status():
    
    data = request.get_json()

    appointment_id = data.get("appointment_id")
    new_status = data.get("status")

    appointment = Appointment.query.get(appointment_id)

    if not appointment:
        return jsonify({"error": "Appointment not found"}), 404

    appointment.status = new_status
    db.session.commit()

    return jsonify({"message": "Appointment status updated"})


@appointment_bp.route("/api/admin/add-availability", methods=["POST"])
def admin_add_availability():
    
    data = request.get_json()

    slot = DoctorAvailability(
        doctor_id=data["doctor_id"],
        date=data["date"],
        time=data["time"]
    )

    db.session.add(slot)
    db.session.commit()

    return jsonify({"message": "Slot added successfully"})


@appointment_bp.route("/api/admin/doctor-slots/<int:doctor_id>")
def admin_doctor_slots(doctor_id):
    
    slots = DoctorAvailability.query.filter_by(doctor_id=doctor_id).all()

    data = []
    for s in slots:
        data.append({
            "id": s.id,
            "date": s.date,
            "time": s.time,
            "is_booked": s.is_booked
        })

    return jsonify({"data": data})

#slot delete kr skta h
@appointment_bp.route("/api/admin/delete-slot/<int:id>", methods=["DELETE"])
def delete_slot(id):
    
    slot = DoctorAvailability.query.get(id)
    
    if not slot:
        return jsonify({"error": "Slot not found"}), 404
        
    db.session.delete(slot)
    db.session.commit()
    
    return jsonify({"message": "Slot deleted successfully"})