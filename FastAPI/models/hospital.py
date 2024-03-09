from ..database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship


class Hospital(Base):
    __tablename__ = "hospitals"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    address = Column(String)
    contact = Column(String)
    doctors = relationship("Doctor", back_populates="hospital")