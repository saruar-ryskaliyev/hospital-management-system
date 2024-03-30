from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from typing import List
from .. import models, schemas
from ..database import get_db
from ..auth import get_current_active_user
from ..models import User


router = APIRouter()


@router.post("/appointments/create/", response_model=schemas.Appointment, tags=["appointments"])
def create_appointment(
    appointment: schemas.AppointmentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_active_user(["doctor", "admin", 'staff']))
):
    db_appointment = models.Appointment(**appointment.dict())
    db.add(db_appointment)
    db.commit()
    db.refresh(db_appointment)
    return db_appointment


@router.get("/appointments/", response_model=List[schemas.Appointment], tags=["appointments"])
def read_appointments(
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_user(["doctor", "admin", 'staff']))):
    appointments = db.query(models.Appointment).options(joinedload(
        models.Appointment.doctor), joinedload(models.Appointment.patient)).offset(skip).limit(limit).all()
    # Assuming your schemas.Appointment model correctly references Pydantic models for doctor and patient
    return appointments


@router.get("/appointments/by_id/{appointment_id}", response_model=schemas.Appointment, tags=["appointments"])
def read_appointment(
        appointment_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_user(["doctor", "admin", 'staff', 'patient']))):
    db_appointment = db.query(models.Appointment).filter(
        models.Appointment.id == appointment_id).first()
    if db_appointment is None:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return db_appointment


@router.put("/appointments/update/{appointment_id}", response_model=schemas.Appointment, tags=["appointments"])
def update_appointment(
        appointment_id: int,
        appointment: schemas.AppointmentCreate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_user(["doctor", "admin", 'staff']))):

    db_appointment = db.query(models.Appointment).filter(
        models.Appointment.id == appointment_id).first()
    if db_appointment is None:
        raise HTTPException(status_code=404, detail="Appointment not found")
    db_appointment.doctor_id = appointment.doctor_id
    db_appointment.patient_id = appointment.patient_id
    db_appointment.date_time = appointment.date_time
    db_appointment.notes = appointment.notes
    db.commit()
    db.refresh(db_appointment)
    return db_appointment


@router.delete("/appointments/delete/{appointment_id}", tags=["appointments"])
def delete_appointment(
        appointment_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_user(["admin", 'staff']))):
    db_appointment = db.query(models.Appointment).filter(
        models.Appointment.id == appointment_id).first()
    if db_appointment is None:
        raise HTTPException(status_code=404, detail="Appointment not found")
    db.delete(db_appointment)
    db.commit()
    return {"message": "Appointment deleted"}



@router.get("/patients/{patient_id}/appointments", response_model=List[schemas.Appointment], tags=["appointments"])
def get_appointments_by_patient_id(
        patient_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_user(["patient", "doctor", "admin", 'staff']))):
    if current_user.role == "patient" and current_user.id != patient_id:
        raise HTTPException(status_code=403, detail="Not enough permissions to view other patients' appointments")
    appointments = db.query(models.Appointment).filter(
        models.Appointment.patient_id == patient_id).all()
    return appointments


@router.get("/doctors/{doctor_id}/appointments", response_model=List[schemas.Appointment], tags=["appointments"])
def get_appointments_by_doctor_id(
        doctor_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_user(["doctor", "admin", 'staff']))):
    if current_user.role == "doctor" and current_user.id != doctor_id:
        raise HTTPException(status_code=403, detail="Not enough permissions to view other doctors' appointments")
    appointments = db.query(models.Appointment).filter(
        models.Appointment.doctor_id == doctor_id).all()
    return appointments


@router.get("/hospitals/{hospital_id}/appointments", response_model=List[schemas.Appointment], tags=["appointments"])
def get_appointments_by_hospital_id(
        hospital_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_user(["doctor", "admin", 'staff']))):
    appointments = db.query(models.Appointment).join(models.Doctor).filter(
        models.Doctor.hospital_id == hospital_id).all()
    return appointments

