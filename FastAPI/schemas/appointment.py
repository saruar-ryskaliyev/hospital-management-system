from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from .doctor import DoctorBase
from .patient import PatientBase

class AppointmentBase(BaseModel):
    doctor_id: int
    patient_id: int
    date_time: datetime
    notes: Optional[str]

class AppointmentCreate(AppointmentBase):
    pass

class Appointment(AppointmentBase):
    id: int
    doctor: DoctorBase
    patient: PatientBase

    class Config:
        orm_mode = True