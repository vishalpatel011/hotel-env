def normalize(score):
    # ensure strictly between (0,1)
    if score <= 0:
        return 0.01
    if score >= 1:
        return 0.99
    return score


def grade_easy(env):
    score = 1.0 if len(env.bookings) > 0 else 0.0
    return normalize(score)


def grade_medium(env):
    if not env.bookings:
        return 0.01

    booked_room_id = env.bookings[0]

    for room in env.rooms:
        if room.id == booked_room_id:
            score = 1.0 if room.type == env.current_request.room_type else 0.3
            return normalize(score)

    return 0.01


def grade_hard(env):
    if not env.bookings:
        return 0.01

    booked_room_id = env.bookings[0]

    correct = False
    for room in env.rooms:
        if room.id == booked_room_id:
            if room.type == env.current_request.room_type:
                correct = True

    if not correct:
        return 0.2

    steps_taken = getattr(env, "steps", 1)

    if steps_taken <= 2:
        score = 1.0
    elif steps_taken <= 4:
        score = 0.7
    else:
        score = 0.4

    return normalize(score)