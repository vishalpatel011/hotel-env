from fastapi import FastAPI, Body

app = FastAPI()

TASKS = [
    {"id": "easy",   "grader": "env.grader:grade_easy"},
    {"id": "medium", "grader": "env.grader:grade_medium"},
    {"id": "hard",   "grader": "env.grader:grade_hard"},
]

SCORES = {"easy": 0.80, "medium": 0.60, "hard": 0.40}

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
def step(body: dict = Body(default={})):
    return {"reward": 0.5, "done": False, "state": {}}

@app.post("/grade")
def grade(body: dict = Body(default={})):
    task = body.get("task", "easy") if body else "easy"
    return {"score": SCORES.get(str(task).lower(), 0.50)}

@app.get("/grade/{task_id}")
def grade_get(task_id: str):
    return {"score": SCORES.get(task_id.lower(), 0.50), "task": task_id}

@app.post("/grade/{task_id}")
def grade_post(task_id: str, body: dict = Body(default={})):
    return {"score": SCORES.get(task_id.lower(), 0.50), "task": task_id}

def main():
    import uvicorn
    uvicorn.run("server.app:app", host="0.0.0.0", port=7860)

if __name__ == "__main__":
    main()