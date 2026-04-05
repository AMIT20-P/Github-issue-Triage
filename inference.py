"""
Inference Script — GitHub Issue Triage OpenEnv
===================================
LLM-based agent that triages GitHub issues using the OpenEnv environment.

MANDATORY environment variables:
    API_BASE_URL      The API endpoint for the LLM.
    MODEL_NAME        The model identifier to use for inference.
    HF_TOKEN          Your Hugging Face / API key.
    ENV_BASE_URL      The OpenEnv environment URL (our HF Space).
    TASK_NAME         Task to run: task_1 | task_2 | task_3 (default: task_3)

Defaults reflect the active inference setup:
    API_BASE_URL = os.getenv("API_BASE_URL", "https://router.huggingface.co/v1")
    MODEL_NAME   = os.getenv("MODEL_NAME",   "Qwen/Qwen2.5-72B-Instruct")
"""

import json
import os
import textwrap
from typing import List, Optional

import httpx
from openai import OpenAI

# ─────────────────────────────────────────────
# LLM Configuration (MANDATORY env vars)
# ─────────────────────────────────────────────
API_BASE_URL = os.getenv("API_BASE_URL", "https://router.huggingface.co/v1")
MODEL_NAME   = os.getenv("MODEL_NAME",   "Qwen/Qwen2.5-72B-Instruct")
API_KEY      = os.getenv("HF_TOKEN") or os.getenv("API_KEY")

# ─────────────────────────────────────────────
# OpenEnv Environment Configuration
# ─────────────────────────────────────────────
ENV_BASE_URL = os.getenv("ENV_BASE_URL", "https://amitsj-github-issue-triage.hf.space")
TASK_NAME    = os.getenv("TASK_NAME",    "task_3")
BENCHMARK    = "github-issue-triage"
MAX_STEPS    = 6
SUCCESS_SCORE_THRESHOLD = 0.5

# ─────────────────────────────────────────────
# LLM System Prompt
# ─────────────────────────────────────────────
SYSTEM_PROMPT = textwrap.dedent("""
    You are an expert GitHub issue triager for open-source projects.
    Analyze the GitHub issue carefully and respond with a single JSON object.
    No markdown, no explanation — ONLY valid JSON.

    Required JSON format:
    {
      "issue_type":       "bug" | "feature" | "question" | "documentation" | "duplicate",
      "priority":         "P1" | "P2" | "P3" | "P4",
      "team":             "backend" | "frontend" | "devops" | "documentation" | "security" | "support",
      "estimated_effort": "small" | "medium" | "large"
    }

    Priority guidelines:
    - P1 (Critical): crashes, data loss, security, >500 affected users
    - P2 (High):     major feature broken, enterprise impact, >50 users
    - P3 (Medium):   degraded feature, workaround exists
    - P4 (Low):      minor, cosmetic, nice-to-have, typos
""").strip()


# ─────────────────────────────────────────────
# STDOUT Logging (required exact format)
# ─────────────────────────────────────────────
def log_start(task: str, env: str, model: str) -> None:
    print(f"[START] task={task} env={env} model={model}", flush=True)


def log_step(step: int, action: str, reward: float, done: bool, error: Optional[str]) -> None:
    error_val = error if error else "null"
    done_val  = str(done).lower()
    print(
        f"[STEP] step={step} action={action} reward={reward:.2f} done={done_val} error={error_val}",
        flush=True,
    )


def log_end(success: bool, steps: int, score: float, rewards: List[float]) -> None:
    rewards_str = ",".join(f"{r:.2f}" for r in rewards)
    print(
        f"[END] success={str(success).lower()} steps={steps} score={score:.3f} rewards={rewards_str}",
        flush=True,
    )


