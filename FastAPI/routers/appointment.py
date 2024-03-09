from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session  
from typing import List
from .. import models, schemas
from ..database import get_db

router = APIRouter()

@router.post("/appointments/", response_model=schemas.Appointment, tags=["appointments"])
def create_appointment(appointment: schemas.AppointmentCreate, db: Session = Depends(get_db)):
    db_appointment = models.Appointment(**appointment.dict())
    db.add(db_appointment)
    db.commit()
    db.refresh(db_appointment)
    return db_appointment

@router.get("/appointments/", response_model=List[schemas.Appointment], tags=["appointments"])
def read_appointments(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    appointments = db.query(models.Appointment).offset(skip).limit(limit).all()
    return appointments