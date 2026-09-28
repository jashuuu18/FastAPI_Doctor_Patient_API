

from typing import Optional

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query
)

from sqlalchemy.orm import Session

from app.database import get_db

from app.models import Patient, Doctor

from app.schemas import (
    PatientCreate,
    PatientUpdate,
    PatientPatch,
    PatientResponse
)

from app.auth.auth import (
    get_current_user,
    admin_required
)


router = APIRouter(
    prefix="/api/v1/patients",
    tags=["Patients"]
)


# =========================
# CREATE PATIENT
# =========================

@router.post(
    "",
    response_model=PatientResponse,
    status_code=201
)
def create_patient(

    patient_data: PatientCreate,

    db: Session = Depends(get_db),

    current_user=Depends(admin_required)

):

    doctor = db.query(Doctor).filter(
        Doctor.id == patient_data.doctor_id
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

    patient = Patient(

        name=patient_data.name,

        age=patient_data.age,

        phone=patient_data.phone,

        doctor_id=patient_data.doctor_id
    )

    db.add(patient)

    db.commit()

    db.refresh(patient)

    return patient


# =========================
# LIST PATIENTS
# FILTER + PAGINATION
# =========================

@router.get("")
def get_patients(

    age_gt: Optional[int] = Query(
        None,
        gt=0
    ),

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

    query = db.query(Patient)

    if age_gt is not None:

        query = query.filter(
            Patient.age > age_gt
        )

    total = query.count()

    offset = (page - 1) * limit

    patients = query.offset(
        offset
    ).limit(
        limit
    ).all()

    return {
        "total": total,
        "page": page,
        "limit": limit,
        "data": patients
    }


# =========================
# GET PATIENT
# =========================

@router.get(
    "/{patient_id}",
    response_model=PatientResponse
)
def get_patient(

    patient_id: int,

    db: Session = Depends(get_db),

    current_user=Depends(get_current_user)

):

    patient = db.query(Patient).filter(
        Patient.id == patient_id
    ).first()

    if not patient:

        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )

    return patient


# =========================
# PUT PATIENT
# =========================

@router.put(
    "/{patient_id}",
    response_model=PatientResponse
)
def update_patient(

    patient_id: int,

    patient_data: PatientUpdate,

    db: Session = Depends(get_db),

    current_user=Depends(admin_required)

):

    patient = db.query(Patient).filter(
        Patient.id == patient_id
    ).first()

    if not patient:

        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )

    doctor = db.query(Doctor).filter(
        Doctor.id == patient_data.doctor_id
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

    patient.name = patient_data.name
    patient.age = patient_data.age
    patient.phone = patient_data.phone
    patient.doctor_id = patient_data.doctor_id

    db.commit()

    db.refresh(patient)

    return patient


# =========================
# PATCH PATIENT
# =========================

@router.patch(
    "/{patient_id}",
    response_model=PatientResponse
)
def patch_patient(

    patient_id: int,

    patient_data: PatientPatch,

    db: Session = Depends(get_db),

    current_user=Depends(admin_required)

):

    patient = db.query(Patient).filter(
        Patient.id == patient_id
    ).first()

    if not patient:

        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )

    update_data = patient_data.model_dump(
        exclude_unset=True
    )

    if "doctor_id" in update_data:

        doctor = db.query(Doctor).filter(
            Doctor.id == update_data["doctor_id"]
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

    for key, value in update_data.items():

        setattr(
            patient,
            key,
            value
        )

    db.commit()

    db.refresh(patient)

    return patient


# =========================
# DELETE PATIENT
# =========================

@router.delete(
    "/{patient_id}"
)
def delete_patient(

    patient_id: int,

    db: Session = Depends(get_db),

    current_user=Depends(admin_required)

):

    patient = db.query(Patient).filter(
        Patient.id == patient_id
    ).first()

    if not patient:

        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )

    db.delete(patient)

    db.commit()

    return {
        "message": "Patient deleted successfully"
    }
