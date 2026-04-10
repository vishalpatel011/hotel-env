tasks = [
    {
        "id": "easy",
        "name": "easy",
        "grader": "env.grader:grade_easy",
    },
    {
        "id": "medium",
        "name": "medium",
        "grader": "env.grader:grade_medium",
    },
    {
        "id": "hard",
        "name": "hard",
        "grader": "env.grader:grade_hard",
    },
]

TASKS = tasks
TASKS_WITH_GRADERS = tasks
TASK_LIST = tasks

__all__ = ["tasks", "TASKS", "TASKS_WITH_GRADERS", "TASK_LIST"]
