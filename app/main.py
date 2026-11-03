from fastapi import FastAPI, Body, status
from typing import Annotated
from app.schema.doctor import Doctor
from app.models.doctor import Doctor as DoctorDB
from app.dependencies import SessionDep
from sqlmodel import select

app = FastAPI()


@app.post('/create', status_code=status.HTTP_201_CREATED)
async def create_doctor(
    doctor_info: Annotated[Doctor, Body()],
    session: SessionDep
):

    # use the **doctor_info in the constructor of model for test if it's work or not
    doctor_for_db = DoctorDB(
        name=doctor_info.name,
        description=doctor_info.description,
        phone_number=doctor_info.phone_number,
        address=doctor_info.address
    )

    session.add(doctor_for_db)
    session.commit()

    return doctor_for_db


@app.get(
    '/doctors',
    status_code=status.HTTP_200_OK
)
async def show_doctors(
    session: SessionDep
):
    return session.exec(select(DoctorDB)).all()
