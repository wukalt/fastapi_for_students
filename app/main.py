from fastapi import FastAPI, Body, status, Path, HTTPException
from typing import Annotated
from app.schema.doctor import Doctor, DoctorUpdate
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



@app.get('/doctors/{id:int}', response_model=DoctorDB)
async def get_doctor_by_id(
    id: Annotated[int, Path()],
    session: SessionDep
) -> DoctorDB:
    doctor_from_db = session.exec(select(DoctorDB).where(DoctorDB.id == id)).first()

    if not doctor_from_db:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail='کاربر پیدا نشد!')

    return doctor_from_db




@app.delete('/doctors/{id:int}/delete', status_code=status.HTTP_204_NO_CONTENT)
async def delete_doctor(
    id: Annotated[int, Path()],
    session: SessionDep
) -> None:
    doctor_from_db = session.exec(select(DoctorDB).where(DoctorDB.id == id)).first()

    if not doctor_from_db:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail='آیتم پیدا نشد برای پاک کردن')

    session.delete(doctor_from_db)
    session.commit()



@app.patch('/doctors/{id:int}/update')
async def update_doctor(
    id: Annotated[int, Path()],
    new_info: Annotated[DoctorUpdate, Body()],
    session: SessionDep
):
    doctor_from_db = session.exec(select(DoctorDB).where(DoctorDB.id == id)).first()
    
    if not doctor_from_db:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail='آیتم پیدا نشد برای آپدیت ')

    doctor_from_db.sqlmodel_update(new_info.model_dump(exclude_unset=True))

    session.commit()
    session.refresh(doctor_from_db)

    return doctor_from_db