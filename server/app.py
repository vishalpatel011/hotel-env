from fastapi import FastAPI
from env.environment import HotelEnv

app = FastAPI()
env = HotelEnv()

@app.get("/reset")
def reset():
    return env.reset()

@app.post("/step")
def step(action: dict):
    action_value = action.get("action")
    state, reward, done, _ = env.step(action_value)

    return {
        "state": state,
        "reward": reward,
        "done": done
    }

def main():
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7860)

# ✅ IMPORTANT FIX
if __name__ == "__main__":
    main()