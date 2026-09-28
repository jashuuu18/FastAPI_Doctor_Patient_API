
from pydantic import BaseModel, EmailStr, Field
from typing import Optional


# =========================
# Authentication Schemas
# =========================

class RegisterRequest(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: str = "doctor"


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str


# =========================
# Doctor Schemas
# =========================

class DoctorCreate(BaseModel):
    name: str
    email: EmailStr
    specialization: str
    phone: str = Field(pattern=r"^\d{10}$")


class DoctorUpdate(BaseModel):
    name: str
    email: EmailStr
    specialization: str
    phone: str = Field(pattern=r"^\d{10}$")


class DoctorPatch(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    specialization: Optional[str] = None
    phone: Optional[str] = Field(
        default=None,
        pattern=r"^\d{10}$"
    )
    is_active: Optional[bool] = None


class DoctorResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    specialization: str
    phone: str
    is_active: bool

    class Config:
        from_attributes = True


# =========================
# Patient Schemas
# =========================

class PatientCreate(BaseModel):
    name: str
    age: int = Field(gt=0)
    phone: str = Field(pattern=r"^\d{10}$")
    doctor_id: int


class PatientUpdate(BaseModel):
    name: str
    age: int = Field(gt=0)
    phone: str = Field(pattern=r"^\d{10}$")
    doctor_id: int


class PatientPatch(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = Field(default=None, gt=0)
    phone: Optional[str] = Field(
        default=None,
        pattern=r"^\d{10}$"
    )
    doctor_id: Optional[int] = None


class PatientResponse(BaseModel):
    id: int
    name: str
    age: int
    phone: str
    doctor_id: int

    class Config:
        from_attributes = True