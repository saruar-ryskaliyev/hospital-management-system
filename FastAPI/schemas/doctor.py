from pydantic import BaseModel


class DoctorBase(BaseModel):
    name: str
    specialization: str

class DoctorCreate(DoctorBase):
    hospital_id: int

class Doctor(DoctorBase):
    id: int
    hospital_id: int

    class Config:
        orm_mode = True
