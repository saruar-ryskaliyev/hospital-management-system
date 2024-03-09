from fastapi import FastAPI
from sqlalchemy.orm import Session
# Assuming your application is inside a directory named "app" at the root level.
from .database import engine, SessionLocal
from .models import Base  # Ensure Base is imported correctly in your models/__init__.py
# Adjusted imports based on the provided structure and the corrected __init__.py in the routers directory
from .routers import appointment_router, hospital_router, doctor_router, patient_router

# Create d atabase tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Include the routers
# app.include_router(doctor_router)
# app.include_router(patient_router)
# app.include_router(hospital_router)
app.include_router(appointment_router)
app.include_router(hospital_router)
app.include_router(doctor_router)
app.include_router(patient_router)
