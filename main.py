from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import appointments
from database import engine
from models.appointment import AppointmentModel
import json
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# 데이터베이스 테이블 생성
AppointmentModel.metadata.create_all(bind=engine)

# CORS 설정
origins = json.loads(os.getenv("BACKEND_CORS_ORIGINS", '["http://localhost:3000"]'))

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(appointments.router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "Hospital Appointment API"} 