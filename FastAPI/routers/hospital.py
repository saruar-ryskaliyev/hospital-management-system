from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from typing import List
from .. import models, schemas
from ..database import get_db
from ..auth import get_current_active_user
from ..models import User


router = APIRouter()


@router.post("/hospitals/create/", response_model=schemas.Hospital, tags=["hospitals"])
def create_hospital(
        hospital: schemas.HospitalCreate, 
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_user(["admin"]))):
    db_hospital = models.Hospital(**hospital.dict())
    db.add(db_hospital)
    db.commit()
    db.refresh(db_hospital)
    return db_hospital


@router.get("/hospitals/", response_model=List[schemas.Hospital], tags=["hospitals"])
def read_hospitals(
        skip: int = 0, 
        limit: int = 100, 
        db: Session = Depends(get_db)):
    
    hospitals = db.query(models.Hospital).options(joinedload(
        models.Hospital.doctors)).offset(skip).limit(limit).all()
    return hospitals


@router.get("/hospitals/by_id/{hospital_id}", response_model=schemas.Hospital, tags=["hospitals"])
def read_hospital(hospital_id: int, db: Session = Depends(get_db)):
    db_hospital = db.query(models.Hospital).filter(
        models.Hospital.id == hospital_id).first()
    if db_hospital is None:
        raise HTTPException(status_code=404, detail="Hospital not found")
    return db_hospital


@router.delete("/hospitals/delete/{hospital_id}", tags=["hospitals"])
def delete_hospital(
        hospital_id: int, 
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_user(["admin"]))):
    db_hospital = db.query(models.Hospital).filter(
        models.Hospital.id == hospital_id).first()
    if db_hospital is None:
        raise HTTPException(status_code=404, detail="Hospital not found")
    db.delete(db_hospital)
    db.commit()
    return {"message": "Hospital deleted"}


@router.put("/hospitals/update/{hospital_id}", response_model=schemas.Hospital, tags=["hospitals"])
def update_hospital(
        hospital_id: int, 
        hospital: schemas.HospitalCreate, 
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_user(["admin"]))):
    db_hospital = db.query(models.Hospital).filter(
        models.Hospital.id == hospital_id).first()
    if db_hospital is None:
        raise HTTPException(status_code=404, detail="Hospital not found")
    db_hospital.name = hospital.name
    db_hospital.address = hospital.address
    db_hospital.contact = hospital.contact
    db.commit()
    db.refresh(db_hospital)
    return db_hospital


@router.get("/hospitals/{hospital_id}/doctors", response_model=List[schemas.Doctor], tags=["hospitals"])
def read_doctors_by_hospital(
        hospital_id: int, 
        db: Session = Depends(get_db)):
    doctors = db.query(models.Doctor).filter(hospital_id == models.Doctor.hospital_id).all()
    return doctors
