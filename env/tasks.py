# env/tasks.py
# Defines the 3 task levels for the environment
# Each task has its own configuration and grader
#
# Task 1 (Easy)   → classify the issue type only
# Task 2 (Medium) → classify type + assign priority
# Task 3 (Hard)   → full triage: type + priority + team + effort

from env.models import TriageAction
from env.rewards import get_reward

TASKS = {
    "task_1": {
        "task_id":     "task_1",
        "name":        "Issue Classification",
        "difficulty":  "easy",
        "description": (
            "Classify the GitHub issue into one of 5 types: "
            "bug, feature, question, documentation, or duplicate. "
            "Read the title and body carefully to decide."
        ),
        "max_steps":   10,      
        "fields_used": ["issue_type"],   
        "score_range": "0.0 to 1.0",
    },

    "task_2": {
        "task_id":     "task_2",
        "name":        "Priority Assignment",
        "difficulty":  "medium",
        "description": (
            "Classify the issue type AND assign the correct priority level "
            "(P1-Critical, P2-High, P3-Medium, P4-Low). "
            "Consider user impact, number of affected users, and severity."
        ),
        "max_steps":   8,        
        "fields_used": ["issue_type", "priority"],
        "score_range": "0.0 to 1.0",
    },

    "task_3": {
        "task_id":     "task_3",
        "name":        "Full Triage",
        "difficulty":  "hard",
        "description": (
            "Perform complete triage: classify type, assign priority, "
            "route to the correct team, and estimate development effort. "
            "All 4 fields are scored with weighted importance."
        ),
        "max_steps":   6,        
        "fields_used": ["issue_type", "priority", "team", "estimated_effort"],
        "score_range": "0.0 to 1.0",
    },
}


def get_task(task_id: str) -> dict:
    """
    Returns the task config dict for a given task_id.
    Raises ValueError if task_id is not valid.
    """
    if task_id not in TASKS:
        raise ValueError(
            f"Invalid task_id '{task_id}'. "
            f"Choose from: {list(TASKS.keys())}"
        )
    return TASKS[task_id]


def get_all_tasks() -> list:
    """Returns list of all task configs (used in openenv.yaml generation)."""
    return list(TASKS.values())


def grade(task_id: str, action: TriageAction, correct_issue: dict) -> tuple[float, str]:
    """
    Main grader function.
    Takes the task, agent's action, and the correct answer.
    Returns (reward, feedback) by calling the right reward function.

    This is the bridge between tasks and rewards:
        tasks.py  → knows WHAT to test
        rewards.py → knows HOW to score it
        grade()   → connects the two
    """
    # Delegate scoring to rewards.py
    reward, feedback = get_reward(task_id, action, correct_issue)
    return reward, feedback


def is_episode_done(task_id: str, step_count: int) -> bool:
    """
    Returns True when the episode should end.
    Episode ends when agent has seen max_steps issues for this task.
    """
    task = get_task(task_id)
    return step_count >= task["max_steps"]
