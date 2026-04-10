from importlib import import_module
from typing import Any

__all__ = [
    "HotelEnv",
    "grade_easy",
    "grade_medium",
    "grade_hard",
    "tasks",
    "TASKS",
    "TASKS_WITH_GRADERS",
    "TASK_LIST",
    "TASK_GRADERS",
    "GRADERS",
]

_MODULE_BY_ATTR = {
    "HotelEnv": "env.environment",
    "grade_easy": "env.grader",
    "grade_medium": "env.grader",
    "grade_hard": "env.grader",
    "tasks": "env.tasks",
    "TASKS": "env.tasks",
    "TASKS_WITH_GRADERS": "env.tasks",
    "TASK_LIST": "env.tasks",
    "TASK_GRADERS": "env.tasks",
    "GRADERS": "env.tasks",
}


def __getattr__(name: str) -> Any:
    module_name = _MODULE_BY_ATTR.get(name)
    if module_name is None:
        raise AttributeError(f"module 'env' has no attribute {name!r}")
    module = import_module(module_name)
    return getattr(module, name)
