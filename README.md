---
title: GitHub Issue Triage
emoji: 🐙
colorFrom: blue
colorTo: purple
sdk: docker
pinned: false
license: mit
short_description: OpenEnv RL environment for AI agents to triage GitHub issues
---

# 🐙 GitHub Issue Triage — OpenEnv Environment

> **MetaXScaler × Meta × PyTorch × Hugging Face Hackathon 2026**  
> An OpenEnv-compatible reinforcement learning environment where AI agents learn to triage GitHub issues.

[![OpenEnv](https://img.shields.io/badge/OpenEnv-Compatible-blue)](https://openenv.dev)
[![Python](https://img.shields.io/badge/Python-3.11-green)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-teal)](https://fastapi.tiangolo.com)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

---

## 🎯 What This Is

Open-source projects receive **thousands of GitHub issues daily** — bugs, feature requests, questions, duplicates. Maintainers spend **4–8 hours per day** just on triage: classifying, prioritizing, routing, and estimating effort for each issue.

This project builds an **OpenEnv-compatible RL training environment** where AI agents can learn to automate this process. Agents interact with realistic simulated GitHub issues and receive reward signals for making accurate triage decisions.

**The core idea:**
```
Agent reads issue → Makes triage decisions → Gets reward (0.0–1.0) → Learns to improve
```

---

## 🏗️ Architecture

```
github-issue-triage-env/
├── env/
│   ├── models.py             # Typed Pydantic models (observation + action spaces)
│   ├── issue_generator.py    # 50 realistic synthetic GitHub issues
│   ├── rewards.py            # Partial reward functions (0.0–1.0)
│   ├── tasks.py              # 3 task definitions + graders
│   └── environment.py        # Core engine: reset() / step() / state()
├── static/
│   └── dashboard.html        # Visual web UI at /dashboard
├── app.py                    # FastAPI server (exposes HTTP endpoints)
├── baseline.py               # Rule-based baseline agent
├── openenv.yaml              # OpenEnv specification config
├── Dockerfile                # Container configuration
└── requirements.txt          # Python dependencies
```

---

## 🎮 The 3 Tasks

| Task | Name | Difficulty | Steps | Fields Graded |
|------|------|-----------|-------|--------------|
| `task_1` | Issue Classification | 🟢 Easy | 10 | `issue_type` |
| `task_2` | Priority Assignment | 🟡 Medium | 8 | `issue_type` + `priority` |
| `task_3` | Full Triage | 🔴 Hard | 6 | All 4 fields (weighted) |

### Task 3 Scoring Weights
```
issue_type   → 25%
priority     → 30%   (most critical — wrong priority = wrong escalation)
team         → 30%   (most critical — wrong team = issue ignored)
effort       → 15%
```

---

## 🔀 Observation Space

What the agent **sees** each step:

```json
{
  "issue_id":          "issue_042",
  "title":             "App crashes on startup after v3.2 update",
  "body":              "## Bug Report\n1,200 crash reports in 2 hours...",
  "repo":              "mobile-app",
  "author_type":       "regular",
  "user_reports":      1200,
  "existing_labels":   [],
  "open_issues_count": 340,
  "task_id":           "task_1",
  "step_number":       3
}
```

---

## ⚡ Action Space

What the agent **does** each step:

```json
{
  "issue_type":       "bug",        
  "priority":         "P1",         
  "team":             "backend",    
  "estimated_effort": "small"       
}
```

**Allowed values:**
- `issue_type`: `bug` | `feature` | `question` | `documentation` | `duplicate`
- `priority`: `P1` (Critical) | `P2` (High) | `P3` (Medium) | `P4` (Low)
- `team`: `backend` | `frontend` | `devops` | `documentation` | `security` | `support`
- `estimated_effort`: `small` | `medium` | `large`

---

## 🏆 Reward Function

```python
# Task 1 — Binary (issue type only)
exact_match → 1.0  |  wrong → 0.0

# Task 2 — Weighted average
(type_score × 0.5) + (priority_score × 0.5)

# Task 3 — Fully weighted
(type × 0.25) + (priority × 0.30) + (team × 0.30) + (effort × 0.15)
```

**Partial rewards for priority:**
```
Exact match  → 1.0
1 level off  → 0.5   (P1 vs P2 — close, partial credit)
2 levels off → 0.2
3+ levels    → 0.0
```

---

## 🚀 Quick Start

### 1. Clone and Install
```bash
git clone https://github.com/yourusername/github-issue-triage-env
cd github-issue-triage-env
pip install -r requirements.txt
```

### 2. Start the Server
```bash
python app.py
```
Server starts at: **http://localhost:7860**

### 3. Open the Dashboard
Visit: **http://localhost:7860/dashboard**

Interactive visual UI — select a task, start an episode, submit triage decisions!

### 4. Explore the API
Visit: **http://localhost:7860/docs**

Swagger UI with interactive API testing for all endpoints.

### 5. Run Baseline Agent
```bash
# In a second terminal (server must be running):
python baseline.py
```

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|---------|-------------|
| `GET`  | `/` | Welcome message + endpoint list |
| `POST` | `/reset` | Start a new episode |
| `POST` | `/step`  | Submit a triage action |
| `GET`  | `/state` | Get current episode metadata |
| `GET`  | `/health`| Health check |
| `GET`  | `/docs`  | Swagger UI (interactive API docs) |
| `GET`  | `/dashboard` | Visual web UI |

### Example: Full Episode via API

```bash
# 1. Start episode
curl -X POST http://localhost:7860/reset \
  -H "Content-Type: application/json" \
  -d '{"task_id": "task_3"}'

# 2. Submit action
curl -X POST http://localhost:7860/step \
  -H "Content-Type: application/json" \
  -d '{
    "issue_type": "bug",
    "priority": "P1",
    "team": "backend",
    "estimated_effort": "small"
  }'

# 3. Check state
curl http://localhost:7860/state
```

---

## 🤖 Baseline Results

The included `baseline.py` uses simple keyword matching to demonstrate reproducible scores:

| Task | Score |
|------|-------|
| Task 1 — Issue Classification (Easy) | ~0.70 |
| Task 2 — Priority Assignment (Medium) | ~0.52 |
| Task 3 — Full Triage (Hard) | ~0.38 |
| **Overall** | **~0.53** |

> A trained RL agent would significantly outperform these baseline scores.

---

## 🐳 Docker

```bash
# Build the container
docker build -t github-issue-triage .

# Run the container
docker run -p 7860:7860 github-issue-triage

# Access at http://localhost:7860
```

---

## 💡 Why This Project?

| Problem | Our Solution |
|---------|-------------|
| Maintainers spend 8hrs/day on triage | AI agent handles it in milliseconds |
| Existing tools use static rules (no learning) | RL environment — agents continuously improve |
| No standard training ground existed | OpenEnv-compatible gym for triage agents |
| Real GitHub API has rate limits | Reproducible synthetic dataset (50 issues) |

---

## 🔮 Future Extensions

- 🔗 Connect to real GitHub API for live issue data
- 🌍 Multilingual issue support (Hindi, Spanish, French)
- 🤝 Multi-agent mode (one classifies, another reviews)
- 📈 Leaderboard for competing agents
- 🔮 LLM-powered agent backbone (GPT / LLaMA)

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| API Server | FastAPI + Uvicorn |
| Data Models | Pydantic v2 |
| Environment | Python 3.11 |
| Dashboard | HTML + Vanilla JS |
| Config | YAML |
| Deployment | Docker + Hugging Face Spaces |

---

## 📄 License

MIT License — free to use, modify, and distribute.

---

*Built for MetaXScaler × Meta × PyTorch × Hugging Face Hackathon 2026*
