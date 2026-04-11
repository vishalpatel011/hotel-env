---
title: Hotel Booking Environment
emoji: 🏨
colorFrom: indigo
colorTo: purple
sdk: docker
app_port: 7860
base_path: /docs
tags:
  - openenv
  - reinforcement-learning
  - hotel-booking
  - rl-environment
---

# 🏨 Hotel Booking OpenEnv Environment

> A real-world reinforcement learning environment for training agents to make
> optimal hotel booking decisions — built on the
> [OpenEnv](https://github.com/meta-pytorch/OpenEnv) framework for the
> Meta PyTorch × Scaler School of Technology Hackathon 2026.

[![OpenEnv](https://img.shields.io/badge/OpenEnv-compatible-blue)](https://github.com/meta-pytorch/OpenEnv)
[![HF Space](https://img.shields.io/badge/🤗%20Space-live-green)](https://huggingface.co/spaces/infiniter011/hotel-env)
[![Phase 1](https://img.shields.io/badge/Phase%201-✅%20Passed-brightgreen)]()
[![Phase 2](https://img.shields.io/badge/Phase%202-✅%20Passed-brightgreen)]()

---

## 🧠 What Is This Environment?

The **Hotel Booking Environment** simulates a real-world hotel reservation
system where an AI agent must serve a customer's booking request as efficiently
as possible.

The agent receives a customer request (room type, check-in, check-out dates)
and must navigate the hotel's room inventory using a discrete action space to
complete the booking — while avoiding conflicts, invalid actions, and wasted
steps.

This environment is specifically designed to be interesting for RL because:

- **Partial observability**: the agent sees room availability but must infer
  conflicts from prior bookings.
- **Sparse + shaped rewards**: success only on correct booking, with
  intermediate signals for useful exploration.
- **Sequential decision-making**: the optimal policy requires at least 2 steps
  (check → book), teaching agents to plan ahead rather than act greedily.
- **Failure modes**: booking the wrong room type, double-booking, or cancelling
  unnecessarily all carry penalties — mirroring real-world cost structures.

---

## 🎮 Action Space

| Action | Description |
|---|---|
| `check_availability` | Scan all rooms and return current booking status |
| `book_room <room_id>` | Attempt to book a specific room (e.g. `book_room 201`) |
| `cancel_booking` | Cancel the most recent booking |

The agent must learn **which room IDs match the requested room type** and
**when to check availability vs. book directly** — a non-trivial policy for
a naive agent.

---

## 👁️ Observation Space

Each step returns a full environment state:

```json
{
  "rooms": [
    {"id": 101, "type": "single", "bookings": []},
    {"id": 102, "type": "single", "bookings": []},
    {"id": 201, "type": "double", "bookings": []},
    {"id": 202, "type": "double", "bookings": []},
    {"id": 301, "type": "suite",  "bookings": []}
  ],
  "bookings": [],
  "request": {
    "room_type": "double",
    "check_in": 10,
    "check_out": 12
  }
}
```

The agent must learn to read `request.room_type`, find a matching room in
`rooms`, verify there are no conflicting `bookings`, and then issue the correct
`book_room <id>` action.

---

## 🏆 Reward Structure

| Event | Reward | Rationale |
|---|---|---|
| Successful booking | `+1.0` | Primary goal achieved |
| Check availability | `+0.1` | Useful exploratory step |
| Cancel & rebook correctly | `+0.2` | Recovery behavior rewarded |
| Wrong room / conflict | `-0.5` | Penalise type mismatch |
| Invalid or no-op action | `-0.1` | Discourage random exploration |

The reward is **shaped but sparse at the terminal** — an agent that just
spams random actions will average around `-0.1` per step. An optimal 2-step
policy (`check_availability` → `book_room 201`) achieves `+1.1` in two steps,
giving a strong learning signal for GRPO and similar RL algorithms.

---

## 📋 Tasks

Three tasks of increasing difficulty are defined for structured evaluation:

| Task | Description | Optimal Policy |
|---|---|---|
| **Easy** | Check availability, then book a double room | `check_availability` → `book_room 201` |
| **Medium** | Book, cancel, and rebook successfully | `check_availability` → `book_room 201` → `cancel_booking` → `book_room 202` |
| **Hard** | Book directly without availability check | `book_room 201` |

Grader scores are **dynamic** — computed by actually running the environment
with the reference policy and converting cumulative reward to a `(0, 1)` score.

---

## 🔌 API Endpoints

The environment is served as a FastAPI application:

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/health` | Liveness check |
| `GET` | `/tasks` | List all tasks with grader paths |
| `POST` | `/reset` | Reset environment, returns initial state |
| `POST` | `/step` | Execute action, returns next state + reward |
| `GET` | `/state` | Get current state without stepping |
| `POST` | `/grade` | Get current score for a task |
| `GET` | `/grade/{task_id}` | Get score for a specific task |
| `GET` | `/docs` | Interactive Swagger UI |

---

## 🤖 LLM Agent (inference.py)

The inference script runs an LLM agent against all three tasks using the
OpenAI-compatible API proxy:

```python
# The agent receives the full state as context and must output
# the next action — no hardcoded heuristics, pure LLM reasoning.
prompt = f"""
Customer wants: {room_type} room, check-in day {check_in}, check-out day {check_out}
Available rooms: {rooms_summary}
Action history: {history}
Choose the next action: check_availability / book_room <id> / cancel_booking
"""
```

The agent is evaluated on actual task performance — not simulated scores.

**Model:** `gpt-4o-mini` via `API_BASE_URL` proxy

---

## 🚀 Quick Start

### Run locally

```bash
git clone https://github.com/vishalpatel011/hotel-env
cd hotel-env
python -m venv venv && source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn server.app:app --host 0.0.0.0 --port 7860
# Open http://localhost:7860/docs
```

### Run with Docker

```bash
docker build -t hotel-env .
docker run -p 7860:7860 \
  -e API_BASE_URL="https://router.huggingface.co/v1" \
  -e API_KEY="your_hf_token" \
  hotel-env
```

### Run inference agent

```bash
export API_BASE_URL="https://router.huggingface.co/v1"
export API_KEY="your_hf_token"
python inference.py
```

---

## 🗂️ Project Structure

```
hotel-env/
├── env/
│   ├── environment.py      # Core HotelEnv logic (step, reset, reward)
│   ├── grader.py           # Dynamic task graders (grade_easy/medium/hard)
│   ├── models.py           # Pydantic models: Room, BookingRequest, Observation
│   └── openenv_env.py      # OpenEnv-compatible wrapper
├── server/
│   └── app.py              # FastAPI server with all endpoints
├── inference.py            # LLM agent runner ([START]/[STEP]/[END] output)
├── openenv.yaml            # OpenEnv manifest
├── Dockerfile              # Container definition
└── requirements.txt
```

---

## 🔬 Why This Is Interesting for RL

Hotel booking is a microcosm of real-world **tool-using agent** tasks:

1. **State interpretation** — the agent must parse structured JSON observations
   and extract task-relevant fields (`room_type`, `bookings`).
2. **Grounded action selection** — actions have parameters (`book_room 201`)
   that require understanding the observation to fill correctly.
3. **Credit assignment** — with a 2-step optimal path, the agent must learn
   that `check_availability` at step 1 gets rewarded indirectly through the
   successful booking at step 2.
4. **Recovery** — the medium task requires cancel + rebook, testing whether
   the agent can recover from a suboptimal state rather than getting stuck.

This makes it a natural fit for **GRPO**, **PPO**, and **rejection sampling**
fine-tuning pipelines — the kind of environments OpenEnv is built for.

---

## 🔭 Possible Extensions

- Date-range conflict detection (overlapping bookings)
- Multi-user contention (two agents competing for the same room)
- Dynamic pricing (reward shaped by cost efficiency)
- Longer horizons (multi-night, multi-room group bookings)
- Natural language actions (free-form text → parsed intent)

---

## 👥 Team InvincibleX

- **Vishal Patel**
- **Mukesh Tiwari**
- **Rishi Patel**

---

## 🔗 Links

- 🤗 HF Space: https://huggingface.co/spaces/infiniter011/hotel-env
- 💻 GitHub: https://github.com/vishalpatel011/hotel-env
- 📖 OpenEnv Docs: https://meta-pytorch.org/OpenEnv
- 🏆 Hackathon: https://www.scaler.com/school-of-technology/meta-pytorch-hackathon