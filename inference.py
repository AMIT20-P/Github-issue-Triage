"""
inference.py — Baseline inference script for the GitHub Issue Triage OpenEnv

This script runs a rule-based agent through the environment and returns
reproducible baseline scores. Required by the OpenEnv specification.

Usage:
    python inference.py
    (Server must be running: python app.py)
"""

import httpx
import sys

BASE_URL = "http://localhost:7860"


def rule_based_agent(observation: dict) -> dict:
    """Simple keyword-matching agent for baseline inference."""
    title = observation.get("title", "").lower()
    body  = observation.get("body",  "").lower()
    text  = title + " " + body

    # issue_type
    if any(w in text for w in ["crash","error","fail","broken","exception","null","500","fix","not working","leak","injection","vulnerability","slow"]):
        issue_type = "bug"
    elif any(w in text for w in ["add","support","request","feature","allow","enable","new","implement","would like","could you"]):
        issue_type = "feature"
    elif any(w in text for w in ["how","what","why","question","help","understand","can i","is it possible"]):
        issue_type = "question"
    elif any(w in text for w in ["readme","docs","documentation","example","tutorial","guide","typo"]):
        issue_type = "documentation"
    else:
        issue_type = "bug"

    # priority
    user_reports = observation.get("user_reports", 0)
    if any(w in text for w in ["crash","data loss","payment","production","revenue","security","cannot login"]) or user_reports > 500:
        priority = "P1"
    elif any(w in text for w in ["enterprise","blocking","revenue","high impact"]) or user_reports > 50:
        priority = "P2"
    elif any(w in text for w in ["slow","occasionally","sometimes","improvement"]) or user_reports > 5:
        priority = "P3"
    else:
        priority = "P4"

    # team
    if any(w in text for w in ["security","injection","vulnerability","auth","xss","csrf"]):
        team = "security"
    elif any(w in text for w in ["button","ui","dark mode","safari","firefox","css","layout","frontend","design","color"]):
        team = "frontend"
    elif any(w in text for w in ["docker","deployment","ci","aws","kubernetes","pipeline","devops","infra"]):
        team = "devops"
    elif any(w in text for w in ["readme","docs","documentation","guide","tutorial"]):
        team = "documentation"
    else:
        team = "backend"

    # effort
    if any(w in text for w in ["typo","quick","simple","minor","small","one line"]):
        effort = "small"
    elif any(w in text for w in ["mobile app","i18n","rewrite","entire","large","major","architecture"]):
        effort = "large"
    else:
        effort = "medium"

    return {
        "issue_type":       issue_type,
        "priority":         priority,
        "team":             team,
        "estimated_effort": effort,
    }


def run_inference(task_id: str = "task_1", base_url: str = BASE_URL) -> dict:
    """
    Run one full episode for the given task.
    Returns a dict with task_id and average_reward.
    """
    with httpx.Client(base_url=base_url, timeout=30.0) as client:
        # Start episode
        reset_resp = client.post("/reset", json={"task_id": task_id})
        reset_resp.raise_for_status()
        data = reset_resp.json()

        observation  = data["observation"]
        step_rewards = []

        while True:
            action = rule_based_agent(observation)
            step_resp = client.post("/step", json=action)
            step_resp.raise_for_status()
            result = step_resp.json()

            step_rewards.append(result["reward"])

            if result["is_done"]:
                break
            observation = result["observation"]

    avg = round(sum(step_rewards) / len(step_rewards), 4) if step_rewards else 0.0
    return {"task_id": task_id, "average_reward": avg, "steps": len(step_rewards)}


def main():
    base_url = sys.argv[1] if len(sys.argv) > 1 else BASE_URL

    print("=" * 55)
    print("  GitHub Issue Triage — Inference Script")
    print(f"  Server: {base_url}")
    print("=" * 55)

    results = []
    for task_id in ["task_1", "task_2", "task_3"]:
        r = run_inference(task_id, base_url)
        results.append(r)
        print(f"  {task_id}: avg_reward = {r['average_reward']:.4f}  ({r['steps']} steps)")

    overall = round(sum(r["average_reward"] for r in results) / len(results), 4)
    print("=" * 55)
    print(f"  Overall Baseline Score: {overall:.4f} / 1.0000")
    print("=" * 55)
    return results


if __name__ == "__main__":
    main()
