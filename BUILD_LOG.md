# BUILD LOG — GitHub Issue Triage OpenEnv Environment
> Hackathon: MetaXScaler x Meta x PyTorch x Hugging Face
> Project Started: March 27, 2026
> Goal: Build a complete AI agent training environment for GitHub issue triage

---

# PHASE 1 — Project Setup + Data Types
## Status: COMPLETE ✅

---

### 📦 File 1: requirements.txt

**What is it?**
A plain text file that lists all the external Python libraries this project needs.
Think of it like a shopping list — before cooking, you list all ingredients.

**Why do we need it?**
Python does not come with FastAPI, Pydantic etc built-in.
We need to tell Python "go download these tools" before we can use them.

**How to use it?**
Run this once: pip install -r requirements.txt
Python reads the file and installs everything automatically.

**What libraries are inside and why:**

| Library | Purpose |
|---------|---------|
| fastapi | Creates the web server (exposes /reset, /step, /state as URLs) |
| uvicorn | Runs the FastAPI server (like a waiter who receives requests) |
| pydantic | Validates data — makes sure agent sends correct format |
| pyyaml | Reads/writes YAML config files (openenv.yaml) |
| faker | Generates realistic fake names/data if needed |
| httpx | Lets Python make HTTP requests (used in baseline agent script) |

---

### 📦 File 2: env/__init__.py

**What is it?**
A completely empty file (or nearly empty) inside the env/ folder.

**Why do we need it?**
In Python, to treat a folder as a "package" that can be imported,
the folder MUST contain an __init__.py file.

Without it:
    from env.models import IssueObservation  ← ERROR!

With it:
    from env.models import IssueObservation  ← Works perfectly!

**Simple analogy:**
Think of it like a "registration certificate" for the folder.
The folder exists physically, but Python doesn't recognize it
as a package until it sees this file inside.

---

### 📦 File 3: env/models.py

**What is it?**
The file that defines ALL the data structures used across the entire project.
Every piece of data that moves between the agent and the environment
is defined here as a Python class.

**Why do we need it?**
Without defined types, data can be anything — which causes silent bugs.
Example: agent sends priority="URGENT!!!" instead of "P1"
Without models.py, Python accepts it. With models.py, it rejects it immediately.

**Two tools used inside:**

**Enum** — A fixed dropdown list of allowed values
    Instead of accepting any string, Enum restricts to specific options only.
    Example:
        class Priority(str, Enum):
            P1 = "P1"   ← only these 4 values allowed
            P2 = "P2"
            P3 = "P3"
            P4 = "P4"
    If agent sends "URGENT" → Python throws error immediately. Safe!

**Pydantic BaseModel** — Form validation for Python data
    Checks that all required fields are present and have correct types.
    Like a signup form that rejects you if you leave a field blank.

**What classes are defined:**

| Class | What it represents | Analogy |
|-------|--------------------|---------|
| IssueType | The 5 allowed issue types | Dropdown: bug/feature/question/docs/duplicate |
| Priority | The 4 priority levels | Dropdown: P1/P2/P3/P4 |
| Team | Which team handles the issue | Dropdown: backend/frontend/devops/docs/security/support |
| Effort | Time estimate | Dropdown: small/medium/large |
| IssueObservation | What the agent SEES per step | Question paper given to agent |
| TriageAction | What the agent DOES (its answer) | Answer sheet submitted by agent |
| StepResult | What step() returns | Teacher's marks + next question |
| EpisodeState | Current episode status | Scoreboard / progress tracker |
| ResetResult | What reset() returns | "New exam started!" message |

**IssueObservation fields (what agent sees):**
- issue_id: unique ID like "issue_042"
- title: the issue headline
- body: full description with steps to reproduce
- repo: which repository (e.g. "mobile-app", "web-frontend")
- author_type: first-time-contributor / regular / maintainer
- user_reports: how many users reported this same problem
- existing_labels: labels already applied
- open_issues_count: how busy is this repository
- task_id: which difficulty level (task_1 / task_2 / task_3)
- step_number: which step we are on in this episode

**TriageAction fields (what agent submits):**
- issue_type: bug / feature / question / documentation / duplicate
- priority: P1 / P2 / P3 / P4
- team: backend / frontend / devops / documentation / security / support
- estimated_effort: small / medium / large

