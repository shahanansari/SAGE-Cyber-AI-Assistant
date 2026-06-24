"""
logger.py
---------
Activity logging module for SAGE.

Logs every user interaction (login attempts, commands sent, flagged
inputs) with a timestamp, to a local log file. This satisfies the
"activity logging" feature and is a common, explainable pattern used
in real security tooling (audit trails).
"""

import os
from datetime import datetime

LOG_DIR = os.path.join(os.path.dirname(__file__), "logs")
LOG_FILE = os.path.join(LOG_DIR, "activity.log")

os.makedirs(LOG_DIR, exist_ok=True)


def log_event(event_type: str, detail: str) -> None:
    """
    Append a timestamped event to the activity log.

    event_type examples: LOGIN_SUCCESS, LOGIN_FAILED, USER_INPUT,
    INPUT_BLOCKED, SYSTEM
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{timestamp}] {event_type}: {detail}\n"

    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(line)


def read_recent_logs(n: int = 20) -> list:
    """Return the last n log lines (used for an optional in-app log viewer)."""
    if not os.path.exists(LOG_FILE):
        return []
    with open(LOG_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()
    return lines[-n:]
