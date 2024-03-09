from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from .doctor import Doctor
from .patient import Patient

class AppointmentBase(BaseModel):
    date_time: datetime
    notes: Optional[str]

class AppointmentCreate(AppointmentBase):
    pass

class Appointment(AppointmentBase):
    id: int
    doctor: Doctor
    patient: Patient

    class Config:
        orm_mode = True