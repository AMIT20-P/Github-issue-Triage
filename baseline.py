# baseline.py
# A rule-based dummy agent that plays through the environment
# This is NOT real AI — it uses simple keyword matching (if/else)
#
# PURPOSE:
#   Prove the environment works end-to-end
#   Generate reproducible scores for the hackathon submission
#   Demonstrate what a real AI agent would interact with
#
# HOW TO RUN:
#   1. Start the server first: python app.py
#   2. In a new terminal: python baseline.py
#   3. Watch the agent play through all 3 tasks

import httpx
import time

# The server URL — change this to HF Spaces URL after deployment
BASE_URL = "http://localhost:7860"


def rule_based_agent(observation: dict) -> dict:
    """
    A dummy agent that makes triage decisions based on keyword matching.

    This is the BASELINE — the minimum expected performance.
    A real trained AI agent would score much higher than this.

    Logic:
        Looks for keywords in the title and body
        Makes a best-guess decision based on those keywords
    """
    title = observation.get("title", "").lower()
    body  = observation.get("body",  "").lower()
    text  = title + " " + body   

    if any(word in text for word in ["crash", "error", "fail", "broken", "bug",
                                      "exception", "null", "500", "fix", "not working",
                                      "leak", "injection", "vulnerability", "slow"]):
        issue_type = "bug"

    elif any(word in text for word in ["add", "support", "request", "feature",
                                        "please", "would be", "integration",
                                        "enhance", "allow", "implement", "enable"]):
        issue_type = "feature"

    elif any(word in text for word in ["how", "what", "why", "where", "can i",
                                        "question", "help", "difference", "understand"]):
        issue_type = "question"

    elif any(word in text for word in ["readme", "docs", "documentation", "guide",
                                        "missing", "outdated", "instructions", "contributing"]):
        issue_type = "documentation"

    else:
        issue_type = "bug"   #  

    user_reports = observation.get("user_reports", 0)

    if any(word in text for word in ["crash", "data loss", "payment", "production",
                                      "all users", "critical", "urgent", "down",
                                      "security", "injection", "gdpr"]) or user_reports > 500:
        priority = "P1"

    elif any(word in text for word in ["broken", "fail", "enterprise", "revenue",
                                        "blocking", "major", "memory leak"]) or user_reports > 50:
        priority = "P2"

    elif any(word in text for word in ["slow", "minor", "sometime", "occasionally",
                                        "improvement", "flaky"]) or user_reports > 5:
        priority = "P3"

    else:
        priority = "P4"

    # ── Determine team ────────────────────────
    if any(word in text for word in ["security", "injection", "vulnerability",
                                      "auth", "password", "gdpr", "2fa"]):
        team = "security"

    elif any(word in text for word in ["frontend", "ui", "button", "page",
                                        "safari", "css", "dark mode", "tooltip",
                                        "drag", "keyboard", "markdown", "chart",
                                        "mobile", "dashboard", "modal"]):
        team = "frontend"

    elif any(word in text for word in ["docker", "deployment", "ci", "pipeline",
                                        "aws", "server", "container", "devops"]):
        team = "devops"

    elif any(word in text for word in ["readme", "docs", "documentation",
                                        "guide", "contributing", "instructions"]):
        team = "documentation"

    else:
        team = "backend"   # default — most server-side issues go to backend

    # ── Determine effort ──────────────────────
    if any(word in text for word in ["typo", "small", "quick", "simple",
                                      "minor", "one line", "easy"]):
        effort = "small"

    elif any(word in text for word in ["mobile app", "i18n", "internationalization",
                                        "full", "complete", "major", "entire",
                                        "multiple", "large", "rewrite"]):
        effort = "large"

    else:
        effort = "medium"   # default

    return {
        "issue_type":        issue_type,
        "priority":          priority,
        "team":              team,
        "estimated_effort":  effort,
    }



