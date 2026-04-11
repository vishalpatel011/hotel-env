from env.environment import HotelEnv


def _run_task(actions: list[str]) -> float:
    env = HotelEnv()
    env.reset()
    total_reward = 0.0
    for action in actions:
        _, reward, done, _ = env.step(action)
        total_reward += float(reward or 0.0)
        if done:
            break
    raw = (total_reward + 2.0) / 4.0
    return max(0.01, min(0.99, round(raw, 3)))


def grade_easy(trajectory=None) -> float:
    """Easy: check availability then book a double room."""
    return _run_task(["check_availability", "book_room 201"])


def grade_medium(trajectory=None) -> float:
    """Medium: book, cancel, then rebook."""
    return _run_task(["check_availability", "book_room 201",
                      "cancel_booking", "book_room 202"])


def grade_hard(trajectory=None) -> float:
    """Hard: direct book without availability check."""
    return _run_task(["book_room 201"])