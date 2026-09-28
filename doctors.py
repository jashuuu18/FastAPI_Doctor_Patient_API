
from typing import Optional

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query
)

from sqlalchemy.orm import Session

from app.database import get_db

from app.models import Doctor, Patient

from app.schemas import (
    DoctorCreate,
    DoctorUpdate,
    DoctorPatch,
    DoctorResponse,
    PatientResponse
)

from app.auth.auth import (
    get_current_user,
    admin_required
)


router = APIRouter(
    prefix="/api/v1/doctors",
    tags=["Doctors"]
)


# =========================
# CREATE
# =========================

@router.post(
    "",
    response_model=DoctorResponse,
    status_code=201
)
def create_doctor(
    doctor_data: DoctorCreate,
    db: Session = Depends(get_db),
    current_user=Depends(admin_required)
):

    existing = db.query(Doctor).filter(
        Doctor.email == doctor_data.email
    ).first()

    if existing:

        raise HTTPException(
            status_code=400,
            detail="Doctor email already exists"
        )

    doctor = Doctor(
        name=doctor_data.name,
        email=doctor_data.email,
        specialization=doctor_data.specialization,
        phone=doctor_data.phone,
        is_active=True
    )

    db.add(doctor)

    db.commit()

    db.refresh(doctor)

    return doctor


# =========================
# LIST + FILTER + PAGINATION
# =========================

@router.get("")
def get_doctors(

    specialization: Optional[str] = None,

    is_active: Optional[bool] = None,

    page: int = Query(
        1,
        ge=1
    ),

    limit: int = Query(
        10,
        ge=1,
        le=100
    ),

    db: Session = Depends(get_db),

    current_user=Depends(get_current_user)
):

    query = db.query(Doctor)

    if specialization:

        query = query.filter(
            Doctor.specialization == specialization
        )

    if is_active is not None:

        query = query.filter(
            Doctor.is_active == is_active
        )

    total = query.count()

    offset = (page - 1) * limit

    doctors = query.offset(
        offset
    ).limit(
        limit
    ).all()

    return {
        "total": total,
        "page": page,
        "limit": limit,
        "data": doctors
    }


# =========================
# GET ONE
# =========================

@router.get(
    "/{doctor_id}",
    response_model=DoctorResponse
)
def get_doctor(

    doctor_id: int,

    db: Session = Depends(get_db),

    current_user=Depends(get_current_user)

):

    doctor = db.query(Doctor).filter(
        Doctor.id == doctor_id
    ).first()

    if not doctor:

        raise HTTPException(
            status_code=404,
            detail="Doctor not found"
        )

    return doctor


# =========================
# PUT
# =========================

@router.put(
    "/{doctor_id}",
    response_model=DoctorResponse
)
def update_doctor(

    doctor_id: int,

    doctor_data: DoctorUpdate,

    db: Session = Depends(get_db),

    current_user=Depends(admin_required)

):

    doctor = db.query(Doctor).filter(
        Doctor.id == doctor_id
    ).first()

    if not doctor:

        raise HTTPException(
            status_code=404,
            detail="Doctor not found"
        )

    duplicate = db.query(Doctor).filter(
        Doctor.email == doctor_data.email,
        Doctor.id != doctor_id
    ).first()

    if duplicate:

        raise HTTPException(
            status_code=400,
            detail="Doctor email already exists"
        )

    doctor.name = doctor_data.name
    doctor.email = doctor_data.email
    doctor.specialization = doctor_data.specialization
    doctor.phone = doctor_data.phone
    doctor.is_active = doctor_data.is_active

    db.commit()

    db.refresh(doctor)

    return doctor


# =========================
# PATCH
# =========================

@router.patch(
    "/{doctor_id}",
    response_model=DoctorResponse
)
def patch_doctor(

    doctor_id: int,

    doctor_data: DoctorPatch,

    db: Session = Depends(get_db),

    current_user=Depends(admin_required)

):

    doctor = db.query(Doctor).filter(
        Doctor.id == doctor_id
    ).first()

    if not doctor:

        raise HTTPException(
            status_code=404,
            detail="Doctor not found"
        )

    update_data = doctor_data.model_dump(
        exclude_unset=True
    )

    if "email" in update_data:

        duplicate = db.query(Doctor).filter(
            Doctor.email == update_data["email"],
            Doctor.id != doctor_id
        ).first()

        if duplicate:

            raise HTTPException(
                status_code=400,
                detail="Doctor email already exists"
            )

    for key, value in update_data.items():

        setattr(
            doctor,
            key,
            value
        )

    db.commit()

    db.refresh(doctor)

    return doctor


# =========================
# SOFT DELETE
# =========================

@router.delete(
    "/{doctor_id}"
)
def delete_doctor(

    doctor_id: int,

    db: Session = Depends(get_db),

    current_user=Depends(admin_required)

):

    doctor = db.query(Doctor).filter(
        Doctor.id == doctor_id
    ).first()

    if not doctor:

        raise HTTPException(
            status_code=404,
            detail="Doctor not found"
        )

    doctor.is_active = False

    db.commit()

    return {
        "message": "Doctor soft deleted successfully"
    }


# =========================
# GET DOCTOR PATIENTS
# =========================

@router.get(
    "/{doctor_id}/patients",
    response_model=list[PatientResponse]
)
def get_doctor_patients(

    doctor_id: int,

    db: Session = Depends(get_db),

    current_user=Depends(get_current_user)

):

    doctor = db.query(Doctor).filter(
        Doctor.id == doctor_id
    ).first()

    if not doctor:

        raise HTTPException(
            status_code=404,
            detail="Doctor not found"
        )

    if not doctor.is_active:

        raise HTTPException(
            status_code=400,
            detail="Doctor is inactive"
        )

    return doctor.patients

@router.patch("/{doctor_id}", response_model=DoctorResponse)
def patch_doctor(
    doctor_id: int,
    doctor_data: DoctorPatch,
    db: Session = Depends(get_db),
    current_user=Depends(admin_required)
):
    doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()

    if not doctor:
        raise HTTPException(
            status_code=404,
            detail="Doctor not found"
        )

    update_data = doctor_data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(doctor, key, value)

    db.commit()
    db.refresh(doctor)

    return doctor
