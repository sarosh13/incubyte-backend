from datetime import date
from typing import Optional
from fastapi import FastAPI, Request, Response
from fastapi.responses import RedirectResponse
from app.database.db import DB
from app.models.error import NotFoundException
from app.models import AddDoctorRequest

from app.models.requests.add_appointment_request import AddAppointmentRequest
from app.models.requests.cancel_appointment_request import CancelAppointmentRequest
from app.services.availability_service import AvailabilityService
from app.services.doctor_service import DoctorService, InDatabaseDoctorService, InMemoryDoctorService
from app.settings import Settings


def create_app() -> FastAPI:
    doctor_service: DoctorService
    availability_service: AvailabilityService
    
    db: Optional[DB] = None
    if Settings.in_database:
        db = DB()
        db.init_if_needed()
        doctor_service = InDatabaseDoctorService(db=db)
        availability_service = AvailabilityService(db=db)
    else:
        doctor_service = InMemoryDoctorService()
        doctor_service.seed()

    app = FastAPI(swagger_ui_parameters={'tryItOutEnabled': True})

    @app.get('/doctors')
    def list_doctors():
        return doctor_service.list_doctors()

    @app.get('/doctors/{id}')
    async def get_doctor(id: int):
        return doctor_service.get_doctor(id)

    @app.post('/doctors')
    def add_doctor(request: AddDoctorRequest):

        id = doctor_service.add_doctor(
            first_name=request.first_name,
            last_name=request.last_name
        )

        return {
            'id': id
        }

    @app.get('/doctors/{doctor_id}/locations')
    def get_doctor_locations(doctor_id: int):
        return doctor_service.list_doctor_locations(doctor_id=doctor_id)
    

    # Add new endpoints here! #
    
    # Doctors Weekly Schedule (Monday - Sunday) 1 - Monday, 2 - Tuesday, etc.
    @app.get('/doctors/{doctor_id}/schedules')
    def list_doctor_schedules(doctor_id: int):
        return availability_service.list_doctor_schedules(doctor_id=doctor_id)
    
    # Doctors timeslots for a particular day
    @app.get('/doctors/{doctor_id}/timeslots')
    def list_doctor_timeslots(doctor_id: int, date: date):
        res = availability_service.list_doctor_timeslots(doctor_id, date)
        return res
    
    # Add/Book an appointment
    @app.post('/doctors/{doctor_id}/timeslots')
    def add_appointment(doctor_id: int, request: AddAppointmentRequest):
        res = availability_service.add_appointment(
            doctor_id=doctor_id,
            doctor_location_id=request.doctor_location_id,
            date=request.date,
            start_time=request.start_time
        )
        
        return res
    
    
    # Cancel Appointment
    @app.delete('/appointments')
    def cancel_appointment(doctor_id: int, request: CancelAppointmentRequest):
        res = availability_service.cancel_appointment(doctor_id, request.date, request.start_time)
        
        return res
        

    @app.exception_handler(NotFoundException)
    async def not_found(request: Request, exc: NotFoundException):
        return Response(status_code=404)

    @app.on_event('shutdown')
    def shutdown():
        if db:
            db.close_db()

    @app.get('/', include_in_schema=False)
    def root():
        return RedirectResponse('/docs')

    return app


app = create_app()
