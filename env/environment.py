# env/environment.py
# The CORE ENGINE of the entire project
# Implements the 3 OpenEnv API methods: reset(), step(), state()
#
# This file connects everything:
#   - issue_generator.py → provides the GitHub issues
#   - tasks.py           → provides task config + grading
#   - models.py          → provides typed return values
#
# Think of this file as the "game engine"
# It holds the state of the current episode in memory
# and responds to each reset/step/state call correctly

import uuid
from typing import Optional
from env.models import (
    IssueObservation,
    TriageAction,
    StepResult,
    EpisodeState,
    ResetResult,
)
from env.issue_generator import get_random_issue
from env.tasks import get_task, grade, is_episode_done

class GitHubTriageEnvironment:
    """
    The main environment class.
    One instance of this class = one running environment.
    It stores episode state as instance variables:
        self.episode_id     → unique ID for the current episode
        self.task_id        → which task is running (task_1/2/3)
        self.step_count     → how many steps taken in this episode
        self.total_reward   → sum of all rewards so far
        self.seen_ids       → which issues were already shown (no repeats)
        self.current_issue  → the issue currently in front of the agent
        self.is_active      → is an episode running right now?
    """

    def __init__(self):
        
        self.episode_id:    Optional[str]  = None
        self.task_id:       Optional[str]  = None
        self.step_count:    int            = 0
        self.total_reward:  float          = 0.0
        self.seen_ids:      list           = []
        self.current_issue: Optional[dict] = None
        self.is_active:     bool           = False

    
    # reset() — Start a brand new episode

    def reset(self, task_id: str = "task_1") -> ResetResult:
        """
        Starts a fresh episode for the given task.

        What happens inside:
            1. Generate a new unique episode ID
            2. Clear all previous episode data (step count, rewards, seen issues)
            3. Pick the first random GitHub issue for this task
            4. Store it as current_issue
            5. Return a ResetResult with the first observation

        Called by: Agent at the start of every new training episode
        Returns: ResetResult (contains first IssueObservation + episode info)
        """

        # Validate task_id before starting
        task_config = get_task(task_id)  # raises ValueError if invalid

        # Assign a fresh unique episode ID (like a game session ID)
        self.episode_id   = f"ep_{uuid.uuid4().hex[:8]}"
        self.task_id      = task_id
        self.step_count   = 0
        self.total_reward = 0.0
        self.seen_ids     = []
        self.is_active    = True

        # Pick the first issue for this episode
        issue = get_random_issue(task_id=task_id, seen_ids=self.seen_ids)
        self.current_issue = issue
        self.seen_ids.append(issue["id"])

        # Build the observation (what the agent sees)
        observation = self._build_observation(issue)

        return ResetResult(
            observation = observation,
            episode_id  = self.episode_id,
            task_id     = task_id,
            message     = (
                f"New episode started! Task: {task_config['name']} "
                f"({task_config['difficulty']}). "
                f"You have {task_config['max_steps']} issues to triage."
            ),
        )

    
    # step()—Agent submits an action

    def step(self, action: TriageAction) -> StepResult:
        """
        Processes the agent's triage decision for the current issue.

        What happens inside:
            1. Check that an episode is active (reset must be called first)
            2. Increment step count
            3. Grade the agent's action against the correct answer
            4. Add reward to running total
            5. Check if episode is done (max steps reached)
            6. If not done: pick next issue and return it
            7. If done: return None as next observation

        Called by: Agent after viewing the current observation
        Returns: StepResult (reward, feedback, next observation or None, is_done)
        """

        # Safety check — must call reset() before step()
        if not self.is_active or self.current_issue is None:
            raise RuntimeError(
                "No active episode. Call reset() before step()."
            )

        self.step_count += 1

        # Grade the agent's answer using tasks.grade()
        # grade() internally calls rewards.py and returns (score, feedback)
        reward, feedback = grade(
            task_id       = self.task_id,
            action        = action,
            correct_issue = self.current_issue
        )

        self.total_reward = round(self.total_reward + reward, 4)

        done = is_episode_done(self.task_id, self.step_count)

        if done:
            self.is_active = False
            return StepResult(
                observation = None,
                reward      = round(reward, 4),
                is_done     = True,
                feedback    = feedback + f" | Episode complete! Total reward: {self.total_reward}",
                step_number = self.step_count,
            )

        # Episode continues — pick next issue (not one already seen)
        next_issue = get_random_issue(task_id=self.task_id, seen_ids=self.seen_ids)
        self.current_issue = next_issue
        self.seen_ids.append(next_issue["id"])

        # Build observation for the next issue
        next_observation = self._build_observation(next_issue)

        return StepResult(
            observation = next_observation,
            reward      = round(reward, 4),
            is_done     = False,
            feedback    = feedback,
            step_number = self.step_count,
        )

    #state()—Get current episode metadata

    def state(self) -> EpisodeState:
        """
        Returns a snapshot of the current episode's state.
        Does NOT advance the episode — just provides information.

        Called by: Agent anytime to check progress/metadata
        Returns: EpisodeState (episode_id, step_count, total_reward, etc.)

        Useful for:
            - Checking how many steps remain
            - Logging current score
            - Debugging agent behavior
        """

        # Get max_steps from task config (or 0 if no episode active)
        max_steps = 0
        if self.task_id:
            task_config = get_task(self.task_id)
            max_steps   = task_config["max_steps"]

        return EpisodeState(
            episode_id   = self.episode_id   or "none",
            current_task = self.task_id      or "none",
            step_count   = self.step_count,
            max_steps    = max_steps,
            total_reward = self.total_reward,
            is_active    = self.is_active,
        )

    #Helper:Build IssueObservation from raw dict

    def _build_observation(self, issue: dict) -> IssueObservation:
        """
        Private helper method.
        Converts a raw issue dict from ISSUE_BANK
        into a typed IssueObservation object.

        The underscore prefix (_) means: internal use only.
        Agents never call this directly — it's used by reset() and step() internally.

        Why separate? Because both reset() and step() need to create observations.
        Instead of duplicating code, we put it here once and call it from both places.
        """
        return IssueObservation(
            issue_id          = issue["id"],
            title             = issue["title"],
            body              = issue["body"],
            repo              = issue["repo"],
            author_type       = issue["author_type"],
            user_reports      = issue["user_reports"],
            existing_labels   = issue.get("existing_labels", []),
            open_issues_count = issue["open_issues_count"],
            task_id           = self.task_id,
            step_number       = self.step_count,
        )
