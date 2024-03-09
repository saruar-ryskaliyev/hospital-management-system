from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from typing import List
from .. import models, schemas
from ..database import get_db

router = APIRouter()

@router.post("/hospitals/", response_model=schemas.Hospital, tags=["hospitals"])
def create_hospital(hospital: schemas.HospitalCreate, db: Session = Depends(get_db)):
    db_hospital = models.Hospital(**hospital.dict())
    db.add(db_hospital)
    db.commit()
    db.refresh(db_hospital)
    return db_hospital

@router.get("/hospitals/", response_model=List[schemas.Hospital], tags=["hospitals"])
def read_hospitals(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    hospitals = db.query(models.Hospital).options(joinedload(models.Hospital.doctors)).offset(skip).limit(limit).all()
    return hospitals