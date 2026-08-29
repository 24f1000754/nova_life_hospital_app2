# nova-life-hospital
A Hospital Management System (HMS) is a comprehensive, integrated software solution that streamlines and automates a healthcare facility's clinical, administrative, and financial operations. 

# for reactivate venv and npm
# Python Virtual Environment:
# Root folder mein jao
cd E:\nova_life_hospital_24f1000754

# Naya venv banao
python -m venv venv

# Activate karo
venv\Scripts\Activate.ps1

# Sab packages install karo
pip install -r requirements.txt

Node Modules:
bash# Frontend folder mein ja (jahan package.json hai)
cd frontend

# Reinstall karo
npm install

# run backend
python -m backend.app

# run frontend
cd frontend
npm run dev

# run celery
celery -A backend.routes.celery_worker worker --loglevel=info --pool=solo

# run beat
celery -A backend.routes.celery_worker beat --loglevel=info

# run manually appointment reminder
celery -A backend.routes.celery_worker call backend.routes.tasks.daily_appointment_reminder

# run manually monthly report
celery -A backend.routes.celery_worker call backend.routes.tasks.monthly_doctor_report
