from fastapi import FastAPI
from env.environment import HotelEnv

app = FastAPI()
env = HotelEnv()

@app.get("/")
def home():
    return {"message": "Hotel Booking Environment Running"}

@app.post("/reset")
def reset():
    state = env.reset()
    return {"state": str(state)}

@app.post("/step")
def step(action: str = "book_room"):
    state, reward, done, _ = env.step(action)
    return {
        "state": str(state),
        "reward": reward,
        "done": done
    }

# 🔥 ADD THIS PART (VERY IMPORTANT)
def main():
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7860)

if __name__ == "__main__":
    main()