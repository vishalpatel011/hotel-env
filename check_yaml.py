import sys
from pathlib import Path

import yaml


def fail(message: str) -> None:
    print(f"FAIL: {message}")
    raise SystemExit(1)


def main() -> None:
    path = Path("openenv.yaml")
    if not path.exists():
        fail("openenv.yaml not found")

    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        fail("top-level YAML must be a mapping")

    tasks = data.get("tasks")
    if not isinstance(tasks, list):
        fail("'tasks' must be a list")

    valid_count = 0
    ids = set()
    errors: list[str] = []

    for i, task in enumerate(tasks):
        ctx = f"tasks[{i}]"
        if not isinstance(task, dict):
            errors.append(f"{ctx} is not a mapping")
            continue

        task_id = task.get("id")
        if not isinstance(task_id, str) or not task_id.strip():
            errors.append(f"{ctx}.id missing/invalid")
        elif task_id in ids:
            errors.append(f"{ctx}.id duplicate: {task_id}")
        else:
            ids.add(task_id)

        if not isinstance(task.get("difficulty"), str) or not task.get("difficulty").strip():
            errors.append(f"{ctx}.difficulty missing/invalid")

        if not isinstance(task.get("description"), str) or not task.get("description").strip():
            errors.append(f"{ctx}.description missing/invalid")

        grader = task.get("grader")
        if not isinstance(grader, dict):
            errors.append(f"{ctx}.grader missing/invalid")
            continue

        if grader.get("type") != "llm":
            errors.append(f"{ctx}.grader.type must be 'llm'")
            continue

        prompt = grader.get("prompt_template")
        if not isinstance(prompt, str) or not prompt.strip():
            errors.append(f"{ctx}.grader.prompt_template missing/invalid")
            continue

        valid_count += 1

    print(f"Task count: {len(tasks)}")
    print(f"Valid graders: {valid_count}")

    if errors:
        print("Errors:")
        for e in errors:
            print(f"- {e}")
        raise SystemExit(1)

    if valid_count < 3:
        fail("not enough valid tasks with graders (need at least 3)")

    print("PASS: openenv.yaml has enough valid tasks with graders.")


if __name__ == "__main__":
    main()
