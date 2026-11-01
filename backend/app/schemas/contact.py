from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class ContactMessageCreate(BaseModel):
    visitor_name: str = Field(min_length=2, max_length=150)
    email: EmailStr
    subject: str | None = Field(default=None, max_length=200)
    message: str = Field(min_length=10)


class ContactMessageCreatedResponse(BaseModel):
    message: str