from fastapi import APIRouter, HTTPException, Depends, status
from typing import List
from sqlalchemy.orm import Session
from models.appointment import Appointment, AppointmentCreate, AppointmentModel
from database import get_db

router = APIRouter()

@router.get("/appointments", response_model=List[Appointment])
async def get_appointments(db: Session = Depends(get_db)):
    try:
        appointments = db.query(AppointmentModel).all()
        return [Appointment.from_orm(appointment) for appointment in appointments]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="예약 목록을 가져오는데 실패했습니다"
        )

@router.post("/appointments", response_model=Appointment)
async def create_appointment(appointment: AppointmentCreate, db: Session = Depends(get_db)):
    try:
        db_appointment = AppointmentModel(**appointment.dict())
        db.add(db_appointment)
        db.commit()
        db.refresh(db_appointment)
        return Appointment.from_orm(db_appointment)
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="예약 생성에 실패했습니다"
        )

@router.get("/appointments/{appointment_id}", response_model=Appointment)
async def get_appointment(appointment_id: int, db: Session = Depends(get_db)):
    appointment = db.query(AppointmentModel).filter(AppointmentModel.id == appointment_id).first()
    if appointment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="예약을 찾을 수 없습니다"
        )
    return Appointment.from_orm(appointment)

@router.delete("/appointments/{appointment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_appointment(appointment_id: int, db: Session = Depends(get_db)):
    try:
        appointment = db.query(AppointmentModel).filter(AppointmentModel.id == appointment_id).first()
        if appointment is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="예약을 찾을 수 없습니다"
            )
        db.delete(appointment)
        db.commit()
        return None
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="예약 삭제에 실패했습니다"
        ) 