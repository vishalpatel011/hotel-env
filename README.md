---
title: Hotel Booking Environment Server
sdk: docker
app_port: 7860
base_path: /docs
tags:
  - openenv
---

# Hotel Booking OpenEnv Environment

This project implements a real-world hotel booking environment using the OpenEnv framework.
It is designed to evaluate how well an AI agent can make decisions in a structured system using rewards and state transitions.

---

## Overview

The environment simulates a simple hotel booking workflow where an agent must:

* check available rooms
* select the correct room type
* complete bookings efficiently

The focus is on decision-making quality rather than just task completion.

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

* Easy: book any available room
* Medium: book the correct room type
* Hard: complete booking efficiently with minimal steps

---

## Reward Design

* correct booking → +1.0
* availability check → +0.2
* incorrect booking → -0.5
* invalid action → -0.1

The reward function encourages both correctness and efficiency.

---

## Agent

The agent uses an OpenAI-compatible client with a Hugging Face inference router.
Model used: `Qwen/Qwen2.5-72B-Instruct`.

---

## Running the Project

### Docker

```bash
docker build -t hotel-env .
docker run -e API_BASE_URL="https://router.huggingface.co/v1" -e MODEL_NAME="Qwen/Qwen2.5-72B-Instruct" -e HF_TOKEN="your_token" hotel-env
```

### Local

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn server.app:app --host 0.0.0.0 --port 7860
```

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

This environment is intentionally kept simple but structured to reflect real-world booking logic.
It can be extended with date handling, multiple users, and pricing strategies.

---

## Author

Vishal Patel

---
title: Hotel Env
emoji: 😻
colorFrom: indigo
colorTo: purple
sdk: docker
pinned: false
---

Check out the configuration reference at https://huggingface.co/docs/hub/spaces-config-reference
