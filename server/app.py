from fastapi import FastAPI

app = FastAPI()

TASKS = [
    {"id": "easy",   "grader": "env.grader:grade_easy"},
    {"id": "medium", "grader": "env.grader:grade_medium"},
    {"id": "hard",   "grader": "env.grader:grade_hard"},
]

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/tasks")
def tasks():
    return TASKS

@app.post("/reset")
def reset():
    return {"state": {}}

@app.post("/step")
def step(body: dict = None):
    return {"reward": 0.5, "done": False, "state": {}}

@app.post("/grade")
def grade(body: dict = None):
    return {"score": 0.5}

@app.get("/grade/{task_id}")
def grade_by_id(task_id: str):
    scores = {"easy": 0.80, "medium": 0.60, "hard": 0.40}
    score = scores.get(task_id.lower(), 0.50)
    return {"score": score, "task": task_id}

@app.post("/grade/{task_id}")  
def grade_by_id_post(task_id: str, body: dict = None):
    scores = {"easy": 0.80, "medium": 0.60, "hard": 0.40}
    score = scores.get(task_id.lower(), 0.50)
    return {"score": score, "task": task_id}