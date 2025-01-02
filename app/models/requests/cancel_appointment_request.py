from datetime import datetime, date
import re

# from attr import validate
from pydantic import BaseModel, field_validator, root_validator, validator


class CancelAppointmentRequest(BaseModel):
    date: date
    start_time: str
    
    @field_validator("start_time")
    def validate_start_time(cls, value):
        # Check if the value matches the 'HH:mm' format using regex
        if not re.match(r'^\d{2}:\d{2}$', value):
            raise ValueError("start_time must be in 'HH:mm' format.")
        try:
            # Check if the value is in 'hh:mm' format
            datetime.strptime(value, '%H:%M')
            return value
        except ValueError:
            raise ValueError("start_time must be in 'hh:mm' format.")
        
    
    