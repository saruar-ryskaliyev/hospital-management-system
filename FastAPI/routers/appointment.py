from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from typing import List
from .. import models, schemas
from ..database import get_db

router = APIRouter()


@router.post("/appointments/create/", response_model=schemas.Appointment, tags=["appointments"])
def create_appointment(appointment: schemas.AppointmentCreate, db: Session = Depends(get_db)):
    db_appointment = models.Appointment(**appointment.dict())
    db.add(db_appointment)
    db.commit()
    db.refresh(db_appointment)
    return db_appointment


@router.get("/appointments/", response_model=List[schemas.Appointment], tags=["appointments"])
def read_appointments(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    appointments = db.query(models.Appointment).options(joinedload(
        models.Appointment.doctor), joinedload(models.Appointment.patient)).offset(skip).limit(limit).all()
    # Assuming your schemas.Appointment model correctly references Pydantic models for doctor and patient
    return appointments


@router.get("/appointments/by_id/{appointment_id}", response_model=schemas.Appointment, tags=["appointments"])
def read_appointment(appointment_id: int, db: Session = Depends(get_db)):
    db_appointment = db.query(models.Appointment).filter(
        models.Appointment.id == appointment_id).first()
    if db_appointment is None:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return db_appointment


@router.put("/appointments/update/{appointment_id}", response_model=schemas.Appointment, tags=["appointments"])
def update_appointment(appointment_id: int, appointment: schemas.AppointmentCreate, db: Session = Depends(get_db)):
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
def delete_appointment(appointment_id: int, db: Session = Depends(get_db)):
    db_appointment = db.query(models.Appointment).filter(
        models.Appointment.id == appointment_id).first()
    if db_appointment is None:
        raise HTTPException(status_code=404, detail="Appointment not found")
    db.delete(db_appointment)
    db.commit()
    return {"message": "Appointment deleted"}