**Tested:** ✅ python -c "from env.models import ..." — PASSED

---

# PHASE 2 — Training Data + Scoring + Task Levels
## Status: COMPLETE ✅

---

### 📦 File 4: env/issue_generator.py

**What is it?**
A file containing 50 fake but realistic GitHub issues.
This is our "training dataset" — the issues the AI agent will practice on.

**Why do we need it?**
Our environment simulates GitHub issue triage.
But we cannot connect to real GitHub (no API key, no internet dependency needed).
So we create our own dataset of fake issues that look exactly like real ones.

**Important design decision:**
Each issue in the list stores TWO things:
    1. The issue itself (title, body, repo — what agent sees)
    2. The CORRECT answer (correct_type, correct_priority, correct_team, correct_effort)

The agent sees only part 1.
The grader compares agent's answer with part 2 in secret.
This is exactly how an exam works — student sees question, teacher has answer key.

**Issue breakdown in our dataset:**
- 20 bug reports (crashes, errors, data loss, security issues)
- 19 feature requests (dark mode, 2FA, export CSV, webhooks etc.)
- 6 questions (how to reset password, API rate limits, setup help)
- 3 documentation issues (missing instructions, outdated guides)
- 2 duplicates (same issue reported twice by different users)
Total: 50 issues

**Functions available:**
- get_all_issues() → returns all 50 issues
- get_issue_by_id("issue_001") → fetch one specific issue
- get_issues_by_type("bug") → get all bugs only
- get_issues_by_priority("P1") → get all critical issues
- get_random_issue(task_id) → picks a random unseen issue for agent

**Tested:** ✅ Total: 50 | Bugs: 20 | Features: 19 | Questions: 6 — PASSED

---

### 📦 File 5: env/rewards.py

**What is it?**
The scoring brain of the project.
Every function here takes the agent's answer and the correct answer,
and returns a score between 0.0 and 1.0.

**Why do we need it?**
This is what teaches the AI agent.
If the agent gets a score, it knows how well it did.
If it gets partial scores repeatedly, it learns what was right and what was wrong.

**KEY CONCEPT: Partial Rewards**
Instead of just giving 0 (wrong) or 1 (right), we give partial credit.
This is crucial because:
    - Agent trying P2 when answer is P1 is MUCH better than trying P4
    - Binary scoring (0 or 1) would treat both mistakes equally
    - Partial scoring helps the agent learn DIRECTION — "I'm close, go 1 step higher"

**Scoring functions explained:**

score_issue_type(predicted, correct)
    What it does: Checks if agent picked the right issue type
    Score: 1.0 if correct, 0.0 if wrong
    Why no partial? Bug and feature are completely different — no "almost right"
    Example: predicted="bug", correct="bug" → 1.0
             predicted="feature", correct="bug" → 0.0

score_priority(predicted, correct)
    What it does: Checks how close the priority guess was
    Score:
        exact match  → 1.0
        1 level off  → 0.5  (said P2, correct was P1 — close!)
        2 levels off → 0.2  (said P3, correct was P1 — somewhat wrong)
        3+ levels    → 0.0  (said P4, correct was P1 — very wrong)
    Why partial? P1 vs P2 is a small mistake. P1 vs P4 is a huge mistake.
    Example: predicted="P2", correct="P1" → 0.5 (partial credit)

score_team(predicted, correct)
    What it does: Checks if agent routed to correct team
    Score: 1.0 if correct, 0.0 if wrong
    Why no partial? Wrong team = issue goes to wrong people entirely. No "almost right" routing.

score_effort(predicted, correct)
    What it does: Checks effort estimate accuracy
    Rankings: small=1, medium=2, large=3
    Score:
        exact match  → 1.0
        1 level off  → 0.5  (said medium, correct was small)
        2 levels off → 0.0  (said large, correct was small)

**Task-level reward calculators:**

calculate_task1_reward(action, correct)
    Used for: Task 1 (Easy)
    What it scores: issue_type only
    Returns: (score, feedback message)
    Example output: (1.0, "Correct! Issue type 'bug' is right.")

