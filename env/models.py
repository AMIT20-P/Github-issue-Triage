# env/models.py
# Typed Pydantic models — defines what the agent SEEs and DOES

from pydantic import BaseModel, Field
from typing import Optional, List
from enum import Enum


# ─────────────────────────────────────────────
#  ENUMS — fixed allowed values
# ─────────────────────────────────────────────

class IssueType(str, Enum):
    bug           = "bug"
    feature       = "feature"
    question      = "question"
    documentation = "documentation"
    duplicate     = "duplicate"


class Priority(str, Enum):
    P1 = "P1"   # Critical — production down, data loss
    P2 = "P2"   # High     — major feature broken
    P3 = "P3"   # Medium   — minor feature broken
    P4 = "P4"   # Low      — cosmetic, nice-to-have


class Team(str, Enum):
    backend  = "backend"
    frontend = "frontend"
    devops   = "devops"
    docs     = "documentation"
    security = "security"
    support  = "support"


class Effort(str, Enum):
    small  = "small"    # < 1 day
    medium = "medium"   # 1–3 days
    large  = "large"    # > 3 days


class TaskDifficulty(str, Enum):
    easy   = "task_1"
    medium = "task_2"
    hard   = "task_3"


# ─────────────────────────────────────────────
#  OBSERVATION — what the agent SEES each step
# ─────────────────────────────────────────────

class IssueObservation(BaseModel):
    """
    Everything the AI agent sees when it receives a GitHub issue.
    Think of this as the 'screen' the agent reads before taking action.
    """
    issue_id:          str            = Field(..., description="Unique issue ID e.g. issue_042")
    title:             str            = Field(..., description="Issue title written by user")
    body:              str            = Field(..., description="Full issue description")
    repo:              str            = Field(..., description="Repository name e.g. react, vscode")
    author_type:       str            = Field(..., description="first-time-contributor / regular / maintainer")
    user_reports:      int            = Field(..., description="How many users reported this same problem")
    existing_labels:   List[str]      = Field(default=[], description="Labels already on the issue")
    open_issues_count: int            = Field(..., description="Total open issues in the repo")
    task_id:           str            = Field(..., description="Which task: task_1 / task_2 / task_3")
    step_number:       int            = Field(..., description="Which step in the current episode")


# ─────────────────────────────────────────────
#  ACTION — what the agent DOES (its decision)
# ─────────────────────────────────────────────

class TriageAction(BaseModel):
    """
    The triage decision the AI agent submits.
    Task 1 uses only issue_type.
    Task 2 uses issue_type + priority.
    Task 3 uses all fields.
    """
    issue_type:        IssueType = Field(..., description="Type of issue")
    priority:          Priority  = Field(..., description="Urgency level P1–P4")
    team:              Team      = Field(..., description="Which team should handle this")
    estimated_effort:  Effort    = Field(..., description="How long will this take to fix")


# ─────────────────────────────────────────────
#  STEP RESULT — what step() returns
# ─────────────────────────────────────────────

class StepResult(BaseModel):
    """Returned by step() after agent submits an action."""
    observation: Optional[IssueObservation] = Field(None,  description="Next issue to triage (None if episode ended)")
    reward:      float                      = Field(...,   description="Score for this step: 0.0 to 1.0")
    is_done:     bool                       = Field(...,   description="True = episode finished")
    feedback:    str                        = Field(...,   description="Human-readable explanation of the reward")
    step_number: int                        = Field(...,   description="Current step count")

#STATE—metadata about current episode
class EpisodeState(BaseModel):
    """Returned by state() — metadata about where we are in the episode."""
    episode_id:      str   = Field(..., description="Unique episode identifier")
    current_task:    str   = Field(..., description="Which task is active: task_1/task_2/task_3")
    step_count:      int   = Field(..., description="Steps taken so far")
    max_steps:       int   = Field(..., description="Maximum steps in this episode")
    total_reward:    float = Field(..., description="Cumulative reward so far")
    is_active:       bool  = Field(..., description="Is an episode currently running?")


#RESET RESULT—what reset() returns
class ResetResult(BaseModel):
    """Returned by reset() when a new episode starts."""
    observation: IssueObservation = Field(..., description="First issue of the new episode")
    episode_id:  str              = Field(..., description="ID of the new episode")
    task_id:     str              = Field(..., description="Which task this episode runs")
    message:     str              = Field(..., description="Welcome message")
