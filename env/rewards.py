# env/rewards.py
# Calculates reward scores for each task
# All functions return a float between 0.0 and 1.0
#
# KEY IDEA: Partial rewards
#   Instead of just 0 or 1, we give partial credit
#   so the agent always has a learning signal
#   Example: priority 1 level off → 0.5 (not 0)

from env.models import TriageAction
PRIORITY_RANK = {
    "P1": 1,
    "P2": 2,
    "P3": 3,
    "P4": 4,
}

def score_issue_type(predicted: str, correct: str) -> float:
    """
    Task 1 scoring — Did the agent classify the issue type correctly?

    Simple binary:
        exact match → 1.0
        wrong       → 0.0

    No partial credit here because types are very different from each other
    (bug vs feature vs question — no "close enough")
    """
    if predicted == correct:
        return 1.0
    return 0.0


def score_priority(predicted: str, correct: str) -> float:
    """
    Task 2 scoring — Did the agent assign the right priority?

    Partial credit based on how far off:
        exact match → 1.0
        1 level off → 0.5   (e.g. said P2, correct was P1)
        2 levels off → 0.2  (e.g. said P3, correct was P1)
        3+ levels off → 0.0 (e.g. said P4, correct was P1)

    Why partial? Because P1 vs P2 is a much smaller mistake
    than P1 vs P4. The agent should be rewarded for being "close".
    """
    pred_rank = PRIORITY_RANK.get(predicted, 4)
    corr_rank = PRIORITY_RANK.get(correct, 4)

    diff = abs(pred_rank - corr_rank)

    if diff == 0:
        return 1.0
    elif diff == 1:
        return 0.5
    elif diff == 2:
        return 0.2
    else:
        return 0.0


def score_team(predicted: str, correct: str) -> float:
    """
    Task 2/3 scoring — Did the agent route to the correct team?

    Binary — either right team or wrong team.
    No partial credit because routing to wrong team
    means the wrong people receive the issue entirely.
    """
    if predicted == correct:
        return 1.0
    return 0.0


def score_effort(predicted: str, correct: str) -> float:
    """
    Task 3 scoring — Did the agent estimate effort correctly?

    Effort ranking: small=1, medium=2, large=3
    Partial credit for being 1 level off.
    """
    effort_rank = {"small": 1, "medium": 2, "large": 3}

    pred_rank = effort_rank.get(predicted, 2)
    corr_rank = effort_rank.get(correct, 2)

    diff = abs(pred_rank - corr_rank)

    if diff == 0:
        return 1.0
    elif diff == 1:
        return 0.5
    else:
        return 0.0


#TASK-LEVEL REWARD CALCULATORS
#Each function takes the agent's action and
#the correct answer, returns a reward + feedback

def calculate_task1_reward(action: TriageAction, correct: dict) -> tuple[float, str]:
    """
    Task 1 (Easy) — Only checks issue_type.
    Returns: (reward_score, feedback_message)
    """
    type_score = score_issue_type(action.issue_type, correct["correct_type"])

    if type_score == 1.0:
        feedback = f"Correct! Issue type '{action.issue_type}' is right."
    else:
        feedback = (
            f"Wrong type. You said '{action.issue_type}', "
            f"correct was '{correct['correct_type']}'."
        )

    return round(type_score, 2), feedback


def calculate_task2_reward(action: TriageAction, correct: dict) -> tuple[float, str]:
    """
    Task 2 (Medium) — Checks issue_type + priority.
    Each is worth 50% of total score.
    Returns: (reward_score, feedback_message)
    """
    type_score     = score_issue_type(action.issue_type, correct["correct_type"])
    priority_score = score_priority(action.priority, correct["correct_priority"])

    # Weighted: type=50%, priority=50%
    total = (type_score * 0.50) + (priority_score * 0.50)

    feedback_parts = []

    if type_score == 1.0:
        feedback_parts.append(f"Type '{action.issue_type}' correct")
    else:
        feedback_parts.append(
            f"Type wrong (said '{action.issue_type}', "
            f"correct '{correct['correct_type']}')"
        )

    if priority_score == 1.0:
        feedback_parts.append(f"Priority '{action.priority}' correct")
    elif priority_score == 0.5:
        feedback_parts.append(
            f"Priority close but off by 1 level "
            f"(said '{action.priority}', correct '{correct['correct_priority']}')"
        )
    else:
        feedback_parts.append(
            f"Priority wrong "
            f"(said '{action.priority}', correct '{correct['correct_priority']}')"
        )

    feedback = " | ".join(feedback_parts)
    return round(total, 2), feedback


def calculate_task3_reward(action: TriageAction, correct: dict) -> tuple[float, str]:
    """
    Task 3 (Hard) — Checks all 4 fields with weights.

    Weights:
        issue_type  → 25%
        priority    → 30%  (highest — priority is most critical)
        team        → 30%  (highest — routing affects who sees the issue)
        effort      → 15%

    Returns: (reward_score, feedback_message)
    """
    type_score     = score_issue_type(action.issue_type,       correct["correct_type"])
    priority_score = score_priority(action.priority,           correct["correct_priority"])
    team_score     = score_team(action.team,                   correct["correct_team"])
    effort_score   = score_effort(action.estimated_effort,     correct["correct_effort"])

    # Weighted average
    total = (
        type_score     * 0.25 +
        priority_score * 0.30 +
        team_score     * 0.30 +
        effort_score   * 0.15
    )

    # Build detailed feedback
    feedback_parts = [
        f"type={type_score:.1f}",
        f"priority={priority_score:.1f}",
        f"team={team_score:.1f}",
        f"effort={effort_score:.1f}",
    ]
    feedback = (
        f"Scores → {' | '.join(feedback_parts)} "
        f"→ Total: {total:.2f}/1.0"
    )

    return round(total, 2), feedback


def get_reward(task_id: str, action: TriageAction, correct: dict) -> tuple[float, str]:
    """
    Main entry point — routes to correct task's reward function.

    task_id: "task_1" | "task_2" | "task_3"
    action:  TriageAction submitted by the agent
    correct: dict from ISSUE_BANK with correct_* fields

    Returns: (reward float 0.0-1.0, feedback string)
    """
    if task_id == "task_1":
        return calculate_task1_reward(action, correct)
    elif task_id == "task_2":
        return calculate_task2_reward(action, correct)
    elif task_id == "task_3":
        return calculate_task3_reward(action, correct)
    else:
        raise ValueError(f"Unknown task_id: {task_id}")
