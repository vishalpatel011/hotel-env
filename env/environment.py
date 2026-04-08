from typing import List
from env.models import Room, BookingRequest, Observation


class HotelEnv:
    def __init__(self):
        self.rooms: List[Room] = []
        self.bookings = []
        self.current_request: BookingRequest = None
        self.done = False
        self.steps = 0

    def reset(self):
        self.steps = 0

        # Initialize hotel rooms
        self.rooms = [
            Room(id=101, type="single", bookings=[]),
            Room(id=102, type="single", bookings=[]),
            Room(id=201, type="double", bookings=[]),
            Room(id=202, type="double", bookings=[]),
            Room(id=301, type="suite", bookings=[]),
        ]

        # Customer booking request
        self.current_request = BookingRequest(
            room_type="double",
            check_in=10,
            check_out=12
        )

        self.bookings = []
        self.done = False

        return self.get_state()

    def get_state(self):
        return Observation(
            rooms=self.rooms,
            bookings=self.bookings,
            request=self.current_request
        )

    # Check date overlap
    def is_conflict(self, existing, new_check_in, new_check_out):
        return not (
            new_check_out <= existing.get("check_in")
            or new_check_in >= existing.get("check_out")
        )

    def step(self, action: str):
        self.steps += 1

        # Episode already finished
        if self.done:
            return self.get_state(), 0.0, True, {}

        # ---------------------------------------------------
        # CHECK AVAILABILITY
        # ---------------------------------------------------
        if action == "check_availability":
            return self.get_state(), 0.1, False, {}

        # ---------------------------------------------------
        # BOOK ROOM
        # Supports:
        # "book_room"
        # "book_room 201"
        # ---------------------------------------------------
        elif action.startswith("book_room"):
            parts = action.split()
            target_room_id = None

            # Optional explicit room id
            if len(parts) > 1 and parts[1].isdigit():
                target_room_id = int(parts[1])

            # Auto-select matching room if validator sends plain book_room
            if target_room_id is None:
                for room in self.rooms:
                    if room.type == self.current_request.room_type:
                        target_room_id = room.id
                        break

            # Attempt booking
            for room in self.rooms:
                if room.id == target_room_id:
                    conflict = False

                    for booking in (room.bookings or []):
                        if self.is_conflict(
                            booking,
                            self.current_request.check_in,
                            self.current_request.check_out
                        ):
                            conflict = True
                            break

                    if not conflict:
                        room.bookings.append({
                            "room_id": room.id,
                            "check_in": self.current_request.check_in,
                            "check_out": self.current_request.check_out
                        })

                        self.bookings.append(room.id)
                        self.done = True

                        return self.get_state(), 1.0, True, {}

            # Booking failed
            return self.get_state(), -0.5, False, {}

        # ---------------------------------------------------
        # CANCEL BOOKING
        # ---------------------------------------------------
        elif action.startswith("cancel_booking"):
            if not self.bookings:
                return self.get_state(), -0.1, False, {}

            last_room_id = self.bookings.pop()

            for room in self.rooms:
                if room.id == last_room_id and room.bookings:
                    room.bookings.pop()
                    return self.get_state(), 0.2, False, {}

            return self.get_state(), -0.1, False, {}

        # ---------------------------------------------------
        # INVALID ACTION
        # ---------------------------------------------------
        return self.get_state(), -0.1, False, {}