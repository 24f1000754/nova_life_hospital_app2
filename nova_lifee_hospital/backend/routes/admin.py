#admin.py

from flask import Blueprint, request, jsonify
from backend.models.models import db, User, Doctor, Patient, Appointment
from werkzeug.security import generate_password_hash

admin_bp = Blueprint("admin", __name__)

#stats

@admin_bp.route("/api/admin/stats")
def admin_stats():
    return jsonify({
        "doctors": Doctor.query.count(),
        "patients": Patient.query.count(),
        "appointments": Appointment.query.count()
    })

#create doctor

@admin_bp.route("/api/admin/create-doctor", methods=["POST"])
def create_doctor():
    data = request.get_json()

    if User.query.filter_by(email=data["email"]).first():
        return jsonify({"error": "Email already exists"}), 409

    user = User(
        name=data["name"],
        email=data["email"],
        password_hash=generate_password_hash(data["password"]),
        role="doctor"
    )
    db.session.add(user)
    db.session.commit()

    doctor = Doctor(
        user_id=user.id,
        specialization=data["specialization"],
        bio=data.get("bio", ""),
        is_approved=True
    )
    db.session.add(doctor)
    db.session.commit()

    return jsonify({"message": "Doctor created"})

# get doctors for admini

@admin_bp.route("/api/admin/doctors")
def get_doctors():
    doctors = Doctor.query.all()
    data = []

    for d in doctors:
        user = User.query.get(d.user_id)
        
        data.append({
            "id": d.id,
            "name": user.name if user else "",
            "email": user.email if user else "",
            "specialization": d.specialization,
            "bio": d.bio,
            "gender": d.gender,  
            "address": d.address,  
            "education": d.education,  
            "experience": d.experience,  
            "is_blacklisted": d.is_blacklisted  
        })

    return jsonify({"data": data})

#get all patient

@admin_bp.route("/api/admin/patients")
def get_patients():
    patients = Patient.query.all()
    data = []

    for p in patients:
        data.append({
            "id": p.id,
            "name": p.user.name,
            "email": p.user.email,
            "age": p.age,  
            "gender": p.gender,  
            "phone": p.phone,  
            "address": p.address  
        })

    return jsonify({"data": data})

# all appointment

@admin_bp.route("/api/admin/appointments")
def all_appointments():
    apps = Appointment.query.all()
    data = []

    for a in apps:
        data.append({
            "id": a.id,
            "doctor": a.doctor.user.name,
            "patient": a.patient.user.name,
            "date": a.date,
            "time": a.time,
            "status": a.status
        })

    return jsonify({"data": data})

#blacklist doctor
#yha se doctor ko delete kr skta h

@admin_bp.route("/api/admin/delete-doctor/<int:id>", methods=["DELETE"])
def delete_doctor(id):
    doctor = Doctor.query.get(id)

    if not doctor:
        return jsonify({"error": "Doctor not found"}), 404

    db.session.delete(doctor.user)
    db.session.commit()

    return jsonify({"message": "Doctor removed"})


#search for admin





@admin_bp.route("/api/admin/search")
def admin_search():
    
    q = request.args.get("q", "").strip()
    
    if not q:
        return jsonify({"doctors": [], "patients": []})
    
    # search doctors by name, email, or specialization

    
    doctors = Doctor.query.join(User).filter(
        (User.name.ilike(f"%{q}%")) | 
        (User.email.ilike(f"%{q}%")) | 
        (Doctor.specialization.ilike(f"%{q}%"))
    ).all()
    
    # search patients by name or email
    patients = Patient.query.join(User).filter(
        (User.name.ilike(f"%{q}%")) | 
        (User.email.ilike(f"%{q}%"))
    ).all()
    
    # format doctor data
    d_data = []
    for d in doctors:
        user = User.query.get(d.user_id)
        d_data.append({
            "id": d.id,
            "name": user.name if user else "Unknown",
            "email": user.email if user else "",
            "specialization": d.specialization,
            "bio": d.bio,
            "gender": d.gender,
            "address": d.address,
            "education": d.education,
            "experience": d.experience,
            "is_blacklisted": d.is_blacklisted
        })
    
    # format patient data
    p_data = []
    for p in patients:
        user = User.query.get(p.user_id)
        p_data.append({
            "id": p.id,
            "name": user.name if user else "Unknown",
            "email": user.email if user else "",
            "age": p.age,
            "gender": p.gender,
            "phone": p.phone,
            "address": p.address
        })
    
    return jsonify({
        "doctors": d_data, 
        "patients": p_data
    })





#delete patient 

@admin_bp.route("/api/admin/delete-patient/<int:id>", methods=["DELETE"])
def delete_patient(id):
    patient = Patient.query.get(id)
    user = User.query.get(patient.user_id)

    db.session.delete(patient)
    db.session.delete(user)
    db.session.commit()

    return jsonify({"message":"Patient deleted"})


#update doctor details dfor admin
@admin_bp.route("/api/admin/update-doctor/<int:id>", methods=["PUT"])
def update_doctor(id):
    data = request.get_json()
    doctor = Doctor.query.get(id)

    doctor.specialization = data["specialization"]
    doctor.bio = data["bio"]

    db.session.commit()
    return jsonify({"message":"Doctor updated"})


#blacklist doctor for adminu
@admin_bp.route("/api/admin/blacklist-doctor/<int:id>", methods=["PUT"])
def blacklist_doctor(id):
    
    data = request.get_json()
    doctor = Doctor.query.get(id)
    
    if not doctor:
        return jsonify({"error": "Doctor not found"}), 404
    
    # toggle blacklist status
    doctor.is_blacklisted = data.get("is_blacklisted", True)
    db.session.commit()
    
    status = "blacklisted" if doctor.is_blacklisted else "unblacklisted"
    return jsonify({"message": f"Doctor {status} successfully"})


#update patients details for admins
@admin_bp.route("/api/admin/update-patient/<int:id>", methods=["PUT"])
def update_patient(id):
    
    data = request.get_json()
    patient = Patient.query.get(id)
    
    if not patient:
        return jsonify({"error": "Patient not found"}), 404
    
    user = User.query.get(patient.user_id)
    
    # update user name
    if "name" in data:
        user.name = data["name"]
        patient.name = data["name"]
    
    # update patient details
    if "age" in data:
        patient.age = data["age"]
    if "gender" in data:
        patient.gender = data["gender"]
    if "phone" in data:
        patient.phone = data["phone"]
    if "address" in data:
        patient.address = data["address"]
    
    db.session.commit()
    return jsonify({"message": "Patient updated successfully"})