calculate_task2_reward(action, correct)
    Used for: Task 2 (Medium)
    What it scores: issue_type (50%) + priority (50%)
    How: Takes weighted average of both scores
    Example: type=1.0, priority=0.5 → total = (1.0×0.5) + (0.5×0.5) = 0.75

calculate_task3_reward(action, correct)
    Used for: Task 3 (Hard)
    What it scores: ALL 4 fields with weights:
        issue_type   → 25% of total score
        priority     → 30% of total score (most important)
        team         → 30% of total score (most important)
        effort       → 15% of total score
    Example: type=1.0 priority=0.5 team=1.0 effort=0.0
             → (1.0×0.25) + (0.5×0.30) + (1.0×0.30) + (0.0×0.15) = 0.70

get_reward(task_id, action, correct)
    The MAIN function — called by the rest of the project
    Routes to correct calculator based on task_id
    Returns: (final_score, feedback_string)

**Tested:** ✅
    Perfect answer Task 3 → reward=1.0
    Partial answer Task 3 → reward=0.4 (agent got type right, team/priority wrong)
    PASSED

---

### 📦 File 6: env/tasks.py

**What is it?**
The file that defines the 3 difficulty levels of the environment.
Think of it as defining 3 different exam papers — easy, medium, hard.

**Why do we need it?**
The problem statement requires minimum 3 tasks (easy → medium → hard).
tasks.py organizes all task-related information in one place
and acts as the bridge between the task definition and the scoring.

**What it contains:**

TASKS dictionary — stores all 3 task configurations:

Task 1: Issue Classification (Easy)
    - Difficulty: Easy
    - Agent must only classify the issue type (bug/feature/question etc.)
    - Episode length: 10 issues (10 steps per episode)
    - Fields graded: issue_type only
    - Why easy: The title alone usually tells you the type
      ("App crashes" = bug, "Please add dark mode" = feature)

Task 2: Priority Assignment (Medium)
    - Difficulty: Medium
    - Agent must classify type AND assign correct priority (P1-P4)
    - Episode length: 8 issues
    - Fields graded: issue_type + priority
    - Why medium: Priority requires reading the full body carefully.
      How many users affected? Is data lost? Is system down?
      These clues are in the body text, not just the title.

Task 3: Full Triage (Hard)
    - Difficulty: Hard
    - Agent must get ALL 4 fields correct (type + priority + team + effort)
    - Episode length: 6 issues (harder = fewer but deeper decisions)
    - Fields graded: all 4 fields with weighted scoring
    - Why hard: Multiple decisions, each affecting the others.
      Wrong team = issue reaches wrong people even if priority was right.

**Functions in tasks.py:**

get_task(task_id)
    Input: "task_1" or "task_2" or "task_3"
    Output: the full config dict for that task
    Use case: environment.py calls this to know max_steps etc.

get_all_tasks()
    Returns all 3 task configs as a list
    Used when generating the openenv.yaml file

grade(task_id, action, correct)
    THE MOST IMPORTANT function in this file
    Input: which task, agent's action, correct answer from issue bank
    Output: (reward score, feedback message)
    How it works: calls get_reward() from rewards.py internally

    This function is the BRIDGE:
        tasks.py  → knows WHAT challenge the agent is on
        rewards.py → knows HOW to score the answers
        grade()   → connects the two together

is_episode_done(task_id, step_count)
    Input: which task, how many steps taken so far
    Output: True (episode over) or False (keep going)
    How: checks if step_count >= max_steps for that task
    Example: Task 1 has max_steps=10
             step_count=9  → False (keep going)
             step_count=10 → True  (episode over!)

**Tested:** ✅
    get_task('task_1') → name=Issue Classification, max_steps=10 — PASSED
    grade('task_3', perfect_action, correct) → reward=1.0 — PASSED
    is_episode_done('task_1', 6) → False (max is 10) — PASSED

---

# PHASE 3 — Core Environment + API Server
## Status: COMPLETE ✅

---

### 📦 File 7: env/environment.py

**What is it?**
The most important file in the entire project.
This is the CORE ENGINE that connects all the previous files together
and actually implements the 3 OpenEnv API methods: reset(), step(), state().

