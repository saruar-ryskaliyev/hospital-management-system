from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session  
from typing import List
from .. import models, schemas
from ..database import get_db

router = APIRouter()

@router.post("/doctors/", response_model=schemas.Doctor, tags=["doctors"])
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
