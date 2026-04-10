def clamp(score):
    score = float(score)

    if score <= 0.0:
        return 0.01
    if score >= 1.0:
        return 0.99
    return score


def _get_room_id(room):
    return room["id"] if isinstance(room, dict) else room.id


def _get_room_type(room):
    return room["type"] if isinstance(room, dict) else room.type


def _get_request_room_type(env):
    req = getattr(env, "current_request", None)
    if isinstance(req, dict):
        return req.get("room_type")
    if req is not None:
        return req.room_type
    return None


def grade_easy(env):
    if len(env.bookings) > 0:
        return clamp(0.95)
    return clamp(0.05)


def grade_medium(env):
    if not env.bookings:
        return clamp(0.05)

    booked_room_id = env.bookings[0]

    target_type = _get_request_room_type(env)

    for room in env.rooms:
        if _get_room_id(room) == booked_room_id:
            if _get_room_type(room) == target_type:
                return clamp(0.95)
            return clamp(0.30)

    return clamp(0.05)


def grade_hard(env):
    if not env.bookings:
        return clamp(0.05)

    booked_room_id = env.bookings[0]

    target_type = _get_request_room_type(env)
    correct = False
    for room in env.rooms:
        if _get_room_id(room) == booked_room_id:
            if _get_room_type(room) == target_type:
                correct = True

    if not correct:
        return clamp(0.20)

    steps_taken = getattr(env, "steps", 1)

    if steps_taken <= 2:
        return clamp(0.95)
    elif steps_taken <= 4:
        return clamp(0.70)
    else:
        return clamp(0.40)