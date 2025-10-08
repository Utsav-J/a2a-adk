from typing import Dict
from datetime import datetime, date, timedelta
COURT_SCHEDULE : Dict[str, Dict[str,str]] = {}
# eg.
# {
#     "2025-10-07": {
#         "08:00": "unknown",
#         "09:00": "Alice",
#         "10:00": "unknown"
#     }
# }

def generate_court_schedule():
    global COURT_SCHEDULE
    today = date.today()
    possible_times = [f"{h:02}:00" for h in range(8,21)] #:02 is a padding to always show two digits like 08 09
    for i in range(7):
        current_date = today + timedelta(days=i)
        date_str = current_date.strftime("%Y-%m-%d")
        COURT_SCHEDULE[date_str] = {time:"unknown" for time in possible_times}

generate_court_schedule()

def list_court_availabilities(date:str) -> Dict:
    try:
        datetime.strptime(date,"%Y-%m-%d")
    except ValueError:
        return {
            "status":"error",
            "message":"Invalid date format"
        }

    daily_schedule = COURT_SCHEDULE.get(date)
    if not daily_schedule:
        return {
            "status": "success",
            "message": f"The court is not open on {date}.",
            "schedule": {},
        }

    available_slots = [
        time for time, party in daily_schedule.items() if party == "unknown"
    ]
    booked_slots = {
        time:party for time,party in daily_schedule.items() if party != "unknown"
    }
    return {
        "status": "success",
        "message": f"Schedule for {date}.",
        "available_slots": available_slots,
        "booked_slots": booked_slots,
    }

def book_court(
    date:str, start_time:str, end_time:str, reservation_name:str
)->Dict:
    try:
        start_datetime = datetime.strptime(f"{date} {start_time}","%Y-%m-%d %H:%M")
        end_datetime = datetime.strptime(f"{date} {end_time}","%Y-%m-%d %H:%M")
    except ValueError:
        return {
            "status": "error",
            "message": "Invalid date or time format. Please use YYYY-MM-DD and HH:MM.",
        }
    if start_datetime > end_datetime:
        return {"status": "error", "message": "Start time must be before end time."}

    if date not in COURT_SCHEDULE:
        return {"status": "error", "message": f"The court is not open on {date}."}

    if not reservation_name:
        return {
            "status": "error",
            "message": "Cannot book a court without a reservation name.",
        }

    required_slots = []
    current_time = start_datetime
    while current_time < end_datetime:
        required_slots.append(current_time.strftime("%H:%M"))
        current_time += timedelta(hours=1)

    daily_schedule = COURT_SCHEDULE.get(date, {})
    for slot in required_slots:
        if daily_schedule.get(slot, "booked") != "unknown":
            party = daily_schedule.get(slot)
            return {
                "status": "error",
                "message": f"The time slot {slot} on {date} is already booked by {party}.",
            }
    for slot in required_slots:
        COURT_SCHEDULE[date][slot] = reservation_name

    return {
        "status": "success",
        "message": f"Success! The pickleball court has been booked for {reservation_name} from {start_time} to {end_time} on {date}.",
    }