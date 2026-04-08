def grade_easy(env):
    # Any booking is success
    if len(env.bookings) > 0:
        return 1.0
    return 0.0


def grade_medium(env):
    # Correct room type booking
    if not env.bookings:
        return 0.0

    booked_room_id = env.bookings[0]

    for room in env.rooms:
        if room.id == booked_room_id:
            if room.type == env.current_request.room_type:
                return 1.0
            else:
                return 0.3  # wrong type but still booked

    return 0.0


def grade_hard(env, steps_taken):
    # Smart behavior + correct booking

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

    # Penalize too many steps
    if steps_taken <= 2:
        return 1.0
    elif steps_taken <= 4:
        return 0.7
    else:
        return 0.4