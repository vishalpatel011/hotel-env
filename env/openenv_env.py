try:
    from openenv import Env
except Exception:
    # Keep FastAPI runtime bootable even when openenv doesn't expose Env.
    class Env:  # type: ignore[no-redef]
        pass


class HotelEnvOpen(Env):
    def __init__(self):
        self.rooms = []
        self.bookings = []
        self.current_request = {}
        self.done = False
        self.steps = 0

    def reset(self):
        self.steps = 0
        self.done = False

        self.rooms = [
            {"id": 101, "type": "single", "bookings": []},
            {"id": 102, "type": "single", "bookings": []},
            {"id": 201, "type": "double", "bookings": []},
            {"id": 202, "type": "double", "bookings": []},
            {"id": 301, "type": "suite", "bookings": []},
        ]
        self.current_request = {"room_type": "double", "check_in": 10, "check_out": 12}
        self.bookings = []

        return {
            "rooms": self.rooms,
            "bookings": self.bookings,
            "request": self.current_request,
        }

    def _is_conflict(self, existing, new_check_in, new_check_out):
        return not (
            new_check_out <= existing.get("check_in")
            or new_check_in >= existing.get("check_out")
        )

    def step(self, action):
        self.steps += 1

        if self.done:
            return self._state(), 0.0, True, {}

        action = (action or "").strip().lower()

        if action == "check_availability":
            return self._state(), 0.1, False, {}

        if action.startswith("book_room"):
            parts = action.split()
            target_room_id = None
            if len(parts) > 1 and parts[1].isdigit():
                target_room_id = int(parts[1])

            if target_room_id is None:
                for room in self.rooms:
                    if room["type"] == self.current_request["room_type"]:
                        target_room_id = room["id"]
                        break

            for room in self.rooms:
                if room["id"] != target_room_id:
                    continue

                has_conflict = False
                for booking in room.get("bookings", []):
                    if self._is_conflict(
                        booking,
                        self.current_request["check_in"],
                        self.current_request["check_out"],
                    ):
                        has_conflict = True
                        break

                if has_conflict:
                    return self._state(), -0.5, False, {}

                room["bookings"].append(
                    {
                        "room_id": room["id"],
                        "check_in": self.current_request["check_in"],
                        "check_out": self.current_request["check_out"],
                    }
                )
                self.bookings.append(room["id"])
                self.done = True
                return self._state(), 1.0, True, {}

            return self._state(), -0.5, False, {}

        if action.startswith("cancel_booking"):
            if not self.bookings:
                return self._state(), -0.1, False, {}

            room_id = self.bookings.pop()
            for room in self.rooms:
                if room["id"] == room_id and room["bookings"]:
                    room["bookings"].pop()
                    break
            return self._state(), 0.2, False, {}

        return self._state(), -0.1, False, {}

    def _state(self):
        return {
            "rooms": self.rooms,
            "bookings": self.bookings,
            "request": self.current_request,
        }
