from fastapi import FastAPI, Body, status, Path, HTTPException
from typing import Annotated
from app.schema.doctor import Doctor, DoctorUpdate
from app.models.doctor import Doctor as DoctorDB
from app.dependencies import SessionDep
from app.core.database import create_db_and_tables
from sqlmodel import select
from openai import OpenAI

app = FastAPI()
create_db_and_tables()


@app.post("/create", status_code=status.HTTP_201_CREATED)
async def create_doctor(doctor_info: Annotated[Doctor, Body()], session: SessionDep):

    # use the **doctor_info in the constructor of model for test if it's work or not
    doctor_for_db = DoctorDB(
        name=doctor_info.name,
        description=doctor_info.description,
        phone_number=doctor_info.phone_number,
        address=doctor_info.address,
    )

    session.add(doctor_for_db)
    session.commit()

    return doctor_for_db


@app.get("/doctors", status_code=status.HTTP_200_OK)
async def show_doctors(session: SessionDep):
    return session.exec(select(DoctorDB)).all()


@app.get("/doctors/{id:int}", response_model=DoctorDB)
async def get_doctor_by_id(id: Annotated[int, Path()], session: SessionDep) -> DoctorDB:
    doctor_from_db = session.exec(select(DoctorDB).where(DoctorDB.id == id)).first()

    if not doctor_from_db:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="کاربر پیدا نشد!")

    return doctor_from_db


@app.delete("/doctors/{id:int}/delete", status_code=status.HTTP_204_NO_CONTENT)
async def delete_doctor(id: Annotated[int, Path()], session: SessionDep) -> None:
    doctor_from_db = session.exec(select(DoctorDB).where(DoctorDB.id == id)).first()

    if not doctor_from_db:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, detail="آیتم پیدا نشد برای پاک کردن"
        )

    session.delete(doctor_from_db)
    session.commit()


@app.patch("/doctors/{id:int}/update")
async def update_doctor(
    id: Annotated[int, Path()],
    new_info: Annotated[DoctorUpdate, Body()],
    session: SessionDep,
):
    doctor_from_db = session.exec(select(DoctorDB).where(DoctorDB.id == id)).first()

    if not doctor_from_db:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, detail="آیتم پیدا نشد برای آپدیت "
        )

    doctor_from_db.sqlmodel_update(new_info.model_dump(exclude_unset=True))

    session.commit()
    session.refresh(doctor_from_db)

    return doctor_from_db

<<<<<<< HEAD


@app.post('/ask_ai')
async def ask_ai(
    text: Annotated[str, Body()],
    session: SessionDep
):

    doctors = session.exec(select(DoctorDB)).all()

    info_text = ""


    for doctor in doctors:
        info_text += f"{doctor.name}:{doctor.description}"

    client = OpenAI(
        # This is the default and can be omitted
        api_key="" # fix
    )

    response = client.responses.create(
        model="gpt-5.5",
        instructions="به عنوان مشاور برای اینکه کدوم دکتر برای این بیمار بهتره کاربر رو راهنمایی کن لحن صمیمی و دوستانه داشته همیشه به فارسی جواب بده",
        input=text + info_text,
    )

    return response.output_text


@app.post('/doctors/{id:int}/reserve')
async def reserve_doctor(
    id: Annotated[int, Path()],
    name: Annotated[str, Body()],
    start: Annotated[str, Body()],
    session: SessionDep
):

    doctor_from_db = session.get(DoctorDB, id)

    if not doctor_from_db:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail='دکتر وجود ندارد')


    for slot in doctor_from_db.schlude:
        if slot.start == start:
            if slot.is_reserved:
                raise HTTPException(status.HTTP_400_BAD_REQUEST, detail='این نوبت رزرو شده است')

            slot.is_reserved = True
            slot.reserved_by = name
            
            doctor_from_db.schlude = list(doctor_from_db.schlude)
            session.add(doctor_from_db)
            session.commit()
            session.refresh(doctor_from_db)
            return {'msg': 'successfully'}

        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail='اصلا این تایم در تایم کاری دکتر موجود نیست!')
=======
>>>>>>> b01273e1a0c7acbbb4b88c2585a798d07f525eeb
