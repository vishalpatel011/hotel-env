from pydantic import BaseModel
from typing import List


class Room(BaseModel):
    id: int
    type: str
    bookings: List[dict]


class BookingRequest(BaseModel):
    room_type: str
    check_in: int
    check_out: int


class Observation(BaseModel):
    rooms: List[Room]
    bookings: List[int]   # ✅ FIXED (important)
    request: BookingRequest


class Action(BaseModel):
    action: str


class Reward(BaseModel):
    value: float