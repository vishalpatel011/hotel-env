from fastapi import FastAPI

app = FastAPI()

TASKS = [
    {
        "id": "easy",
        "grader": "env.grader:grade_easy",
        "description": "Basic task",
    },
    {
        "id": "medium",
        "grader": "env.grader:grade_medium",
        "description": "Intermediate task",
    },
    {
        "id": "hard",
        "grader": "env.grader:grade_hard",
        "description": "Advanced task",
    },
]

@app.get("/")
def home():
    return {"status": "ok"}

@app.get("/tasks")
def list_tasks():
    return TASKS

@app.post("/reset")
def reset():
    return {"status": "reset ok"}

def main():
    import uvicorn
    uvicorn.run("server.app:app", host="0.0.0.0", port=7860)

if __name__ == "__main__":
    main()