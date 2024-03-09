from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session  
from typing import List
from .. import models, schemas
from ..database import get_db


router = APIRouter()

@router.post("/patients/", response_model=schemas.Patient, tags=["patient"])
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
