from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session  
from typing import List
from .. import models, schemas
from ..database import get_db


router = APIRouter()

@router.post("/patients/create/", response_model=schemas.Patient, tags=["patient"])
def create_patient(patient: schemas.PatientCreate, db: Session = Depends(get_db)):
    db_patient = models.Patient(**patient.dict())
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    return db_patient


@router.get("/patients/", response_model=List[schemas.Patient], tags=["patient"])
def read_patients(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    patients = db.query(models.Patient).offset(skip).limit(limit).all()
    return patients


@router.get("/patients/by_id/{patient_id}", response_model=schemas.Patient, tags=["patient"])
def read_patient(patient_id: int, db: Session = Depends(get_db)):
    db_patient = db.query(models.Patient).filter(models.Patient.id == patient_id).first()
    if db_patient is None:
        raise HTTPException(status_code=404, detail="Patient not found")
    return db_patient


@router.put("/patients/update/{patient_id}", response_model=schemas.Patient, tags=["patient"])
def update_patient(patient_id: int, patient: schemas.PatientCreate, db: Session = Depends(get_db)):
    db_patient = db.query(models.Patient).filter(models.Patient.id == patient_id).first()
    if db_patient is None:
        raise HTTPException(status_code=404, detail="Patient not found")
    db_patient.name = patient.name
    db_patient.dob = patient.dob
    db_patient.medical_history = patient.medical_history
    db.commit()
    db.refresh(db_patient)
    return db_patient


@router.delete("/patients/delete/{patient_id}", tags=["patient"])
def delete_patient(patient_id: int, db: Session = Depends(get_db)):
    db_patient = db.query(models.Patient).filter(models.Patient.id == patient_id).first()
    if db_patient is None:
        raise HTTPException(status_code=404, detail="Patient not found")
    

    db.query(models.Appointment).filter(models.Appointment.patient_id == patient_id).delete()


    db.delete(db_patient)
    db.commit()
    return {"message": "Patient deleted"}