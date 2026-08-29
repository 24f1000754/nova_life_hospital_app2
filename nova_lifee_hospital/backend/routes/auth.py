from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from backend.models.models import db, User, Patient , Doctor

auth_bp = Blueprint("auth", __name__)




def create_default_admin():
    admin_email = "admin@hms.com"

    admin_exists = User.query.filter_by(email=admin_email).first()
    if not admin_exists:
        admin = User(
            name="Main Admin",
            email=admin_email,
            password_hash=generate_password_hash("admin123"),
            role="admin"
        )
        db.session.add(admin)
        db.session.commit()
        print("Default admin created → admin@hms.com | admin123")


#register routes
@auth_bp.route("/api/register", methods=["POST"])
def register_patient():
    try:
        data = request.get_json()

        name = data.get("name")
        email = data.get("email")
        password = data.get("password")

        if not name or not email or not password:
            return jsonify({"error": "All fields are required"}), 400

        if User.query.filter_by(email=email).first():
            return jsonify({"error": "Email already registered"}), 409

        new_user = User(
            name=name,
            email=email,
            password_hash=generate_password_hash(password),
            role="patient"
        )

        db.session.add(new_user)
        db.session.commit()

        patient_profile = Patient(
            user_id=new_user.id,
            name=name,
            email=email,
            phone=data.get("phone"),
            gender=data.get("gender"),
            address=data.get("address")
        )

        db.session.add(patient_profile)
        db.session.commit()

        return jsonify({"message": "Patient registered successfully"}), 201

    except Exception as e:
        print("REGISTER ERROR:", e)
        return jsonify({"error": str(e)}), 500




#login routes
@auth_bp.route("/api/login", methods=["POST"])
def login():
    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password_hash, password):
        return jsonify({"error": "Invalid email or password"}), 401

    if not user.is_active:
        return jsonify({"error": "User is blocked"}), 403


    if user.role == "doctor":
        doctor = Doctor.query.filter_by(user_id=user.id).first()
        if doctor and doctor.is_blacklisted:
            return jsonify({"error": "Your account has been suspended. Contact admin."}), 403

    return jsonify({
        "message": "Login successful",
        "user_id": user.id,
        "name": user.name,
        "role": user.role
    })


#patient profile
@auth_bp.route("/api/patient/profile/<int:user_id>", methods=["GET", "PUT"])
def patient_profile(user_id):
    user = User.query.get(user_id)
    patient = Patient.query.filter_by(user_id=user_id).first()

    if not user or not patient:
        return jsonify({"error": "Patient not found"}), 404

    if request.method == "GET":
        return jsonify({
            "name": patient.name,
            "email": patient.email,
            "age": patient.age,
            "gender": patient.gender,
            "phone": patient.phone,
            "address": patient.address
        })



    if request.method == "PUT":
        data = request.get_json()

        user.name = data.get("name", user.name)
        patient.age = data.get("age", patient.age)
        patient.gender = data.get("gender", patient.gender)
        patient.phone = data.get("phone", patient.phone)

        db.session.commit()

        return jsonify({"message": "Profile updated successfully"})

#converting time to am/pm

def format_time_ampm(time_str):
    
    try:
        from datetime import datetime
        time_obj = datetime.strptime(time_str, "%H:%M")
        return time_obj.strftime("%I:%M %p")
    except:
        return time_str