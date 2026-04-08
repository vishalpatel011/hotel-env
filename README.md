---

title: Hotel Booking Environment Server
emoji: 🏨
colorFrom: indigo
colorTo: purple
sdk: docker
app_port: 7860
base_path: /docs
tags:
  - openenv

---

# Hotel Booking OpenEnv Environment

This project implements a real-world hotel booking environment using the OpenEnv framework.
It evaluates how effectively an AI agent can make decisions in a structured system using states, actions, and rewards.

---

## Overview

The environment simulates a hotel booking workflow where an agent must:

* check available rooms
* select the correct room type
* complete bookings efficiently

The focus is on **decision-making quality and efficiency**, not just task completion.

---

## Actions

* `check_availability`
* `book_room`
* `cancel_booking`

---

## Observation

```json
{
  "rooms": [{"id": 101, "type": "single", "available": true}],
  "bookings": [],
  "request": {"room_type": "single", "days": 2}
}
```

---

## Tasks

* **Easy** → Book any available room
* **Medium** → Book the correct room type
* **Hard** → Complete booking efficiently with minimal steps

---

## Reward Design

* +1.0 → Correct booking
* +0.2 → Availability check
* -0.5 → Incorrect booking
* -0.1 → Invalid action

The reward system balances correctness with efficiency.

---

## Agent

The agent uses an OpenAI-compatible client via the Hugging Face inference router.

**Model used:**
`Qwen/Qwen2.5-72B-Instruct`

---

## Running the Project

### Docker

```bash
docker build -t hotel-env .
docker run -e API_BASE_URL="https://router.huggingface.co/v1" \
           -e MODEL_NAME="Qwen/Qwen2.5-72B-Instruct" \
           -e HF_TOKEN="your_token" \
           hotel-env
```

---

### Local

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn server.app:app --host 0.0.0.0 --port 7860
```

---

## API Access

After running, open:

http://localhost:7860/docs

---

## Project Structure

```
hotel-env/
├── env/
├── server/
├── inference.py
├── openenv.yaml
├── Dockerfile
└── README.md
```

---

## Notes

This environment is intentionally simple but structured to reflect real-world booking logic.
It can be extended with:

* date-based booking conflicts
* multiple users
* pricing strategies
* dynamic availability

---

## Team

* Vishal Patel
* Mukesh Tiwari
* Rishi Patel

---

## Links

* Hugging Face Space: https://huggingface.co/spaces/infiniter011/hotel-env
* GitHub Repository: https://github.com/vishalpatel011/hotel-env

---
