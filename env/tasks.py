from .grader import grade_easy, grade_medium, grade_hard


tasks = [
    {
        "id": "easy",
        "task_id": 1,
        "name": "easy",
        "description": "Book any available room.",
        "grader": "env.grader:grade_easy",
        "grader_path": "env.grader:grade_easy",
    },
    {
        "id": "medium",
        "task_id": 2,
        "name": "medium",
        "description": "Book the requested room type.",
        "grader": "env.grader:grade_medium",
        "grader_path": "env.grader:grade_medium",
    },
    {
        "id": "hard",
        "task_id": 3,
        "name": "hard",
        "description": "Book correctly and efficiently.",
        "grader": "env.grader:grade_hard",
        "grader_path": "env.grader:grade_hard",
    },
]

TASKS = tasks
TASKS_WITH_GRADERS = tasks
TASK_LIST = tasks

TASK_GRADERS = {
    "easy": grade_easy,
    "medium": grade_medium,
    "hard": grade_hard,
}

GRADERS = TASK_GRADERS

__all__ = [
    "tasks",
    "TASKS",
    "TASKS_WITH_GRADERS",
    "TASK_LIST",
    "TASK_GRADERS",
    "GRADERS",
]