**Simple analogy:**
If our project was a car:
    models.py          = parts catalog (defines all parts)
    issue_generator.py = fuel tank (provides raw material)
    rewards.py         = speedometer (measures performance)
    tasks.py           = gear system (controls difficulty)
    environment.py     = ENGINE (makes everything actually work together)

**How it connects all files:**
    Uses models.py          → for typed return values
    Uses issue_generator.py → to get the next GitHub issue
    Uses tasks.py           → for task config and grading
    Uses rewards.py         → (indirectly through tasks.grade())

**What it stores in memory (episode state):**
When an episode is running, this file remembers:
    episode_id    → unique ID for this episode (like a session ID)
    task_id       → which task is running (task_1/2/3)
    step_count    → how many steps taken so far
    total_reward  → sum of all rewards earned this episode
    seen_ids      → list of issue IDs already shown (no repeats)
    current_issue → the issue currently in front of the agent
    is_active     → is an episode running right now? (True/False)

**The 3 main methods:**

reset(task_id)
    What it does:
        1. Generates a fresh unique episode ID
        2. Clears all previous state (step count, rewards, seen issues)
        3. Picks first random GitHub issue for this task
        4. Returns ResetResult with first IssueObservation
    When called: Agent calls this to start a brand new episode
    Returns: ResetResult (first issue + episode ID + welcome message)

step(action)
    What it does:
        1. Checks a reset() was called first (safety check)
        2. Increments step count by 1
        3. Calls grade() from tasks.py to score agent's action
        4. Adds reward to running total
        5. Checks if episode is done (max steps reached)
        6. If not done: picks next random issue and returns it
        7. If done: returns None as next observation
    When called: Agent calls this after deciding what to do with current issue
    Returns: StepResult (reward + feedback + next issue OR None if done)

state()
    What it does:
        Just reads current episode memory and returns it
        Does NOT change anything — purely informational
    When called: Agent calls this anytime to check progress
    Returns: EpisodeState (episode_id, step_count, max_steps, total_reward)

_build_observation(issue) — private helper
    Converts raw issue dict from ISSUE_BANK into typed IssueObservation
    Called internally by reset() and step() (never by agent directly)
    The underscore means: for internal use only

**Tested:** ✅
    reset() → Episode ID generated, first issue returned — PASSED
    state() → Step 0/10, Reward 0.0, Active True — PASSED
    step()  → Reward returned, next issue provided, Done=False — PASSED

---

### 📦 File 8: app.py

**What is it?**
The FastAPI web server that wraps the environment and exposes it over HTTP.
It takes our Python code and turns it into a web service that anyone can use.

**Why do we need it?**
Without app.py:
    Only Python code can use the environment (internal only)
    No browser testing, no remote access, no deployment possible

With app.py (FastAPI server):
    Any AI agent from anywhere in the world can connect via HTTP
    Swagger UI auto-generated at /docs (like a browser preview for APIs)
    Can be deployed to Hugging Face Spaces as a live public URL

**The web dev comparison:**
    Web Dev → You write HTML/CSS/JS, browser shows you the result
    Our project → You run app.py, Swagger UI at /docs shows you the result

**What FastAPI does automatically:**
    Reads our Pydantic models (from models.py)
    Auto-generates interactive API documentation at /docs
    Validates all incoming requests automatically
    Returns proper error messages if wrong data is sent

**Endpoints created:**

GET /
    Returns a welcome message with list of all endpoints
    Like the home page of the API

POST /reset
    Calls env.reset(task_id)
    Agent sends: {"task_id": "task_1"}
    Returns: First GitHub issue + episode ID

POST /step
    Calls env.step(action)
    Agent sends: {"issue_type": "bug", "priority": "P1", "team": "backend", "estimated_effort": "small"}
    Returns: Reward + feedback + next issue (or None if done)

GET /state
    Calls env.state()
    Returns: Current episode metadata (step count, total reward, etc.)

GET /health
    Returns: {"status": "healthy"}
    Used by Docker and Hugging Face to check if server is running

GET /dashboard
    Serves the visual HTML dashboard (built in Phase 4)
    Accessible at http://localhost:7860/dashboard

