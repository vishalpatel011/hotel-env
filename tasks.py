from grader import grade_easy, grade_medium, grade_hard


tasks = [
    {
        "id": "easy",
        "task_id": 1,
        "name": "easy",
        "description": "Book any available room",
        "grader": grade_easy,
        "grader_path": "grader:grade_easy",
    },
    {
        "id": "medium",
        "task_id": 2,
        "name": "medium",
        "description": "Book requested room type",
        "grader": grade_medium,
        "grader_path": "grader:grade_medium",
    },
    {
        "id": "hard",
        "task_id": 3,
        "name": "hard",
        "description": "Book correctly and efficiently",
        "grader": grade_hard,
        "grader_path": "grader:grade_hard",
    },
]

TASKS = tasks

TASK_GRADERS = {
    "easy": grade_easy,
    "medium": grade_medium,
    "hard": grade_hard,
}

__all__ = ["tasks", "TASKS", "TASK_GRADERS"]
