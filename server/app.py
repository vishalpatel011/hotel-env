from fastapi import FastAPI
from pydantic import BaseModel
from env.environment import HotelEnv

app = FastAPI()
env = HotelEnv()

# 🔥 Request model (IMPORTANT)
class ActionRequest(BaseModel):
    action: str

@app.get("/")
def home():
    return {"message": "Hotel Booking Environment Running"}

@app.post("/reset")
def reset():
    state = env.reset()
    return {"state": str(state)}

@app.post("/step")
def step(req: ActionRequest):
    state, reward, done, _ = env.step(req.action)
    return {
        "state": str(state),
        "reward": reward,
        "done": done
    }

# 🔥 REQUIRED FOR OPENENV
def main():
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7860)

if __name__ == "__main__":
    main()