**The shared environment instance:**
    app.py creates ONE instance of GitHubTriageEnvironment
    All HTTP requests use this SAME instance
    This is how episode state is preserved between reset() and step() calls

**How to run:**
    python app.py
    Server starts at: http://localhost:7860
    Swagger UI at:   http://localhost:7860/docs
    Dashboard at:    http://localhost:7860/dashboard

**Tested:** ✅
    Server started successfully on port 7860
    /docs Swagger UI loaded with all 5 endpoints visible
    POST /reset returned episode_id and first GitHub issue
    Response code 200 (success) confirmed — PASSED

---

### 📦 File 9: openenv.yaml

**What is it?**
A YAML config file that acts as the "identity card" of the environment.
Required by the OpenEnv specification.

**What is YAML?**
YAML is a file format for configuration — like JSON but cleaner (no brackets).
    JSON version: {"name": "github-issue-triage", "version": "1.0.0"}
    YAML version: name: github-issue-triage
                  version: 1.0.0
Same data, YAML is easier to read.

**Why do we need it?**
The OpenEnv standard requires this file.
Judges check this file to understand:
    - What is this environment called?
    - What tasks does it have?
    - What can the agent see? (observation space)
    - What can the agent do? (action space)
    - How is scoring designed?
Think of it like the back of a board game box — describes the rules without
you having to read all the code.

**What is inside openenv.yaml:**

name & version
    github-issue-triage, version 1.0.0
    Like a product label

description
    2-3 line summary of what the environment does

domain & task_type
    domain: software-engineering
    task_type: multi-label-classification

api section
    Lists the endpoints: /reset, /step, /state, port 7860

tasks section
    Lists all 3 tasks with id, name, difficulty,
    description, max_steps, fields_graded, reward_range

reward section
    Explains partial reward design
    Lists scoring weights for Task 3:
        issue_type=25%, priority=30%, team=30%, effort=15%

observation_space
    Documents all fields the agent can see:
    issue_id, title, body, repo, author_type,
    user_reports, existing_labels, open_issues_count, task_id, step_number

action_space
    Documents all choices the agent can make:
    issue_type: [bug, feature, question, documentation, duplicate]
    priority:   [P1, P2, P3, P4]
    team:       [backend, frontend, devops, documentation, security, support]
    effort:     [small, medium, large]

deployment section
    platform: huggingface-spaces
    type: docker
    port: 7860

**Tested:** ✅
    Python yaml.safe_load() reads the file correctly
    name, version, tasks, observation fields all verified — PASSED

---

# PHASE 4 — Baseline Agent + Web Dashboard + Docker
## Status: PENDING ⏳

### Files to build:

baseline.py
    A simple rule-based agent that "plays" through the environment.
    Used to prove the environment works and generate reproducible scores.

static/dashboard.html
    A visual web UI accessible at http://localhost:7860/dashboard
    Shows the current issue, agent's action, reward bar, episode progress.
    This is the "visual demo" for hackathon presentation.

Dockerfile
    Instructions for packaging the entire project into a Docker container.
    Anyone anywhere can run the environment with one command.

README.md
    Full documentation of the project.
    Required by the hackathon problem statement.

---

# PHASE 5 — Deploy to Hugging Face Spaces
## Status: PENDING ⏳

