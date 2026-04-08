from env.grader import grade_easy, grade_medium, grade_hard


tasks = [
    {
        "name": "easy",
        "grader": lambda env: float(grade_easy(env)),
    },
    {
        "name": "medium",
        "grader": lambda env: float(grade_medium(env)),
    },
    {
        "name": "hard",
        "grader": lambda env: float(grade_hard(env)),
    },
]