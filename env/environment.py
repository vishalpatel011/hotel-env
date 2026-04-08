import random
from env.models import Room, BookingRequest, Observation


class HotelEnv:
    def __init__(self):
        self.reset()

    def reset(self):
        self.rooms = [
            Room(id=101, type="single", bookings=[]),
            Room(id=102, type="single", bookings=[]),
            Room(id=201, type="double", bookings=[]),
            Room(id=202, type="double", bookings=[]),
            Room(id=301, type="suite", bookings=[]),
        ]

        self.bookings = []

        check_in = random.randint(1, 10)
        check_out = check_in + random.randint(1, 5)

        self.current_request = BookingRequest(
            room_type=random.choice(["single", "double", "suite"]),
            check_in=check_in,
            check_out=check_out
        )

        self.done = False
        self.steps = 0

        return self.state()

    def state(self):
        return Observation(
            rooms=self.rooms,
            bookings=self.bookings,
            request=self.current_request
        )

    def is_available(self, room, check_in, check_out):
        for b in room.bookings:
            if not (check_out <= b["check_in"] or check_in >= b["check_out"]):
                return False
        return True

    def step(self, action):
        action_type = action if isinstance(action, str) else action.action
        reward = 0.0
        self.steps += 1

        if action_type == "check_availability":
            reward = 0.1

        elif action_type == "book_room":
            for room in self.rooms:
                if room.type == self.current_request.room_type:
                    if self.is_available(room, self.current_request.check_in, self.current_request.check_out):

                        booking = {
                            "room_id": room.id,
                            "check_in": self.current_request.check_in,
                            "check_out": self.current_request.check_out
                        }

                        room.bookings.append(booking)
                        self.bookings.append(booking)

                        reward = 1.0
                        self.done = True
                        break
            else:
                reward = -0.7

        elif action_type == "cancel_booking":
            if self.bookings:
                self.bookings.pop()
                reward = 0.3
            else:
                reward = -0.2

        else:
            reward = -0.1

        return self.state(), reward, self.done, {}