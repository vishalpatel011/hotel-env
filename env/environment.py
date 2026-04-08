import random
from env.models import Room, BookingRequest, Observation

class HotelEnv:
    def __init__(self):
        self.reset()

    def reset(self):
        self.rooms = [
            Room(id=101, type="single", available=True),
            Room(id=102, type="single", available=True),
            Room(id=201, type="double", available=True),
            Room(id=202, type="double", available=True),
            Room(id=301, type="suite", available=True),
        ]

        self.bookings = []

        self.current_request = BookingRequest(
            room_type=random.choice(["single", "double", "suite"]),
            days=random.randint(1, 5)
        )

        self.done = False

        return self.state()

    def state(self):
        return Observation(
            rooms=self.rooms,
            bookings=self.bookings,
            request=self.current_request
        )

    def step(self, action):
        action_type = action if isinstance(action, str) else action.action
        reward = 0.0

        if action_type == "check_availability":
            reward = 0.2

        elif action_type == "book_room":
            for room in self.rooms:
                if room.type == self.current_request.room_type and room.available:
                    room.available = False
                    self.bookings.append(room.id)
                    reward = 1.0
                    self.done = True
                    break
            else:
                reward = -0.5

        elif action_type == "cancel_booking":
            if self.bookings:
                room_id = self.bookings.pop()
                for room in self.rooms:
                    if room.id == room_id:
                        room.available = True
                reward = 0.5
            else:
                reward = -0.2

        else:
            reward = -0.1

        return self.state(), reward, self.done, {}