from datetime import date, timedelta, datetime
from pydoc import doc
from tracemalloc import start
from app.database.db import DB
from app.models import DoctorAvailability, doctor

class AvailabilityService:
    """
    This is left up to you to implement, generally following the patterns in the repo.

    That said, *don't* feel obliged to make an abstract base class/interface for your chosen approach - you
    can simply write the service using either the database or in-memory approach from the beginning.
    We used that pattern for the doctor_service to have examples for both modes.
    """
    
    def __init__(self, db: DB):
        self.db = db
        
        
    # List all weekly schedules of doctor
    def list_doctor_schedules(self, doctor_id: int):
        dict_result = self.db.execute(
            'SELECT ds.id, ds.doctor_id,ds.day_of_week,ds.start_time,ds.end_time FROM doctor_schedules ds '
            'INNER JOIN doctors d ON ds.doctor_id = d.id '
            'WHERE ds.doctor_id = ?',
            [doctor_id]
        )
        
        return [
            res for res in dict_result
        ]
        
        
    # List all appointments of doctor
    def list_appointments(self, doctor_id: int):
        dict_result = self.db.execute(
            'SELECT * FROM appointments '
            'WHERE doctor_id = ?',
            [doctor_id]
        )
        
        return [res for res in dict_result]
    
    
    # List doctor timeslots for a particular date
    def list_doctor_timeslots(self, doctor_id: int, date: date):
        
        schedule = self.db.execute(
            'SELECT * FROM doctor_schedules '
            'WHERE doctor_id = ? AND day_of_week = strftime("%w", ?)',
            [doctor_id, date]
        )
        
        appointments = self.db.execute(
            'SELECT * FROM appointments '
            'WHERE doctor_id = ? AND date = ? AND is_booked = ?',
            [doctor_id, date, 1]
        )
        
        # fetch booked appointments slots into a list
        booked_slots = {(appt['start_time'], appt['end_time']) for appt in appointments}

        slots = [] # append all the timeslots
        
        for sched in schedule:
            # start_time and end_time are converted from strings to datetime objects
            start_time = datetime.strptime(sched['start_time'], '%H:%M')
            end_time = datetime.strptime(sched['end_time'], '%H:%M')

            # iterate through the time range (start_time to end_time) in 1-hour intervals:
            while start_time < end_time:
                slot_start = start_time.strftime('%H:%M')
                slot_end = (start_time + timedelta(hours=1)).strftime('%H:%M')
                
                # Check if the slot is booked
                is_booked = (slot_start, slot_end) in booked_slots
                
                slots.append({
                    "start_time": slot_start,
                    "end_time": slot_end,
                    "is_booked": True if is_booked else False
                })

                start_time += timedelta(hours=1)

        return slots
    
      
    # Book/Add an appointment  
    def add_appointment(self, doctor_id: int, doctor_location_id: int, date: str, start_time: str):

        timeslots = self.list_doctor_timeslots(doctor_id,date)
        
        for slot in timeslots:
            if slot['start_time'] == start_time:
                if slot['is_booked'] == True:
                    return {
                        "status": "error",
                        "message": "The requested time slot is already booked."
                    }
                    
                else:
                    # calculate end time
                    start_time_obj = datetime.strptime(start_time, '%H:%M')
                    end_time_obj = start_time_obj + timedelta(hours=1)
                    end_time = end_time_obj.strftime('%H:%M')
                    
                    self.db.execute(
                        'INSERT INTO appointments (doctor_id, doctor_location_id, date, start_time, end_time) '
                        'VALUES (?, ?, ?, ?, ?)',
                        [doctor_id, doctor_location_id, date, start_time, end_time]
                    ) 
                    
                    return {
                        "status":"success",
                        "message":"Appointment successfully booked."
                    }
        else:
            return {
                "status": "error",
                "message": "The requested time slot is not on the schedule."
            }
            
    def cancel_appointment(self, doctor_id: int, date: date, start_time: str):
        
        appointment = self.db.execute(
            'SELECT * FROM appointments '
            'WHERE doctor_id = ? AND date = ? AND start_time = ? AND is_booked = 1',
            [doctor_id, date, start_time]
            )
            
        if not appointment:
            return {
                "status": "error",
                "message": "No active appointment found for the specified details."
            }
        
        # Cancel the appointment
        self.db.execute(
            'UPDATE appointments SET is_booked = 0 '
            'WHERE doctor_id = ? AND date = ? AND start_time = ?',
            [doctor_id, date, start_time]
        )
        
        return {
            "status": "success",
            "message": "Appointment cancelled."
        }
            

