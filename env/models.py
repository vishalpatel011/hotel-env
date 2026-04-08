from pydantic import BaseModel
from typing import List, Optional

class Room(BaseModel):
    id: int
    type: str
    bookings: List[dict]  # store date ranges

class BookingRequest(BaseModel):
    room_type: str
    check_in: int
    check_out: int

class Observation(BaseModel):
    rooms: List[Room]
    bookings: List[dict]
    request: BookingRequest

class Action(BaseModel):
    action: str # "check_availability" | "book_room" | "cancel_booking"

class Reward(BaseModel):
    value: float