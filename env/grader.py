def safe_score(x):
    x = float(x)
    if x <= 0:
        return 0.1
    if x >= 1:
        return 0.9
    return x


def grade_easy(env=None):
    try:
        if hasattr(env, "bookings") and len(env.bookings) > 0:
            return safe_score(0.8)
        return safe_score(0.2)
    except Exception:
        return safe_score(0.2)


def grade_medium(env=None):
    try:
        if hasattr(env, "bookings") and len(env.bookings) > 0:
            return safe_score(0.7)
        return safe_score(0.3)
    except Exception:
        return safe_score(0.3)


def grade_hard(env=None):
    try:
        steps = getattr(env, "steps", 3)

        if steps <= 2:
            return safe_score(0.9)
        if steps <= 4:
            return safe_score(0.6)
        return safe_score(0.4)
    except Exception:
        return safe_score(0.5)