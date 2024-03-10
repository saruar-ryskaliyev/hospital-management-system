from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session  
from typing import List
from .. import models, schemas
from ..database import get_db

router = APIRouter()


@router.post("/doctors/create/", response_model=schemas.Doctor, tags=["doctors"])
def create_doctor(doctor: schemas.DoctorCreate, db: Session = Depends(get_db)):
    db_doctor = models.Doctor(**doctor.dict())
    db.add(db_doctor)
    db.commit()
    db.refresh(db_doctor)
    return db_doctor


@router.get("/doctors/", response_model=List[schemas.Doctor], tags=["doctors"])
def read_doctors(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    doctors = db.query(models.Doctor).offset(skip).limit(limit).all()
    return doctors


@router.get("/doctors/by_id/{doctor_id}", response_model=schemas.Doctor, tags=["doctors"])
def read_doctor(doctor_id: int, db: Session = Depends(get_db)):
    db_doctor = db.query(models.Doctor).filter(models.Doctor.id == doctor_id).first()
    if db_doctor is None:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return db_doctor


@router.put("/doctors/{doctor_id}/reassign/{hospital_id}", tags=["doctors"])
def reassign_doctor(doctor_id: int, hospital_id: int, db: Session = Depends(get_db)):
    db_doctor = db.query(models.Doctor).filter(models.Doctor.id == doctor_id).first()
    if db_doctor is None:
        raise HTTPException(status_code=404, detail="Doctor not found")
    db_doctor.hospital_id = hospital_id
    db.commit()
    return {"message": "Doctor reassigned"}


@router.put("/doctors/update/{doctor_id}", response_model=schemas.Doctor, tags=["doctors"])
def update_doctor(doctor_id: int, doctor: schemas.DoctorCreate, db: Session = Depends(get_db)):
    db_doctor = db.query(models.Doctor).filter(models.Doctor.id == doctor_id).first()
    if db_doctor is None:
        raise HTTPException(status_code=404, detail="Doctor not found")
    db_doctor.name = doctor.name
    db_doctor.specialization = doctor.specialization
    db.commit()
    db.refresh(db_doctor)
    return db_doctor


@router.delete("/doctors/delete/{doctor_id}", tags=["doctors"])
def delete_doctor(doctor_id: int, db: Session = Depends(get_db)):
    db_doctor = db.query(models.Doctor).filter(models.Doctor.id == doctor_id).first()
    if db_doctor is None:
        raise HTTPException(status_code=404, detail="Doctor not found")
    
    db.query(models.Appointment).filter(models.Appointment.doctor_id == doctor_id).delete()

    
    db.delete(db_doctor)
    db.commit()
    return {"message": "Doctor deleted"}
