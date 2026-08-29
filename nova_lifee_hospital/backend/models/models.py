#models.py

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False)  
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    \
    patient = db.relationship("Patient", backref="user", uselist=False, cascade="all, delete-orphan")
    doctor = db.relationship("Doctor", backref="user", uselist=False, cascade="all, delete-orphan")


class Doctor(db.Model):
    __tablename__ = "doctors"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    
    specialization = db.Column(db.String(100))
    bio = db.Column(db.Text)
    is_approved = db.Column(db.Boolean, default=False)
    education = db.Column(db.String(120))
    experience = db.Column(db.String(50))
    gender = db.Column(db.String(20))
    address = db.Column(db.String(200))
    
    is_blacklisted = db.Column(db.Boolean, default=False)
    appointments = db.relationship("Appointment", backref="doctor", cascade="all, delete-orphan")
    availability = db.relationship("DoctorAvailability", backref="doctor", cascade="all, delete-orphan")


class Patient(db.Model):
    __tablename__ = "patients"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    name = db.Column(db.String(100))
    email = db.Column(db.String(120))
    age = db.Column(db.Integer)
    gender = db.Column(db.String(20))
    phone = db.Column(db.String(20))
    address = db.Column(db.String(200))
    
    
    appointments = db.relationship("Appointment", backref="patient", cascade="all, delete-orphan")


class Appointment(db.Model):
    __tablename__ = "appointments"

    id = db.Column(db.Integer, primary_key=True)

    doctor_id = db.Column(db.Integer, db.ForeignKey("doctors.id", ondelete="CASCADE"), nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey("patients.id", ondelete="CASCADE"), nullable=False)

    date = db.Column(db.String(20), nullable=False)
    time = db.Column(db.String(20), nullable=False)

    status = db.Column(db.String(20), default="Booked")  
    diagnosis = db.Column(db.Text)
    prescription = db.Column(db.Text)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class DoctorAvailability(db.Model):
    __tablename__ = "doctor_availability"

    id = db.Column(db.Integer, primary_key=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey("doctors.id", ondelete="CASCADE"), nullable=False)

    date = db.Column(db.String(20), nullable=False)
    time = db.Column(db.String(20), nullable=False)

    is_booked = db.Column(db.Boolean, default=False)