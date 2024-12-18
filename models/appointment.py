from sqlalchemy import Column, Integer, String, DateTime
from database import Base
from pydantic import BaseModel
from datetime import datetime

# SQLAlchemy 모델
class AppointmentModel(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)
    patientName = Column(String(100))
    date = Column(String(50))
    time = Column(String(50))
    symptoms = Column(String(500))
    created_at = Column(DateTime, default=datetime.utcnow)

# Pydantic 모델
class AppointmentBase(BaseModel):
    patientName: str
    date: str
    time: str
    symptoms: str

class AppointmentCreate(AppointmentBase):
    pass

class Appointment(AppointmentBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
        from_attributes = True