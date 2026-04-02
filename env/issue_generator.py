# env/issue_generator.py
# A bank of 50+ realistic fake GitHub issues
# Each issue has the CORRECT triage answer stored alongside it
# The grader compares agent's answer with the correct answer

import random
from typing import List, Dict

ISSUE_BANK: List[Dict] = [

    {
        "id": "issue_001",
        "title": "App crashes immediately on launch after v3.2 update",
        "body": (
            "## Bug Report\n"
            "**What happened:** App crashes on startup — users cannot open it at all.\n\n"
            "**Steps to reproduce:**\n"
            "1. Install latest update v3.2\n"
            "2. Open the app\n"
            "3. App closes instantly\n\n"
            "**Error:** `NullPointerException at MainActivity.onCreate`\n"
            "**Affected users:** 1,200 crash reports in last 2 hours\n"
            "**Platform:** Android 13, 14"
        ),
        "repo": "mobile-app",
        "author_type": "regular",
        "user_reports": 1200,
        "existing_labels": [],
        "open_issues_count": 340,
        "correct_type": "bug",
        "correct_priority": "P1",
        "correct_team": "backend",
        "correct_effort": "small"
    },

    {
        "id": "issue_002",
        "title": "Payment processing failing for all users — checkout broken",
        "body": (
            "## Critical Bug\n"
            "All payments are failing since 3:00 AM IST.\n\n"
            "**Error returned:** `Payment gateway timeout after 30s`\n"
            "**Impact:** 100% of checkout attempts failing\n"
            "**Revenue loss:** Estimated Rs 4 lakh/hour\n"
            "**Stripe dashboard:** Shows no successful transactions since 3 AM"
        ),
        "repo": "ecommerce-platform",
        "author_type": "maintainer",
        "user_reports": 890,
        "existing_labels": ["critical"],
        "open_issues_count": 120,
        "correct_type": "bug",
        "correct_priority": "P1",
        "correct_team": "backend",
        "correct_effort": "small"
    },

    {
        "id": "issue_003",
        "title": "User data deleted after password reset flow",
        "body": (
            "## Data Loss Bug — URGENT\n"
            "When a user resets their password, all their saved data "
            "(preferences, history, files) is being wiped.\n\n"
            "**Reproduction rate:** 100% reproducible\n"
            "**Affected:** Any user who uses 'Forgot Password'\n"
            "**Severity:** User data permanently lost\n\n"
            "This has been going on since the auth refactor in PR #892."
        ),
        "repo": "user-auth-service",
        "author_type": "regular",
        "user_reports": 340,
        "existing_labels": [],
        "open_issues_count": 210,
        "correct_type": "bug",
        "correct_priority": "P1",
        "correct_team": "backend",
        "correct_effort": "medium"
    },

    {
        "id": "issue_004",
        "title": "Login page shows blank white screen on Safari",
        "body": (
            "## Bug Report\n"
            "Login page is completely blank on Safari 17.\n\n"
            "**Steps:**\n"
            "1. Open Safari 17\n"
            "2. Go to app.example.com/login\n"
            "3. White blank screen — nothing loads\n\n"
            "**Works on:** Chrome, Firefox\n"
            "**Doesn't work:** Safari 17 on macOS Sonoma\n"
            "**Console error:** `TypeError: Cannot read properties of undefined`"
        ),
        "repo": "web-frontend",
        "author_type": "regular",
        "user_reports": 78,
        "existing_labels": [],
        "open_issues_count": 450,
        "correct_type": "bug",
        "correct_priority": "P2",
        "correct_team": "frontend",
        "correct_effort": "small"
    },

    {
        "id": "issue_005",
        "title": "File upload silently fails for files larger than 50MB",
        "body": (
            "## Bug Report\n"
            "When uploading files over 50MB, the upload appears to succeed "
            "(progress bar reaches 100%) but the file is never saved.\n\n"
            "**Steps:**\n"
            "1. Go to Upload section\n"
            "2. Select any file > 50MB\n"
            "3. Upload completes — no error shown\n"
            "4. File not visible in file manager\n\n"
            "**Note:** Files under 50MB upload fine.\n"
            "**Affected users:** 23 reports this week"
        ),
        "repo": "file-manager",
        "author_type": "regular",
        "user_reports": 23,
        "existing_labels": [],
        "open_issues_count": 180,
        "correct_type": "bug",
        "correct_priority": "P2",
        "correct_team": "backend",
        "correct_effort": "medium"
    },

    {
        "id": "issue_006",
        "title": "Dark mode toggle resets to light mode after page refresh",
        "body": (
            "## Bug Report\n"
            "When I switch to dark mode and then refresh the page, "
            "it goes back to light mode. The preference is not being saved.\n\n"
            "**Steps:**\n"
            "1. Go to Settings > Appearance\n"
            "2. Enable Dark Mode\n"
            "3. Refresh the page\n"
            "4. Light mode is back\n\n"
            "Expected: dark mode preference persists across sessions."
        ),
        "repo": "web-frontend",
        "author_type": "regular",
        "user_reports": 12,
        "existing_labels": [],
        "open_issues_count": 450,
        "correct_type": "bug",
        "correct_priority": "P3",
        "correct_team": "frontend",
        "correct_effort": "small"
    },

    {
        "id": "issue_007",
        "title": "Tooltip text is cut off on mobile screens",
        "body": (
            "## Bug Report\n"
            "The tooltip that appears on hover over the info icon is "
            "getting clipped on screens smaller than 375px width.\n\n"
            "You can see the tooltip is being cut by the screen edge — "
            "the right portion of the text is not visible.\n\n"
            "Tested on: iPhone SE (375px), Galaxy S21\n"
            "Works fine on desktop."
        ),
        "repo": "web-frontend",
        "author_type": "first-time-contributor",
        "user_reports": 3,
        "existing_labels": [],
        "open_issues_count": 450,
        "correct_type": "bug",
        "correct_priority": "P4",
        "correct_team": "frontend",
        "correct_effort": "small"
    },

    {
        "id": "issue_008",
        "title": "Memory leak in WebSocket connection handler",
        "body": (
            "## Bug Report\n"
            "The WebSocket handler does not clean up listeners when "
            "connection is closed. Memory usage grows ~50MB every hour "
            "in long-running sessions.\n\n"
            "**Root cause identified:** `connectionPool.addListener()` "
            "is called but never removed in `onDisconnect` handler.\n\n"
            "Found during load testing. In prod, servers restart every "
            "8 hours due to OOM (Out Of Memory) errors."
        ),
        "repo": "realtime-server",
        "author_type": "maintainer",
        "user_reports": 1,
        "existing_labels": ["performance"],
        "open_issues_count": 89,
        "correct_type": "bug",
        "correct_priority": "P2",
        "correct_team": "backend",
        "correct_effort": "medium"
    },

    {
        "id": "issue_009",
        "title": "API returns 500 error when date field is null",
        "body": (
            "## Bug Report\n"
            "`GET /api/v2/events` returns a 500 Internal Server Error "
            "when the event's `end_date` field is null.\n\n"
            "**Request:** `GET /api/v2/events?id=1023`\n"
            "**Response:** `500 Internal Server Error`\n"
            "**Error in logs:** `AttributeError: 'NoneType' has no attribute 'strftime'`\n\n"
            "Events with null end_date (ongoing events) should be supported."
        ),
        "repo": "events-api",
        "author_type": "regular",
        "user_reports": 8,
        "existing_labels": [],
        "open_issues_count": 67,
        "correct_type": "bug",
        "correct_priority": "P2",
        "correct_team": "backend",
        "correct_effort": "small"
    },

    {
        "id": "issue_010",
        "title": "SQL injection vulnerability in search endpoint",
        "body": (
            "## Security Bug\n"
            "The `/api/search?q=` endpoint is vulnerable to SQL injection.\n\n"
            "**Proof of concept:**\n"
            "`GET /api/search?q=' OR '1'='1`\n"
            "Returns all records from the database.\n\n"
            "**Impact:** Full database read access possible for any user.\n"
            "Please treat this as critical and patch immediately.\n\n"
            "Reported via security disclosure program."
        ),
        "repo": "api-gateway",
        "author_type": "regular",
        "user_reports": 1,
        "existing_labels": ["security"],
        "open_issues_count": 200,
        "correct_type": "bug",
        "correct_priority": "P1",
        "correct_team": "security",
        "correct_effort": "small"
    },

    # ── FEATURES ─────────────────────────────────────────────

    {
        "id": "issue_011",
        "title": "Add dark mode support to the dashboard",
        "body": (
            "## Feature Request\n"
            "It would be great to have a dark mode option available in Settings.\n\n"
            "Many users have been requesting this — see related issues: "
            "#234, #301, #445, #512.\n\n"
            "Dark mode helps reduce eye strain during night-time usage "
            "and is standard on modern apps.\n\n"
            "Expected: A toggle in Settings > Appearance that switches "
            "between light and dark themes."
        ),
        "repo": "dashboard-ui",
        "author_type": "regular",
        "user_reports": 67,
        "existing_labels": ["enhancement"],
        "open_issues_count": 340,
        "correct_type": "feature",
        "correct_priority": "P3",
        "correct_team": "frontend",
        "correct_effort": "medium"
    },

    {
        "id": "issue_012",
        "title": "Add two-factor authentication (2FA) support",
        "body": (
            "## Feature Request\n"
            "Please add 2FA support using TOTP (Google Authenticator / Authy).\n\n"
            "**Why:** Enterprise customers require 2FA for compliance "
            "(SOC2, ISO27001). We are losing deals because of this missing feature.\n\n"
            "**Expected behavior:**\n"
            "- User enables 2FA in Account Security settings\n"
            "- On login, prompt for 6-digit TOTP code\n"
            "- Backup codes provided\n\n"
            "This is blocking 3 enterprise signups."
        ),
        "repo": "user-auth-service",
        "author_type": "maintainer",
        "user_reports": 45,
        "existing_labels": ["enhancement", "security"],
        "open_issues_count": 210,
        "correct_type": "feature",
        "correct_priority": "P2",
        "correct_team": "backend",
        "correct_effort": "large"
    },

    {
        "id": "issue_013",
        "title": "Export data to CSV/Excel from dashboard",
        "body": (
            "## Feature Request\n"
            "Users need to export their data (reports, analytics, lists) "
            "to CSV or Excel format for offline analysis.\n\n"
            "Currently there is no way to get raw data out of the dashboard.\n\n"
            "**Requested by:** 12 enterprise customers in support tickets\n"
            "**Expected:** Download button on each table/chart that exports data."
        ),
        "repo": "dashboard-ui",
        "author_type": "regular",
        "user_reports": 38,
        "existing_labels": ["enhancement"],
        "open_issues_count": 340,
        "correct_type": "feature",
        "correct_priority": "P3",
        "correct_team": "frontend",
        "correct_effort": "medium"
    },

    {
        "id": "issue_014",
        "title": "Add keyboard shortcuts for common actions",
        "body": (
            "## Feature Request\n"
            "Power users would benefit from keyboard shortcuts for:\n"
            "- Ctrl+N: New item\n"
            "- Ctrl+S: Save\n"
            "- Ctrl+F: Search\n"
            "- Ctrl+/: Open shortcuts help\n\n"
            "This would significantly improve productivity for frequent users."
        ),
        "repo": "web-frontend",
        "author_type": "regular",
        "user_reports": 14,
        "existing_labels": [],
        "open_issues_count": 450,
        "correct_type": "feature",
        "correct_priority": "P4",
        "correct_team": "frontend",
        "correct_effort": "medium"
    },

    {
        "id": "issue_015",
        "title": "Support bulk operations — delete/archive multiple items at once",
        "body": (
            "## Feature Request\n"
            "Currently users have to delete/archive items one by one.\n\n"
            "Please add:\n"
            "- Checkbox to select multiple items\n"
            "- 'Select All' option\n"
            "- Bulk action dropdown: Delete, Archive, Export\n\n"
            "This is a very common request in our support channel. "
            "Users managing large datasets find the current UX very tedious."
        ),
        "repo": "dashboard-ui",
        "author_type": "regular",
        "user_reports": 29,
        "existing_labels": ["enhancement"],
        "open_issues_count": 340,
        "correct_type": "feature",
        "correct_priority": "P3",
        "correct_team": "frontend",
        "correct_effort": "medium"
    },

    {
        "id": "issue_016",
        "title": "Add email digest — weekly summary of activity",
        "body": (
            "## Feature Request\n"
            "It would be useful to receive a weekly email digest summarizing:\n"
            "- New items created\n"
            "- Items completed\n"
            "- Team activity highlights\n\n"
            "User should be able to opt in/out from Notification Settings.\n"
            "Frequency: daily or weekly."
        ),
        "repo": "notifications-service",
        "author_type": "regular",
        "user_reports": 19,
        "existing_labels": [],
        "open_issues_count": 78,
        "correct_type": "feature",
        "correct_priority": "P4",
        "correct_team": "backend",
        "correct_effort": "medium"
    },

    {
        "id": "issue_017",
        "title": "API rate limiting — protect endpoints from abuse",
        "body": (
            "## Feature Request / Security\n"
            "Our public API currently has no rate limiting.\n\n"
            "We have seen abuse with some IPs making 10,000+ requests/minute, "
            "causing degraded performance for all users.\n\n"
            "**Requested:** Implement rate limiting:\n"
            "- 100 requests/minute for free tier\n"
            "- 1000 requests/minute for paid tier\n"
            "- Return 429 Too Many Requests with Retry-After header"
        ),
        "repo": "api-gateway",
        "author_type": "maintainer",
        "user_reports": 5,
        "existing_labels": ["security", "enhancement"],
        "open_issues_count": 200,
        "correct_type": "feature",
        "correct_priority": "P2",
        "correct_team": "backend",
        "correct_effort": "medium"
    },

    {
        "id": "issue_018",
        "title": "Add Slack integration for notifications",
        "body": (
            "## Feature Request\n"
            "Many teams use Slack and would like to receive notifications "
            "directly in their Slack channels.\n\n"
            "**Requested integration:**\n"
            "- Connect Slack workspace in Settings > Integrations\n"
            "- Choose channel for notifications\n"
            "- Notify on: new item, comment, status change, deadline\n\n"
            "This is #1 most requested integration from our survey."
        ),
        "repo": "integrations-service",
        "author_type": "regular",
        "user_reports": 88,
        "existing_labels": ["enhancement"],
        "open_issues_count": 145,
        "correct_type": "feature",
        "correct_priority": "P2",
        "correct_team": "backend",
        "correct_effort": "large"
    },

    {
        "id": "issue_019",
        "title": "Add drag and drop support for file uploads",
        "body": (
            "## Feature Request\n"
            "Currently users have to click 'Browse' to upload files.\n\n"
            "Please add drag-and-drop upload support so users can "
            "drag files directly from their desktop into the browser.\n\n"
            "Expected: Drag file onto any upload zone to trigger upload."
        ),
        "repo": "web-frontend",
        "author_type": "first-time-contributor",
        "user_reports": 22,
        "existing_labels": [],
        "open_issues_count": 450,
        "correct_type": "feature",
        "correct_priority": "P3",
        "correct_team": "frontend",
        "correct_effort": "small"
    },

    {
        "id": "issue_020",
        "title": "Support markdown formatting in comments",
        "body": (
            "## Feature Request\n"
            "Comments currently only support plain text.\n\n"
            "Please add markdown support so users can:\n"
            "- **Bold** and *italic* text\n"
            "- Code blocks with syntax highlighting\n"
            "- Bullet lists\n"
            "- Links\n\n"
            "This is especially important for technical teams sharing code snippets."
        ),
        "repo": "collaboration-service",
        "author_type": "regular",
        "user_reports": 41,
        "existing_labels": [],
        "open_issues_count": 190,
        "correct_type": "feature",
        "correct_priority": "P3",
        "correct_team": "frontend",
        "correct_effort": "medium"
    },

    # ── QUESTIONS ────────────────────────────────────────────

    {
        "id": "issue_021",
        "title": "How do I reset my password?",
        "body": (
            "I forgot my password.\n\n"
            "I clicked 'Forgot Password' and it says it sent an email "
            "but I haven't received anything in 30 minutes.\n"
            "I also checked my spam folder.\n\n"
            "What should I do?"
        ),
        "repo": "user-auth-service",
        "author_type": "first-time-contributor",
        "user_reports": 1,
        "existing_labels": [],
        "open_issues_count": 210,
        "correct_type": "question",
        "correct_priority": "P4",
        "correct_team": "support",
        "correct_effort": "small"
    },

    {
        "id": "issue_022",
        "title": "What is the rate limit for the API?",
        "body": (
            "Hi,\n\n"
            "I'm building an integration and need to know:\n"
            "1. What is the rate limit for API calls?\n"
            "2. Is it per minute or per hour?\n"
            "3. What headers are returned for rate limit info?\n\n"
            "I couldn't find this in the docs. Thanks!"
        ),
        "repo": "api-gateway",
        "author_type": "regular",
        "user_reports": 1,
        "existing_labels": [],
        "open_issues_count": 200,
        "correct_type": "question",
        "correct_priority": "P4",
        "correct_team": "support",
        "correct_effort": "small"
    },

    {
        "id": "issue_023",
        "title": "How to migrate data from v1 to v2?",
        "body": (
            "We are upgrading from v1 to v2 and need guidance on data migration.\n\n"
            "Specifically:\n"
            "- Is there a migration script provided?\n"
            "- Will v1 data format be auto-converted?\n"
            "- Is there a rollback plan if migration fails?\n\n"
            "We have 50GB of production data so need to be careful."
        ),
        "repo": "database-core",
        "author_type": "regular",
        "user_reports": 6,
        "existing_labels": [],
        "open_issues_count": 95,
        "correct_type": "question",
        "correct_priority": "P3",
        "correct_team": "documentation",
        "correct_effort": "small"
    },

    {
        "id": "issue_024",
        "title": "Can I self-host this project?",
        "body": (
            "Hello,\n\n"
            "I want to self-host this tool on my company's private server.\n\n"
            "Is self-hosting supported? If yes:\n"
            "- Is there a Docker image available?\n"
            "- What are the minimum server requirements?\n"
            "- Is the license compatible with commercial self-hosting?\n\n"
            "Thank you"
        ),
        "repo": "platform-core",
        "author_type": "first-time-contributor",
        "user_reports": 1,
        "existing_labels": [],
        "open_issues_count": 312,
        "correct_type": "question",
        "correct_priority": "P4",
        "correct_team": "support",
        "correct_effort": "small"
    },

    {
        "id": "issue_025",
        "title": "What is the difference between workspaces and projects?",
        "body": (
            "Hi,\n\n"
            "I'm a new user and I'm confused about the difference "
            "between Workspaces and Projects in the UI.\n\n"
            "When should I create a Workspace vs a Project?\n"
            "Can Projects exist across multiple Workspaces?\n\n"
            "The documentation doesn't clearly explain this."
        ),
        "repo": "platform-core",
        "author_type": "first-time-contributor",
        "user_reports": 1,
        "existing_labels": [],
        "open_issues_count": 312,
        "correct_type": "question",
        "correct_priority": "P4",
        "correct_team": "documentation",
        "correct_effort": "small"
    },

    # ── DOCUMENTATION ─────────────────────────────────────────

    {
        "id": "issue_026",
        "title": "README missing installation steps for Windows",
        "body": (
            "## Documentation Issue\n"
            "The README only has installation instructions for Linux and macOS.\n\n"
            "Windows users (a significant portion of contributors) have no guide.\n\n"
            "Please add:\n"
            "- Prerequisites for Windows\n"
            "- Clone and setup steps\n"
            "- How to run dev server on Windows\n"
            "- Common Windows-specific issues"
        ),
        "repo": "platform-core",
        "author_type": "first-time-contributor",
        "user_reports": 9,
        "existing_labels": ["documentation"],
        "open_issues_count": 312,
        "correct_type": "documentation",
        "correct_priority": "P3",
        "correct_team": "documentation",
        "correct_effort": "small"
    },

    {
        "id": "issue_027",
        "title": "API docs missing response schema for /users endpoint",
        "body": (
            "## Documentation Bug\n"
            "The API documentation for `GET /api/users` is missing:\n"
            "- Response schema / field descriptions\n"
            "- Example response JSON\n"
            "- Error codes and what they mean\n\n"
            "Without this, integrators have to guess the response format "
            "by trial and error."
        ),
        "repo": "api-gateway",
        "author_type": "regular",
        "user_reports": 7,
        "existing_labels": ["documentation"],
        "open_issues_count": 200,
        "correct_type": "documentation",
        "correct_priority": "P3",
        "correct_team": "documentation",
        "correct_effort": "small"
    },

    {
        "id": "issue_028",
        "title": "Contributing guide is outdated — references old branch names",
        "body": (
            "## Documentation Issue\n"
            "The CONTRIBUTING.md still references the old branch `master` "
            "but the project now uses `main`.\n\n"
            "Also the PR process steps mentioned are outdated — "
            "the project now uses linear history (rebase, not merge commits).\n\n"
            "New contributors are confused and submitting PRs incorrectly."
        ),
        "repo": "platform-core",
        "author_type": "regular",
        "user_reports": 4,
        "existing_labels": ["documentation"],
        "open_issues_count": 312,
        "correct_type": "documentation",
        "correct_priority": "P4",
        "correct_team": "documentation",
        "correct_effort": "small"
    },

    # ── DUPLICATES ────────────────────────────────────────────

    {
        "id": "issue_029",
        "title": "Login not working on Safari browser",
        "body": (
            "Login page is not loading on Safari.\n\n"
            "I get a blank white page when I go to the login URL.\n"
            "Works fine on Chrome.\n\n"
            "Safari version: 17, macOS Sonoma"
        ),
        "repo": "web-frontend",
        "author_type": "first-time-contributor",
        "user_reports": 1,
        "existing_labels": [],
        "open_issues_count": 450,
        "correct_type": "duplicate",
        "correct_priority": "P3",
        "correct_team": "frontend",
        "correct_effort": "small"
    },

    {
        "id": "issue_030",
        "title": "Please add night mode to the app",
        "body": (
            "I would really love a night mode / dark theme for this app.\n\n"
            "It's very bright at night and hurts my eyes.\n\n"
            "Can this be added?"
        ),
        "repo": "dashboard-ui",
        "author_type": "first-time-contributor",
        "user_reports": 1,
        "existing_labels": [],
        "open_issues_count": 340,
        "correct_type": "duplicate",
        "correct_priority": "P4",
        "correct_team": "frontend",
        "correct_effort": "small"
    },

    # ── MORE BUGS (P2/P3/P4) ─────────────────────────────────

    {
        "id": "issue_031",
        "title": "Search results not updating when filter is changed",
        "body": (
            "## Bug Report\n"
            "When I change the filter dropdown on the search results page, "
            "the results do not update. I have to manually refresh the page.\n\n"
            "**Steps:**\n"
            "1. Search for any term\n"
            "2. Results load correctly\n"
            "3. Change filter from 'All' to 'Recent'\n"
            "4. Results do NOT change — old results still showing\n"
            "5. Refresh page → correct filtered results appear"
        ),
        "repo": "web-frontend",
        "author_type": "regular",
        "user_reports": 17,
        "existing_labels": [],
        "open_issues_count": 450,
        "correct_type": "bug",
        "correct_priority": "P2",
        "correct_team": "frontend",
        "correct_effort": "small"
    },

    {
        "id": "issue_032",
        "title": "Notification badges not clearing after reading",
        "body": (
            "## Bug Report\n"
            "The red notification badge on the bell icon doesn't disappear "
            "after I read my notifications.\n\n"
            "**Steps:**\n"
            "1. Receive a notification (badge shows '3')\n"
            "2. Click bell icon and read all notifications\n"
            "3. Close notification panel\n"
            "4. Badge still shows '3'\n\n"
            "Expected: Badge clears after all notifications are read."
        ),
        "repo": "web-frontend",
        "author_type": "regular",
        "user_reports": 8,
        "existing_labels": [],
        "open_issues_count": 450,
        "correct_type": "bug",
        "correct_priority": "P3",
        "correct_team": "frontend",
        "correct_effort": "small"
    },

    {
        "id": "issue_033",
        "title": "Pagination breaks when items are deleted",
        "body": (
            "## Bug Report\n"
            "When I'm on page 3 of results and delete an item, "
            "the page reloads but shows an empty page instead of "
            "recalculating pagination.\n\n"
            "Reproducible 100% when deleting items from any page > 1."
        ),
        "repo": "web-frontend",
        "author_type": "regular",
        "user_reports": 5,
        "existing_labels": [],
        "open_issues_count": 450,
        "correct_type": "bug",
        "correct_priority": "P3",
        "correct_team": "frontend",
        "correct_effort": "small"
    },

    {
        "id": "issue_034",
        "title": "Database queries slow on tables with > 1 million rows",
        "body": (
            "## Performance Bug\n"
            "`GET /api/reports?type=full` takes 45+ seconds when the "
            "events table has more than 1 million rows.\n\n"
            "**Root cause:** The query does a full table scan — no index on `created_at`.\n\n"
            "Adding an index on `created_at` and `status` should fix this.\n"
            "This is affecting all enterprise customers with large datasets."
        ),
        "repo": "database-core",
        "author_type": "maintainer",
        "user_reports": 12,
        "existing_labels": ["performance"],
        "open_issues_count": 95,
        "correct_type": "bug",
        "correct_priority": "P2",
        "correct_team": "backend",
        "correct_effort": "small"
    },

    {
        "id": "issue_035",
        "title": "CI pipeline fails randomly on test step — flaky test",
        "body": (
            "## Bug Report\n"
            "The CI pipeline fails about 1 in 5 runs on the test step.\n\n"
            "**Failing test:** `test_concurrent_user_sessions`\n"
            "**Error:** `AssertionError: Expected 3 sessions, got 2`\n\n"
            "This is a timing/race condition issue — the test assumes "
            "async operations complete instantly. Needs a proper await or mock."
        ),
        "repo": "ci-cd-pipeline",
        "author_type": "maintainer",
        "user_reports": 1,
        "existing_labels": ["flaky-test"],
        "open_issues_count": 55,
        "correct_type": "bug",
        "correct_priority": "P3",
        "correct_team": "devops",
        "correct_effort": "medium"
    },

    {
        "id": "issue_036",
        "title": "Docker container exits with code 137 on startup",
        "body": (
            "## Bug Report\n"
            "The Docker container for the API service exits immediately "
            "with exit code 137 (OOM killed) when starting up.\n\n"
            "**Environment:** Docker 24, 2GB RAM allocated\n"
            "**Logs:** `Killed` — no other error\n\n"
            "The service used to work with 2GB. Something in the last "
            "3 releases must be consuming more memory on startup."
        ),
        "repo": "api-gateway",
        "author_type": "maintainer",
        "user_reports": 3,
        "existing_labels": [],
        "open_issues_count": 200,
        "correct_type": "bug",
        "correct_priority": "P2",
        "correct_team": "devops",
        "correct_effort": "medium"
    },

    # ── MORE FEATURES ────────────────────────────────────────

    {
        "id": "issue_037",
        "title": "Add GitHub OAuth login option",
        "body": (
            "## Feature Request\n"
            "Please add 'Login with GitHub' as an OAuth option.\n\n"
            "Many of our users are developers who already have GitHub accounts. "
            "This would reduce signup friction significantly.\n\n"
            "**Expected:** GitHub OAuth button on login/signup page."
        ),
        "repo": "user-auth-service",
        "author_type": "regular",
        "user_reports": 33,
        "existing_labels": ["enhancement"],
        "open_issues_count": 210,
        "correct_type": "feature",
        "correct_priority": "P3",
        "correct_team": "backend",
        "correct_effort": "medium"
    },

    {
        "id": "issue_038",
        "title": "Add audit log — track who changed what and when",
        "body": (
            "## Feature Request\n"
            "Enterprise customers require an audit log for compliance:\n\n"
            "- Who created/modified/deleted each record\n"
            "- Timestamp of each change\n"
            "- Old value vs new value\n"
            "- IP address of the actor\n\n"
            "This is a hard requirement for HIPAA and SOC2 compliance clients."
        ),
        "repo": "platform-core",
        "author_type": "maintainer",
        "user_reports": 18,
        "existing_labels": ["enterprise", "compliance"],
        "open_issues_count": 312,
        "correct_type": "feature",
        "correct_priority": "P2",
        "correct_team": "backend",
        "correct_effort": "large"
    },

    {
        "id": "issue_039",
        "title": "Support multiple languages (i18n)",
        "body": (
            "## Feature Request — Internationalization\n"
            "We have significant user bases in India, Brazil, and Germany "
            "who prefer using the app in their native language.\n\n"
            "Please add i18n support with at minimum:\n"
            "- Hindi\n"
            "- Portuguese (Brazil)\n"
            "- German\n\n"
            "This would unlock significant growth in non-English markets."
        ),
        "repo": "web-frontend",
        "author_type": "regular",
        "user_reports": 52,
        "existing_labels": ["enhancement", "i18n"],
        "open_issues_count": 450,
        "correct_type": "feature",
        "correct_priority": "P3",
        "correct_team": "frontend",
        "correct_effort": "large"
    },

    {
        "id": "issue_040",
        "title": "Add mobile app for iOS and Android",
        "body": (
            "## Feature Request\n"
            "Please build a mobile app for iOS and Android.\n\n"
            "Many users need to access the platform on the go. "
            "The current web app is not optimized for mobile screens.\n\n"
            "A React Native app would allow sharing code with the web."
        ),
        "repo": "platform-core",
        "author_type": "regular",
        "user_reports": 120,
        "existing_labels": ["enhancement"],
        "open_issues_count": 312,
        "correct_type": "feature",
        "correct_priority": "P3",
        "correct_team": "frontend",
        "correct_effort": "large"
    },

    {
        "id": "issue_041",
        "title": "Add webhook support for real-time event notifications",
        "body": (
            "## Feature Request\n"
            "Please add webhook support so external systems can be notified "
            "when events happen in our platform.\n\n"
            "**Use case:** When a new item is created, fire a POST request "
            "to a user-configured URL with event payload.\n\n"
            "This would enable Zapier/n8n integrations and custom automation."
        ),
        "repo": "integrations-service",
        "author_type": "regular",
        "user_reports": 44,
        "existing_labels": ["enhancement"],
        "open_issues_count": 145,
        "correct_type": "feature",
        "correct_priority": "P2",
        "correct_team": "backend",
        "correct_effort": "medium"
    },

    # ── EDGE CASES / TRICKY ONES ──────────────────────────────

    {
        "id": "issue_042",
        "title": "Server throwing 503 errors under high load",
        "body": (
            "## Bug Report\n"
            "During business hours (10am–4pm IST), the API starts returning "
            "503 Service Unavailable errors for about 5-10% of requests.\n\n"
            "Load testing shows the issue begins at ~500 concurrent users.\n\n"
            "The server has capacity for 1000 concurrent users per our benchmarks. "
            "Something is causing early saturation — possibly connection pool exhaustion."
        ),
        "repo": "api-gateway",
        "author_type": "maintainer",
        "user_reports": 67,
        "existing_labels": ["performance"],
        "open_issues_count": 200,
        "correct_type": "bug",
        "correct_priority": "P1",
        "correct_team": "backend",
        "correct_effort": "medium"
    },

    {
        "id": "issue_043",
        "title": "Typo in button label: 'Sumbit' should be 'Submit'",
        "body": (
            "The button on the contact form says 'Sumbit' instead of 'Submit'.\n\n"
            "Small typo but looks unprofessional."
        ),
        "repo": "web-frontend",
        "author_type": "first-time-contributor",
        "user_reports": 1,
        "existing_labels": [],
        "open_issues_count": 450,
        "correct_type": "bug",
        "correct_priority": "P4",
        "correct_team": "frontend",
        "correct_effort": "small"
    },

    {
        "id": "issue_044",
        "title": "Need to improve test coverage — currently at 23%",
        "body": (
            "## Technical Debt\n"
            "Our test coverage is at 23% — far below the recommended 80%.\n\n"
            "Key areas with zero test coverage:\n"
            "- Payment processing module\n"
            "- User authentication flows\n"
            "- File upload service\n\n"
            "This makes refactoring risky and bugs harder to catch."
        ),
        "repo": "platform-core",
        "author_type": "maintainer",
        "user_reports": 1,
        "existing_labels": ["technical-debt"],
        "open_issues_count": 312,
        "correct_type": "feature",
        "correct_priority": "P2",
        "correct_team": "backend",
        "correct_effort": "large"
    },

    {
        "id": "issue_045",
        "title": "Deployment script fails on AWS us-west-2 region",
        "body": (
            "## Bug Report\n"
            "The deployment script `deploy.sh` fails when targeting AWS us-west-2.\n\n"
            "**Error:** `AMI ami-0abc123 does not exist in us-west-2`\n\n"
            "The AMI ID is hardcoded to us-east-1. The script should "
            "automatically select the correct AMI for the target region."
        ),
        "repo": "ci-cd-pipeline",
        "author_type": "regular",
        "user_reports": 2,
        "existing_labels": [],
        "open_issues_count": 55,
        "correct_type": "bug",
        "correct_priority": "P2",
        "correct_team": "devops",
        "correct_effort": "small"
    },

    {
        "id": "issue_046",
        "title": "How do I set up local development environment?",
        "body": (
            "Hi, I'm a new contributor.\n\n"
            "I cloned the repo and followed the README but I keep getting "
            "an error:\n"
            "`ModuleNotFoundError: No module named 'config'`\n\n"
            "The README doesn't mention this module. Is there a setup "
            "step I'm missing?"
        ),
        "repo": "platform-core",
        "author_type": "first-time-contributor",
        "user_reports": 1,
        "existing_labels": [],
        "open_issues_count": 312,
        "correct_type": "question",
        "correct_priority": "P3",
        "correct_team": "documentation",
        "correct_effort": "small"
    },

    {
        "id": "issue_047",
        "title": "Add support for custom domain names",
        "body": (
            "## Feature Request\n"
            "Currently all users are on `username.app.io` subdomains.\n\n"
            "Please allow users to connect their own custom domain "
            "e.g. `app.mycompany.com`.\n\n"
            "This is a must-have for enterprise/white-label customers.\n"
            "Estimated from sales: blocking ~15 enterprise deals."
        ),
        "repo": "platform-core",
        "author_type": "maintainer",
        "user_reports": 31,
        "existing_labels": ["enhancement", "enterprise"],
        "open_issues_count": 312,
        "correct_type": "feature",
        "correct_priority": "P2",
        "correct_team": "devops",
        "correct_effort": "large"
    },

    {
        "id": "issue_048",
        "title": "Charts library version upgrade — v2 breaking changes",
        "body": (
            "## Maintenance\n"
            "The charts library (ChartJS) released v4 with breaking changes.\n"
            "We're still on v2 which is no longer receiving security patches.\n\n"
            "Need to upgrade to v4 and update all chart components to new API.\n\n"
            "Affected files: ~12 chart components across the dashboard."
        ),
        "repo": "web-frontend",
        "author_type": "maintainer",
        "user_reports": 1,
        "existing_labels": ["dependencies"],
        "open_issues_count": 450,
        "correct_type": "feature",
        "correct_priority": "P3",
        "correct_team": "frontend",
        "correct_effort": "medium"
    },

    {
        "id": "issue_049",
        "title": "Email verification link expires too quickly — 15 minutes",
        "body": (
            "## Bug / UX Issue\n"
            "The email verification link expires in 15 minutes.\n\n"
            "Many users miss this window (especially in different timezones "
            "or if email delivery is slow) and have to request a new link.\n\n"
            "**Suggestion:** Extend expiry to 24 hours — this is industry standard.\n"
            "Support tickets about this: 34 in the last month."
        ),
        "repo": "user-auth-service",
        "author_type": "regular",
        "user_reports": 34,
        "existing_labels": [],
        "open_issues_count": 210,
        "correct_type": "bug",
        "correct_priority": "P3",
        "correct_team": "backend",
        "correct_effort": "small"
    },

    {
        "id": "issue_050",
        "title": "Add GDPR data deletion — right to be forgotten",
        "body": (
            "## Compliance Feature\n"
            "We need to implement GDPR Article 17 — Right to Erasure.\n\n"
            "Users must be able to:\n"
            "1. Request deletion of all their personal data\n"
            "2. Receive confirmation email once complete\n"
            "3. Be fully removed from all systems within 30 days\n\n"
            "This is a legal requirement for EU users. "
            "We've received 3 formal GDPR requests already this month."
        ),
        "repo": "user-auth-service",
        "author_type": "maintainer",
        "user_reports": 3,
        "existing_labels": ["compliance", "GDPR"],
        "open_issues_count": 210,
        "correct_type": "feature",
        "correct_priority": "P1",
        "correct_team": "backend",
        "correct_effort": "large"
    },
]


