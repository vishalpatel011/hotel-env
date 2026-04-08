def grade_easy(env):
    # Any booking success
    return 1.0 if len(env.bookings) > 0 else 0.0


def grade_medium(env):
    if not env.bookings:
        return 0.0

    booking = env.bookings[0]

    for room in env.rooms:
        if room.id == booking["room_id"]:
            if room.type == env.current_request.room_type:
                return 1.0
            else:
                return 0.3

    return 0.0


def grade_hard(env):
    if not env.bookings:
        return 0.0

    booking = env.bookings[0]

    # Check correct room type
    correct_type = False
    for room in env.rooms:
        if room.id == booking["room_id"]:
            if room.type == env.current_request.room_type:
                correct_type = True

    if not correct_type:
        return 0.2

    # Check date validity
    correct_dates = (
        booking["check_in"] >= env.current_request.check_in and
        booking["check_out"] <= env.current_request.check_out
    )

    if not correct_dates:
        return 0.5

    #  Efficiency (steps)
    if env.steps <= 2:
        return 1.0
    elif env.steps <= 4:
        return 0.7
    else:
        return 0.4