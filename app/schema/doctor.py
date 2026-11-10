from pydantic import BaseModel, Field


class Doctor(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    description: str = Field(max_length=800)
    phone_number: str = Field(max_length=11)
    address: str = Field(min_length=1, max_length=800)




class DoctorUpdate(BaseModel):
    name: str | None = Field(min_length=1, max_length=100, default=None)
    description: str | None = Field(max_length=800, default=None)
    phone_number: str | None = Field(max_length=11, default=None)
    address: str | None = Field(min_length=1, max_length=800, default=None)