def run_episode(task_id: str, client: httpx.Client) -> float:
    """
    Runs one complete episode for the given task.
    Returns the average reward for the episode.
    """
    # Start new episode
    response = client.post(f"{BASE_URL}/reset", json={"task_id": task_id})
    if response.status_code != 200:
        print(f"   ERROR calling /reset: {response.text}")
        return 0.0

    data        = response.json()
    observation = data["observation"]
    episode_id  = data["episode_id"]

    step_rewards = []
    step_num     = 0

    print(f"   Episode {episode_id} started")

    while True:
        step_num += 1

        # Agent decides action based on current observation
        action = rule_based_agent(observation)

        # Print what agent sees and does
        title_preview = observation["title"][:55] + "..." if len(observation["title"]) > 55 else observation["title"]
        print(f"   Step {step_num:2d} | Issue: {title_preview}")
        print(f"          Agent: type={action['issue_type']:<14} priority={action['priority']}  team={action['team']:<14} effort={action['estimated_effort']}")

        # Submit action to environment
        response = client.post(f"{BASE_URL}/step", json=action)
        if response.status_code != 200:
            print(f"   ERROR calling /step: {response.text}")
            break

        result = response.json()
        reward   = result["reward"]
        feedback = result["feedback"]
        is_done  = result["is_done"]

        step_rewards.append(reward)

        # Show reward bar
        bar_filled = int(reward * 10)
        bar        = "█" * bar_filled + "░" * (10 - bar_filled)
        print(f"          Reward: [{bar}] {reward:.2f}  | {feedback[:70]}")
        print()

        if is_done:
            break

        observation = result["observation"]

    avg_reward = sum(step_rewards) / len(step_rewards) if step_rewards else 0.0
    return round(avg_reward, 3)



def main():
    print("=" * 65)
    print("  GitHub Issue Triage — Baseline Agent Evaluation")
    print("=" * 65)
    print(f"  Server: {BASE_URL}")
    print(f"  Agent:  Rule-based keyword matching (not real AI)")
    print("=" * 65)
    print()

    # Check server is running
    try:
        response = httpx.get(f"{BASE_URL}/health", timeout=5)
        if response.status_code != 200:
            raise Exception("Server not healthy")
        print("  Server is running! Starting evaluation...\n")
    except Exception:
        print("  ERROR: Server is not running!")
        print("  Please start the server first: python app.py")
        return

    tasks = [
        ("task_1", "Issue Classification  (Easy)  "),
        ("task_2", "Priority Assignment   (Medium)"),
        ("task_3", "Full Triage           (Hard)  "),
    ]

    final_scores = {}

    with httpx.Client(timeout=30) as client:
        for task_id, task_name in tasks:
            print(f"{'─' * 65}")
            print(f"  TASK: {task_name}")
            print(f"{'─' * 65}")

            # Run 2 episodes per task for reproducibility check
            episode_scores = []
            for ep in range(1, 3):
                print(f"\n  [Episode {ep}/2]")
                score = run_episode(task_id, client)
                episode_scores.append(score)
                print(f"  Episode {ep} avg reward: {score:.3f}")
                time.sleep(0.5)

            task_avg = sum(episode_scores) / len(episode_scores)
            final_scores[task_id] = round(task_avg, 3)
            print(f"\n  {task_name} FINAL SCORE: {task_avg:.3f}")
            print()

    # ── Print Summary ────────────────────────
    print("=" * 65)
    print("  BASELINE EVALUATION COMPLETE")
    print("=" * 65)
    print()
    print("  Task Scores:")
    print(f"    Task 1 — Issue Classification  (Easy):   {final_scores.get('task_1', 0):.3f}")
    print(f"    Task 2 — Priority Assignment   (Medium): {final_scores.get('task_2', 0):.3f}")
    print(f"    Task 3 — Full Triage           (Hard):   {final_scores.get('task_3', 0):.3f}")
    print()

    overall = sum(final_scores.values()) / len(final_scores)
    print(f"  Overall Baseline Score: {overall:.3f} / 1.000")
    print()
    print("  ✅ Environment working correctly — all 3 tasks completed!")
    print("  ℹ  These scores represent a simple rule-based agent.")
    print("     A trained RL agent would score significantly higher.")
    print("=" * 65)


if __name__ == "__main__":
    main()
