from fastapi import FastAPI, Body
from typing import Annotated
from app.schema.doctor import Doctor
from app.dependencies import SessionDep

app = FastAPI()



@app.post('/create')
async def create_doctor(
    doctor_info: Annotated[Doctor, Body()],
    session: SessionDep
):
    