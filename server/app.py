from fastapi import FastAPI

app = FastAPI()

# 🔥 TASKS (validator reads this)
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


# 🔥 REQUIRED ENDPOINT
@app.get("/tasks")
def list_tasks():
    return TASKS


# 🔥 HEALTH CHECK (safe)
@app.get("/")
def home():
    return {"status": "ok"}


# 🔥 REQUIRED for HF
def main():
    import uvicorn
    uvicorn.run("server.app:app", host="0.0.0.0", port=7860)


if __name__ == "__main__":
    main()