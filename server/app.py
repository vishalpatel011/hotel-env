from fastapi import FastAPI
from env.environment import HotelEnv

app = FastAPI()

env = HotelEnv()

@app.get("/")
def home():
    return {"message": "Hotel Booking Environment Running"}

@app.get("/reset")
def reset():
    state = env.reset()
    return {"state": str(state)}

@app.get("/step")
def step(action: str = "book_room"):
    state, reward, done, _ = env.step(action)
    return {
        "state": str(state),
        "reward": reward,
        "done": done
    }