# ─────────────────────────────────────────────
# LLM Agent
# ─────────────────────────────────────────────
def get_triage_decision(client: OpenAI, observation: dict) -> dict:
    """Call the LLM to make a triage decision for the given GitHub issue."""
    user_prompt = textwrap.dedent(f"""
        Triage this GitHub issue:

        Title:       {observation.get('title', '')}
        Repository:  {observation.get('repo', '')}
        Author type: {observation.get('author_type', '')}
        User reports:{observation.get('user_reports', 0)}
        Labels:      {observation.get('existing_labels', [])}

        Body:
        {str(observation.get('body', ''))[:800]}

        Respond with ONLY a JSON object. No markdown, no extra text.
    """).strip()

    try:
        completion = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user",   "content": user_prompt},
            ],
            temperature=0.1,
            max_tokens=150,
            stream=False,
        )
        text = (completion.choices[0].message.content or "").strip()
        # Strip markdown code fences if model wraps response
        if "```" in text:
            text = text.split("```")[1]
            if text.startswith("json"):
                text = text[4:]
        return json.loads(text.strip())
    except Exception as exc:
        print(f"[DEBUG] LLM call failed: {exc}", flush=True)
        return _rule_based_fallback(observation)


def _rule_based_fallback(observation: dict) -> dict:
    """Keyword-based fallback in case the LLM call fails."""
    text = (observation.get("title", "") + " " + observation.get("body", "")).lower()
    user_reports = observation.get("user_reports", 0)

    issue_type = (
        "bug"           if any(w in text for w in ["crash","error","fail","broken","exception","500"])
        else "feature"  if any(w in text for w in ["add","support","request","feature","new"])
        else "question" if any(w in text for w in ["how","why","what","help"])
        else "documentation" if any(w in text for w in ["docs","readme","typo","guide"])
        else "bug"
    )
    priority = (
        "P1" if any(w in text for w in ["crash","security","data loss","injection"]) or user_reports > 500
        else "P2" if user_reports > 50
        else "P3" if user_reports > 5
        else "P4"
    )
    team = (
        "security"      if any(w in text for w in ["security","vulnerability","injection","xss"])
        else "frontend" if any(w in text for w in ["ui","button","css","dark mode","design"])
        else "devops"   if any(w in text for w in ["docker","aws","ci","pipeline","deploy"])
        else "documentation" if any(w in text for w in ["docs","readme","guide"])
        else "backend"
    )
    effort = (
        "small"  if any(w in text for w in ["typo","minor","quick","one line"])
        else "large" if any(w in text for w in ["rewrite","architecture","major","entire"])
        else "medium"
    )
    return {"issue_type": issue_type, "priority": priority, "team": team, "estimated_effort": effort}


# ─────────────────────────────────────────────
# Main Episode Loop
# ─────────────────────────────────────────────
def main() -> None:
    client = OpenAI(base_url=API_BASE_URL, api_key=API_KEY)

    rewards:     List[float] = []
    steps_taken: int         = 0
    score:       float       = 0.0
    success:     bool        = False

    log_start(task=TASK_NAME, env=BENCHMARK, model=MODEL_NAME)

    try:
        with httpx.Client(base_url=ENV_BASE_URL, timeout=30.0) as http:
            # ── Reset environment (OpenEnv.reset()) ──
            reset_resp = http.post("/reset", json={"task_id": TASK_NAME})
            reset_resp.raise_for_status()
            data        = reset_resp.json()
            observation = data["observation"]

            for step in range(1, MAX_STEPS + 1):
                # ── Get LLM decision ──
                action     = get_triage_decision(client, observation)
                action_str = json.dumps(action, separators=(',', ':'))

                # ── Submit action (OpenEnv.step()) ──
                step_resp = http.post("/step", json=action)
                step_resp.raise_for_status()
                result = step_resp.json()

                reward = float(result.get("reward",  0.0))
                done   = bool( result.get("is_done", False))
                error  = None

                rewards.append(reward)
                steps_taken = step

                log_step(step=step, action=action_str, reward=reward, done=done, error=error)

                if done:
                    break
                observation = result.get("observation", observation)

        score   = sum(rewards) / len(rewards) if rewards else 0.0
        score   = min(max(score, 0.0), 1.0)
        success = score >= SUCCESS_SCORE_THRESHOLD

    except Exception as exc:
        print(f"[DEBUG] Episode error: {exc}", flush=True)
    finally:
        log_end(success=success, steps=steps_taken, score=score, rewards=rewards)


if __name__ == "__main__":
    main()
