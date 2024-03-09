from pydantic import BaseModel
from typing import Optional
from datetime import date

class PatientBase(BaseModel):
    name: str
    dob: date
    medical_history: Optional[str]



class PatientCreate(PatientBase):
    pass

class Patient(PatientBase):
    id: int


    class Config:
        orm_mode = True