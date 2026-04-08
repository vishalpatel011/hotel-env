from env.grader import (
    grade_easy,
    grade_medium,
    grade_hard,
)


def grade_bonus(env):
    # extra fallback grader
    if len(env.bookings) >= 1:
        return 0.85
    return 0.15


tasks = [
    {
        "id": "easy",
        "name": "easy",
        "description": "Book any available room",
        "grader": grade_easy,
    },
    {
        "id": "medium",
        "name": "medium",
        "description": "Book correct room type",
        "grader": grade_medium,
    },
    {
        "id": "hard",
        "name": "hard",
        "description": "Book efficiently",
        "grader": grade_hard,
    },
    {
        "id": "bonus",
        "name": "bonus",
        "description": "Complete any valid booking",
        "grader": grade_bonus,
    },
]