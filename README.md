# Doctor & Patient Management API

A REST API built using **Python, FastAPI, SQLAlchemy, SQLite, and JWT Authentication** for managing doctors and patients.

## Technologies

- Python 3.9+
- FastAPI
- SQLAlchemy
- SQLite
- Pydantic
- JWT Authentication
- Uvicorn
- Pytest
- Docker

## Features

### Authentication
- User registration and login
- JWT-based authentication
- Protected API endpoints
- Role-based authorization

### Doctors
- Create doctor
- Get doctors
- Get doctor by ID
- Update doctor using PUT
- Partial update using PATCH
- Soft delete doctor
- Activate/deactivate doctor
- Assign patients
- Get doctor's patients

### Patients
- Create patient
- Get patients
- Get patient by ID
- Update patient using PUT
- Partial update using PATCH
- Delete patient
- Assign patient to a doctor

### Validation
- Unique doctor email
- Phone number must contain exactly 10 digits
- Patient age validation
- Doctor must exist and be active before assigning a patient

### Filtering
- Filter doctors by specialization
- Filter doctors by active status
- Filter patients by age

### Pagination
Supports:
- `page`
- `limit`
- `total`
- `data`

Example:

`GET /api/v1/doctors?page=1&limit=10`

## API Versioning

All main APIs use:

`/api/v1/`

Examples:

- `/api/v1/auth/login`
- `/api/v1/doctors`
- `/api/v1/patients`

## Database

The project uses **SQLite** with **SQLAlchemy ORM**.

Database file:

`doctor_patient.db`

## Authentication Testing

1. Register a user.
2. Login and copy the `access_token`.
3. Click **Authorize** in Swagger.
4. Enter:

`Bearer <access_token>`

5. Test the protected APIs.

### 401 Unauthorized

If you receive:

`401 Unauthorized`

check that:
- You are logged in.
- The JWT token is valid.
- The token has not expired.
- Swagger is authorized with the Bearer token.

## Testing

Swagger documentation:

`http://127.0.0.1:8000/docs`

## Project Structure

```text
fastapi/
│
├── routes/
│   ├── __init__.py
│   ├── auth.py
│   ├── doctors.py
│   └── patients.py
│
├── auth.py
├── database.py
├── main.py
├── models.py
├── schemas.py
├── services.py
├── requirements.txt
├── .gitignore
└── README.md
