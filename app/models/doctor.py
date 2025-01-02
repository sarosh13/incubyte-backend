from pydantic import BaseModel


class Doctor(BaseModel):
    id: int
    first_name: str
    last_name: str


class Location(BaseModel):
    id: int
    address: str


class DoctorLocation(BaseModel):
    """
    This indicates that a doctor works at a location. Locations can have
    multiple doctors, and doctors can have multiple locations
    """
    id: int
    doctor_id: int
    location_id: int
    

class DoctorAvailability(BaseModel):
    id: int
    doctor_id: int
    date: str
    start_time: str
    end_time: str
    is_booked: int
    