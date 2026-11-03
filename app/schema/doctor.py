from pydantic import BaseModel, Field


class Doctor(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    description: str = Field(max_length=800)
    phone_number: str = Field(max_length=11)
    address: str = Field(min_length=1, max_length=800)