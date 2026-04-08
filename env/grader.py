def grade_easy(env):
    return 1.0 if len(env.bookings) > 0 else 0.0


def grade_medium(env):
    if not env.bookings:
        return 0.0

    booked_room_id = env.bookings[0]

    for room in env.rooms:
        if room.id == booked_room_id:
            return 1.0 if room.type == env.current_request.room_type else 0.3

    return 0.0


def grade_hard(env, steps_taken=1):
    if not env.bookings:
        return 0.0

    booked_room_id = env.bookings[0]

    correct = False
    for room in env.rooms:
        if room.id == booked_room_id:
            if room.type == env.current_request.room_type:
                correct = True

    if not correct:
        return 0.2

    if steps_taken <= 2:
        return 1.0
    elif steps_taken <= 4:
        return 0.7
    else:
        return 0.4