### Steps:
1. Create a free account on huggingface.co
2. Create a new Space (select Docker as the type)
3. Push the project code via Git
4. Hugging Face reads the Dockerfile and runs the server
5. A public URL is generated (e.g. https://username-github-issue-triage.hf.space)
6. Run the baseline script against the live URL to verify deployment

---

# CURRENT FILE STRUCTURE
```
MetaxScaler/
├── BUILD_LOG.md              ← This file (project diary)
├── notes.md                  ← Study notes and concepts
├── requirements.txt          ← Python dependencies ✅
├── openenv.yaml              ← Environment identity card ✅
├── app.py                    ← FastAPI web server ✅
└── env/
    ├── __init__.py           ← Makes env/ a Python package ✅
    ├── models.py             ← All data types defined ✅
    ├── issue_generator.py    ← 50 fake GitHub issues ✅
    ├── rewards.py            ← Scoring functions ✅
    ├── tasks.py              ← 3 task levels defined ✅
    └── environment.py        ← Core engine (reset/step/state) ✅
```

# OVERALL PROGRESS: 75% ████████████░░░░


---

# PHASE 4 — Baseline Agent + Web Dashboard + Docker
## Status: PENDING ⏳

### Files to build:

baseline.py
    A simple rule-based agent that "plays" through the environment.
    Used to prove the environment works and generate reproducible scores.

static/dashboard.html
    A visual web UI accessible at http://localhost:7860/dashboard
    Shows the current issue, agent's action, reward bar, episode progress.
    This is the "visual demo" for hackathon presentation.

Dockerfile
    Instructions for packaging the entire project into a Docker container.
    Anyone anywhere can run the environment with one command.

README.md
    Full documentation of the project.
    Required by the hackathon problem statement.

---

# PHASE 5 — Deploy to Hugging Face Spaces
## Status: PENDING ⏳

### Steps:
1. Create a free account on huggingface.co
2. Create a new Space (select Docker as the type)
3. Push the project code via Git
4. Hugging Face reads the Dockerfile and runs the server
5. A public URL is generated (e.g. https://username-github-issue-triage.hf.space)
6. Run the baseline script against the live URL to verify deployment

---

# CURRENT FILE STRUCTURE
```
MetaxScaler/
├── BUILD_LOG.md              ← This file (project diary)
├── notes.md                  ← Study notes and concepts
├── requirements.txt          ← Python dependencies ✅
└── env/
    ├── __init__.py           ← Makes env/ a Python package ✅
    ├── models.py             ← All data types defined ✅
    ├── issue_generator.py    ← 50 fake GitHub issues ✅
    ├── rewards.py            ← Scoring functions ✅
    └── tasks.py              ← 3 task levels defined ✅
```

# OVERALL PROGRESS: 83% █████████████░░░

---

# PHASE 4 LOG — Baseline Agent + Dashboard + Docker
## (Appended as completed)

---

### 📦 File 10: baseline.py

**What is it?**
A script that runs a simple fake agent through the entire environment.
It is NOT real artificial intelligence — it uses basic keyword matching (if/else).
Its purpose is to PROVE the environment works correctly end-to-end.

**Why do we need it?**
The hackathon problem statement requires:
"Baseline inference script with reproducible scores"

This means: run something through your environment and show consistent scores.
You don't need a trained AI. A rule-based dummy agent is perfectly acceptable
and is actually the standard approach for new environments.

**Why keyword matching works for baseline:**
    GitHub issues have predictable patterns in their titles/body:
    "crash" / "error" / "exception" → almost always a bug
    "add" / "support" / "please" → almost always a feature request
    "how" / "what" / "can i" → almost always a question
    So simple keyword matching gets maybe 60-70% correct — enough for a baseline.

**How it works — step by step:**

Step 1: Check server is running (GET /health)
    If server not running → print error and stop
    If running → continue

Step 2: Loop through all 3 tasks

Step 3: For each task, run 2 episodes
    (2 episodes to verify scores are reproducible — same score both times)

Step 4: Inside each episode:
    a. Call POST /reset with task_id → get first issue
    b. Read title + body of the issue
    c. rule_based_agent() decides action using keyword matching
    d. Call POST /step with action → get reward + next issue
    e. Print step details: issue title, agent decision, reward bar
    f. Repeat until is_done = True

Step 5: Calculate and print final scores for all tasks

**The rule_based_agent() function logic:**

For issue_type:
    Looks for: "crash", "error", "fail", "broken" → bug
    Looks for: "add", "support", "request", "feature" → feature
    Looks for: "how", "what", "can i", "question" → question
    Looks for: "readme", "docs", "documentation" → documentation
    Default: bug

For priority:
    user_reports > 500 OR "production down" / "crash" / "payment" → P1
    user_reports > 50  OR "enterprise" / "blocking" / "revenue" → P2
    user_reports > 5   OR "slow" / "occasionally" / "improvement" → P3
    Default: P4

For team:
    "security" / "injection" / "vulnerability" / "auth" → security
    "button" / "ui" / "dark mode" / "safari" / "frontend" → frontend
    "docker" / "deployment" / "ci" / "aws" → devops
    "readme" / "docs" / "documentation" → documentation
    Default: backend

For effort:
    "typo" / "quick" / "simple" / "minor" → small
    "mobile app" / "i18n" / "rewrite" / "large" → large
    Default: medium

**What the terminal output looks like when you run it:**
    =================================================================
      GitHub Issue Triage — Baseline Agent Evaluation
    =================================================================
      Server: http://localhost:7860
      Agent:  Rule-based keyword matching (not real AI)
    ─────────────────────────────────────────────────────────────────
      TASK: Issue Classification  (Easy)
    ─────────────────────────────────────────────────────────────────

      [Episode 1/2]
       Step  1 | Issue: App crashes immediately on launch after v3.2 update...
               Agent: type=bug  priority=P1  team=backend effort=small
               Reward: [██████████] 1.00 | Correct! Issue type 'bug' is right.

       Step  2 | Issue: Add dark mode support to the dashboard...
               Agent: type=feature  priority=P3  team=frontend effort=medium
               Reward: [██████████] 1.00 | Correct! Issue type 'feature' is right.
      ...
      Episode 1 avg reward: 0.700

    =================================================================
      BASELINE EVALUATION COMPLETE
    =================================================================
      Task 1 — Issue Classification  (Easy):   0.700
      Task 2 — Priority Assignment   (Medium):  0.520
      Task 3 — Full Triage           (Hard):    0.380

      Overall Baseline Score: 0.533 / 1.000
      ✅ Environment working correctly — all 3 tasks completed!

**How to run it yourself:**
    Step 1: Open terminal 1 → python app.py    (starts server)
    Step 2: Open terminal 2 → python baseline.py  (runs agent)
    Watch the output scroll — every step shows issue + agent decision + reward

**Tested:** ✅
    Server health check passed
    All 3 tasks ran without errors
    Rewards returned correctly (0.0 to 1.0 range)
    is_done triggered at correct step counts — PASSED


---

### ?? File 11: static/dashboard.html

**What is it?**
A visual web interface (webpage) for the environment.
Accessible at http://localhost:7860/dashboard once the server is running.
Built using plain HTML, CSS, and JavaScript � no extra framework needed.

**Why do we need it?**
The environment works purely through API calls (/reset, /step, /state).
For a hackathon DEMO, a visual UI makes a massive difference.
Judges and viewers can SEE the environment working in real time.
This is our WOW factor.

**What the dashboard shows (3 panels):**

LEFT PANEL � Control Panel:
    Task selector buttons (Easy / Medium / Hard)
    Start Episode button ? calls /reset
    Episode State: ID, task, status, progress bar
    Cumulative Reward running total

MIDDLE PANEL � Current Issue:
    Tags: repo name, user reports, task ID, author type
    Issue title (large, bold)
    Issue body (scrollable monospace text box)
    4 dropdowns: Issue Type, Priority, Team, Effort
    Green Submit button ? calls /step

RIGHT PANEL � Step History:
    Last Step Reward: score + color bar + feedback text
    Step Log: every step with issue title and score

**Tested:** ? Dashboard loaded, issue appeared, reward bar updated � PASSED

---

### ?? File 12: Dockerfile

**What is it?**
Instructions for packaging the entire project into a Docker container.
A Docker container = a sealed box with your code + Python + all libraries inside.

**Why do we need it?**
Hugging Face Spaces uses Docker to host projects publicly.
Without it: only runs on your laptop.
With it: runs anywhere, deployed publicly in one command.

**Analogy:**
    Your code = a recipe you wrote
    Docker    = a sealed box with everything pre-cooked inside
    Anyone opens the box, food is ready � no setup needed

**Key instructions inside Dockerfile:**
    FROM python:3.11-slim   ? start with bare Python 3.11
    WORKDIR /app            ? work inside /app folder
    COPY requirements.txt . ? copy dependency list first (for caching)
    RUN pip install ...      ? install all libraries during build
    COPY . .                ? copy all project files
    EXPOSE 7860             ? open port 7860 (required by HF Spaces)
    CMD [uvicorn ...]       ? start the FastAPI server when container runs

**Tested:** ? Dockerfile syntax verified � PASSED

---

# OVERALL PROGRESS: 92% ����������������
