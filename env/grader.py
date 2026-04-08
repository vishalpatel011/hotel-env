def clamp(score):
    score = float(score)

    if score <= 0.0:
        return 0.01
    if score >= 1.0:
        return 0.99
    return score


def grade_easy(env):
    if len(env.bookings) > 0:
        return clamp(0.95)
    return clamp(0.05)


def grade_medium(env):
    if not env.bookings:
        return clamp(0.05)

    booked_room_id = env.bookings[0]

    for room in env.rooms:
        if room.id == booked_room_id:
            if room.type == env.current_request.room_type:
                return clamp(0.95)
            return clamp(0.30)

    return clamp(0.05)


def grade_hard(env):
    if not env.bookings:
        return clamp(0.05)

    booked_room_id = env.bookings[0]

    correct = False
    for room in env.rooms:
        if room.id == booked_room_id:
            if room.type == env.current_request.room_type:
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