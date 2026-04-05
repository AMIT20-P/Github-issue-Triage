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
from fastapi.responses import FileResponse, JSONResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
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

# Allow all origins so automated checkers and agents can access the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# ─────────────────────────────────────────────
# Request body model for /reset
# Agent sends: { "task_id": "task_1" }
# ─────────────────────────────────────────────

class ResetRequest(BaseModel):
    task_id: str = "task_1"   # Default to easiest task if not specified


# ─────────────────────────────────────────────
# ENDPOINTS
# ─────────────────────────────────────────────

@app.get("/", summary="Welcome", include_in_schema=False)
def root():
    """Redirects to the visual dashboard."""
    return RedirectResponse(url="/dashboard")


@app.post("/reset", response_model=ResetResult, summary="Start a new episode")
def reset(request: ResetRequest = None):
    """
    **Start a new training episode.**
    - Clears all previous episode state
    - Returns the first GitHub issue for the agent to triage
    - Body is optional — defaults to task_1 if not provided

    **Request body (optional):**
    ```json
    { "task_id": "task_1" }
    ```
    task_id options: task_1 (easy) | task_2 (medium) | task_3 (hard)
    """
    try:
        task_id = request.task_id if request else "task_1"
        result = env.reset(task_id=task_id)
        return result
    except ValueError as e:
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

def main():
    """Named entry point for pyproject.toml scripts — runs the server."""
    import uvicorn
    uvicorn.run(
        "app:app",
        host   = "0.0.0.0",
        port   = 7860,
        reload = False,
    )

if __name__ == "__main__":
    main()
