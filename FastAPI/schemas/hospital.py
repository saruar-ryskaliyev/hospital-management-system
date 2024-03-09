from pydantic import BaseModel

class HospitalBase(BaseModel):
    name: str
    address: str
    contact: str

class HospitalCreate(HospitalBase):
    pass

class Hospital(HospitalBase):
    id: int

    class Config:
        orm_mode = True