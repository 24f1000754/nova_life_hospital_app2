#doctor.py
from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash
from backend.models.models import db, User, Doctor , Patient , Appointment
from backend.routes.cache import get_cache, set_cache
from datetime import datetime, timedelta , date
from backend.models.models import DoctorAvailability



doctor_bp = Blueprint("doctor", __name__)

#creating doctor here



@doctor_bp.route("/api/admin/create-doctor", methods=["POST"])
def create_doctor():
    data = request.get_json()

    name = data.get("name")
    email = data.get("email")
    password = data.get("password")
    specialization = data.get("specialization")
    bio = data.get("bio")

    if not all([name, email, password, specialization]):
        return jsonify({"error": "Missing required fields"}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Email already exists"}), 409

    hashed_password = generate_password_hash(password)

    user = User(
        name=name,
        email=email,
        password_hash=hashed_password,
        role="doctor"
    )

    db.session.add(user)
    db.session.commit()

    doctor = Doctor(
        user_id=user.id,
        specialization=specialization,
        bio=bio,
        is_approved=True
    )

    db.session.add(doctor)
    db.session.commit()

    return jsonify({"message": "Doctor account created successfully"})

#get doctor here
#doctor ki details lega


@doctor_bp.route("/api/doctors", methods=["GET"])
def get_doctors():

    try:
        cached = get_cache("doctors_list")
        if cached:
            return jsonify({"source": "cache", "data": cached})
    except Exception as e:
        print("Cache read failed:", e)

    doctors = Doctor.query.all()
    data = []

    for d in doctors:
        user = User.query.get(d.user_id)
        data.append({
            "id": d.id,
            "name": user.name if user else "Unknown",
            "specialization": d.specialization
        })

    try:
        set_cache("doctors_list", data, ex=120)
    except Exception as e:
        print("Cache write failed:", e)

    return jsonify({"source": "db", "data": data})

#specialization

@doctor_bp.route("/api/specializations", methods=["GET"])
def get_specializations():
    specs = db.session.query(Doctor.specialization).distinct().all()
    data = [s[0] for s in specs]
    return jsonify({"data": data})


@doctor_bp.route("/api/patient/available-doctors", methods=["GET"])
def available_doctors():
    today = datetime.today().date()
    end_date = today + timedelta(days=7)

    doctors = Doctor.query.all()
    result = []

    for d in doctors:
        slots = DoctorAvailability.query.filter_by(
            doctor_id=d.id,
            is_booked=False
        ).all()

        valid_slots = []

        for s in slots:
            slot_date = datetime.strptime(s.date, "%Y-%m-%d").date()
            if today <= slot_date <= end_date:
                valid_slots.append({
                    "id": s.id,
                    "date": s.date,
                    "time": s.time
                })

        if valid_slots:
            result.append({
                "id": d.id,
                "name": d.user.name,
                "specialization": d.specialization,
                "bio": d.bio,
                "slots": valid_slots
            })

    return jsonify({"data": result})




#doctor profile

@doctor_bp.route("/api/doctor/profile/<int:user_id>")
def doctor_profile(user_id):
    doctor = Doctor.query.filter_by(user_id=user_id).first()
    if not doctor:
        return jsonify({"error": "Doctor not found"}), 404

    user = User.query.get(user_id)

    return jsonify({
        "id": doctor.id,
        "name": user.name,
        "email": user.email,
        "specialization": doctor.specialization,
        "bio": doctor.bio
    })


#doctor appointments

@doctor_bp.route("/api/doctor/appointments/<int:user_id>")
def doctor_appointments(user_id):
    doctor = Doctor.query.filter_by(user_id=user_id).first()
    if not doctor:
        return jsonify({"data": []})

    apps = Appointment.query.filter_by(doctor_id=doctor.id).all()
    data = []

    for a in apps:
        patient_name = "Unknown"

        patient = Patient.query.get(a.patient_id)
        if patient:
            user = User.query.get(patient.user_id)
            if user:
                patient_name = user.name

        data.append({
            "id": a.id,
            "patient": patient_name,
            "date": a.date,
            "time": a.time,
            "status": a.status,
            "diagnosis": a.diagnosis,
            "prescription": a.prescription
        })

    return jsonify({"data": data})




#doctor stats

@doctor_bp.route("/api/doctor/stats/<int:user_id>")
def doctor_stats(user_id):
    doctor = Doctor.query.filter_by(user_id=user_id).first()
    apps = Appointment.query.filter_by(doctor_id=doctor.id).all()

    today_str = str(date.today())

    today = len([a for a in apps if a.date == today_str])
    total = len(apps)
    pending = len([a for a in apps if a.status == "Booked"])
    completed = len([a for a in apps if a.status == "Completed"])

    patients = len(set([a.patient_id for a in apps]))

    return jsonify({
        "today": today,
        "total": total,
        "pending": pending,
        "completed": completed,
        "patients": patients
    })


#doctr kepatents

@doctor_bp.route("/api/doctor/patients/<int:user_id>")
def doctor_patients(user_id):
    doctor = Doctor.query.filter_by(user_id=user_id).first()

    apps = Appointment.query.filter_by(doctor_id=doctor.id).all()
    patient_ids = list(set([a.patient_id for a in apps]))

    patients = Patient.query.filter(Patient.id.in_(patient_ids)).all()

    data = []
    for p in patients:
        data.append({
            "id": p.id,
            "name": p.user.name,
            "email": p.user.email,
            "phone": p.phone   
        })

    return jsonify({"data": data})



#update appointment

@doctor_bp.route("/api/doctor/update-status", methods=["PUT"])
def update_status():
    data = request.get_json()
    app = Appointment.query.get(data["appointment_id"])

    app.status = data["status"]
    db.session.commit()

    return jsonify({"message": "Status updated"})


#add treatment here
@doctor_bp.route("/api/doctor/add-treatment", methods=["PUT"])
def add_treatment():
    data = request.get_json()
    app = Appointment.query.get(data["appointment_id"])

    app.diagnosis = data["diagnosis"]
    app.prescription = data["prescription"]
    app.status = "Completed"

    db.session.commit()

    return jsonify({"message": "Treatment added"})


@doctor_bp.route("/api/doctor/add-availability", methods=["POST"])
def add_availability():
    data = request.json

    doctor = Doctor.query.filter_by(user_id=data["doctor_id"]).first()

    slot = DoctorAvailability(
        doctor_id=doctor.id,
        date=data["date"],
        time=data["time"]
    )

    db.session.add(slot)
    db.session.commit()

    return jsonify({"message": "Slot added"})

#update doctor profile

@doctor_bp.route("/api/doctor/update-profile/<int:user_id>", methods=["PUT"])
def update_doctor_profile(user_id):
    doctor = Doctor.query.filter_by(user_id=user_id).first()
    user = User.query.get(user_id)

    data = request.json

    user.name = data["name"]
    user.email = data["email"]

    doctor.specialization = data["specialization"]
    doctor.bio = data["bio"]
    doctor.gender = data["gender"]
    doctor.address = data["address"]
    doctor.education = data["education"]
    doctor.experience = data["experience"]

    db.session.commit()
    return jsonify({"message":"Profile updated"})



@doctor_bp.route("/api/patient/doctor-availability-week", methods=["GET"])
def get_doctor_availability_week():
    today = datetime.today().date()
    dates = [(today + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(7)]
    doctors = Doctor.query.filter_by(is_approved=True).all()
    result = []
    
    for doctor in doctors:
        user = User.query.get(doctor.user_id)
        week_availability = [{"date": date_str, "available": DoctorAvailability.query.filter_by(doctor_id=doctor.id, date=date_str, is_booked=False).count() > 0} for date_str in dates]
        result.append({"doctor_name": user.name if user else "Unknown", "specialization": doctor.specialization or "None", "availability": week_availability})
    
    return jsonify({"dates": dates, "doctors": result})