def get_all_issues() -> List[Dict]:
    """Return the full issue bank."""
    return ISSUE_BANK


def get_issue_by_id(issue_id: str) -> Dict:
    """Fetch a specific issue by its ID."""
    for issue in ISSUE_BANK:
        if issue["id"] == issue_id:
            return issue
    raise ValueError(f"Issue {issue_id} not found")


def get_issues_by_type(issue_type: str) -> List[Dict]:
    """Return all issues of a specific type e.g. 'bug', 'feature'."""
    return [i for i in ISSUE_BANK if i["correct_type"] == issue_type]


def get_issues_by_priority(priority: str) -> List[Dict]:
    """Return all issues of a specific priority e.g. 'P1', 'P2'."""
    return [i for i in ISSUE_BANK if i["correct_priority"] == priority]


def get_random_issue(task_id: str = "task_1", seen_ids: List[str] = None) -> Dict:
    """
    Return a random issue not yet seen in this episode.
    task_id controls difficulty:
      task_1 → mix of clear-cut issues (easy to classify)
      task_2 → issues with more context needed for priority
      task_3 → full mix including tricky edge cases
    """
    if seen_ids is None:
        seen_ids = []

    if task_id == "task_1":
        pool = [i for i in ISSUE_BANK
                if i["id"] not in seen_ids
                and i["correct_type"] in ["bug", "feature", "question"]]
    elif task_id == "task_2":
        pool = [i for i in ISSUE_BANK
                if i["id"] not in seen_ids
                and i["correct_priority"] in ["P1", "P2", "P3", "P4"]]
    else:
        pool = [i for i in ISSUE_BANK if i["id"] not in seen_ids]

    if not pool:
        pool = ISSUE_BANK  # reset if all seen

    return random.choice(pool)
