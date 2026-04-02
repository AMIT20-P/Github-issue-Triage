# app.py
# The FastAPI web server — exposes the environment over HTTP
#
# This file does 3 things:
#   1. Creates the FastAPI application
#   2. Creates ONE shared instance of GitHubTriageEnvironment
#   3. Defines HTTP endpoints: /reset, /step, /state
#
# Once this runs, any AI agent can connect via HTTP and use the environment
# It also auto-generates a Swagger UI at /docs for visual testing

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
import os

from env.environment import GitHubTriageEnvironment
from env.models import TriageAction, ResetResult, StepResult, EpisodeState

# ─────────────────────────────────────────────
# Create the FastAPI app
# The title and description appear in Swagger UI at /docs
# ─────────────────────────────────────────────

app = FastAPI(
    title       = "GitHub Issue Triage Environment",
    description = (
        "An OpenEnv-compatible reinforcement learning environment "
        "where AI agents learn to triage GitHub issues. "
        "Agents classify issue types, assign priorities, route to teams, "
        "and estimate effort — earning rewards for correct decisions.\n\n"
        "**Tasks:**\n"
        "- task_1 (Easy): Issue Classification\n"
        "- task_2 (Medium): Priority Assignment\n"
        "- task_3 (Hard): Full Triage\n\n"
        "**Usage:** Call /reset to start, /step to submit actions, /state for metadata."
    ),
    version     = "1.0.0",
)

# ─────────────────────────────────────────────
# ONE shared environment instance
# All HTTP requests use this same instance
# This way the episode state is preserved across calls
# (reset() sets state, step() reads it, state() reads it)
# ─────────────────────────────────────────────

env = GitHubTriageEnvironment()


# ─────────────────────────────────────────────
# Request body model for /reset
# Agent sends: { "task_id": "task_1" }
# ─────────────────────────────────────────────

class ResetRequest(BaseModel):
    task_id: str = "task_1"   # Default to easiest task if not specified


# ─────────────────────────────────────────────
# ENDPOINTS
# ─────────────────────────────────────────────

@app.get("/", summary="Welcome message")
def root():
    """
    Root endpoint — returns a welcome message and links.
    Visit /docs for the interactive Swagger UI.
    """
    return {
        "message"     : "Welcome to the GitHub Issue Triage OpenEnv Environment!",
        "version"     : "1.0.0",
        "docs"        : "/docs",
        "dashboard"   : "/dashboard",
        "endpoints"   : {
            "reset" : "POST /reset — Start a new episode",
            "step"  : "POST /step  — Submit a triage action",
            "state" : "GET  /state — Check current episode state",
        },
        "tasks": {
            "task_1": "Issue Classification (Easy)   — 10 steps",
            "task_2": "Priority Assignment (Medium)   — 8 steps",
            "task_3": "Full Triage (Hard)             — 6 steps",
        }
    }


@app.post("/reset", response_model=ResetResult, summary="Start a new episode")
def reset(request: ResetRequest):
    """
    **Start a new training episode.**

    - Clears all previous episode state
    - Returns the first GitHub issue for the agent to triage
    - Agent must call this before calling /step

    **Request body:**
    ```json
    { "task_id": "task_1" }
    ```
    task_id options: task_1 (easy) | task_2 (medium) | task_3 (hard)
    """
    try:
        result = env.reset(task_id=request.task_id)
        return result
    except ValueError as e:
        # Invalid task_id was sent
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/step", response_model=StepResult, summary="Submit a triage action")
def step(action: TriageAction):
    """
    **Submit the agent's triage decision for the current issue.**

    - Scores the action against the correct answer
    - Returns reward (0.0–1.0) + feedback + next issue
    - Returns is_done=True when episode ends

    **Request body:**
    ```json
    {
      "issue_type"       : "bug",
      "priority"         : "P1",
      "team"             : "backend",
      "estimated_effort" : "small"
    }
    ```
    """
    try:
        result = env.step(action)
        return result
    except RuntimeError as e:
        # step() called before reset()
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/state", response_model=EpisodeState, summary="Get current episode state")
def state():
    """
    **Get metadata about the current episode.**

    Returns information like:
    - episode_id, current_task
    - step_count and max_steps
    - total_reward accumulated so far
    - is_active (whether an episode is running)

    Does NOT advance the episode — purely informational.
    """
    return env.state()


@app.get("/health", summary="Health check")
def health():
    """Simple health check endpoint — used by Docker and Hugging Face to verify server is running."""
    return {"status": "healthy", "environment": "github-issue-triage"}


# ─────────────────────────────────────────────
# Dashboard endpoint — serves the visual HTML UI
# We will build static/dashboard.html in Phase 4
# ─────────────────────────────────────────────

@app.get("/dashboard", summary="Visual dashboard", include_in_schema=False)
def dashboard():
    """Serves the visual web dashboard for demo purposes."""
    dashboard_path = os.path.join("static", "dashboard.html")
    if os.path.exists(dashboard_path):
        return FileResponse(dashboard_path)
    return JSONResponse(
        status_code = 200,
        content     = {"message": "Dashboard coming soon! Use /docs for now."}
    )


# ─────────────────────────────────────────────
# Run the server
# Only executes when file is run directly: python app.py
# (Not when imported by other files)
# ─────────────────────────────────────────────

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app:app",
        host    = "0.0.0.0",  # Accept connections from any IP
        port    = 7860,        # Port 7860 is required by Hugging Face Spaces
        reload  = False,       # No auto-reload in production
    )
