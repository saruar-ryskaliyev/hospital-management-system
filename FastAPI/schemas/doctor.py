from pydantic import BaseModel
from typing import Optional


class DoctorBase(BaseModel):
    name: str
    specialization: str

class DoctorCreate(DoctorBase):
    hospital_id: Optional[int] = None

class Doctor(DoctorBase):
    id: int
    hospital_id: Optional[int] = None

    class Config:
        orm_mode = True
