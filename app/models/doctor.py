from sqlmodel import SQLModel, Field
from pydantic import BaseModel
from sqlalchemy import JSON


class TimeSlot(BaseModel):
    start: str
    end: str
    reserved_by: str 
    is_reserved: bool


class Doctor(SQLModel, table=True):
    id: int | None = Field(primary_key=True, index=True)
    name: str = Field(min_length=1, max_length=100)
    description: str = Field(max_length=800)
    phone_number: str = Field(max_length=11)
    address: str = Field(min_length=1, max_length=800)

    schlude: list[TimeSlot] = Field(
        default_factory=list,
        sa_type=JSON
    )