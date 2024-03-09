from pydantic import BaseModel
from .doctor import Doctor
from typing import List

class HospitalBase(BaseModel):
    name: str
    address: str
    contact: str

class HospitalCreate(HospitalBase):
    pass

class Hospital(HospitalBase):
    id: int
    doctors: List[Doctor] = []

    class Config:
        orm_mode = True