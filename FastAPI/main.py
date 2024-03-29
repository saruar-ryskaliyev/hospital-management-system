from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
# Assuming your application is inside a directory named "app" at the root level.
from .database import engine, SessionLocal, get_db
from .models import Base  # Ensure Base is imported correctly in your models/__init__.py
# Adjusted imports based on the provided structure and the corrected __init__.py in the routers directory
from .routers import appointment_router, hospital_router, doctor_router, patient_router
from . import auth
from typing import Annotated
from starlette import status
from .auth import get_current_user

# Create d atabase tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Include the routers
# app.include_router(doctor_router)
# app.include_router(patient_router)
# app.include_router(hospital_router)
app.include_router(appointment_router)
app.include_router(hospital_router)
app.include_router(doctor_router)
app.include_router(patient_router)
app.include_router(auth.router)


dp_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[auth.User, Depends(get_current_user)]


@app.get("/", status_code=status.HTTP_200_OK)
async def user(user: user_dependency, db: dp_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication failed")
    return {"User": user}
