"""
security.py
-----------
Input validation and sanitization module for SAGE.

This is the core "cybersecurity" feature of the project: every piece
of user input is checked BEFORE it reaches the NLP engine. This
demonstrates a practical understanding of input validation - a
foundational concept in OWASP's Top 10 (Injection is #3 on the
2021 list).

What this blocks:
1. Script injection patterns (e.g. <script>, javascript:, onerror=)
2. SQL injection patterns (e.g. ' OR 1=1, DROP TABLE, UNION SELECT)
3. Known malware/backdoor-related keywords (as a basic keyword filter -
   this is NOT malware detection, it's a keyword-based content filter
   to demonstrate the concept of flagging suspicious input)
4. Command injection patterns (e.g. ;rm -rf, &&, |, backticks)

Interview talking point:
"This isn't a production-grade WAF - it's a rule-based filter that
demonstrates the OWASP Top 10 concept of input validation. I used
regex pattern matching to flag common injection signatures before
input reaches the response engine."
"""

import re

# Patterns associated with script/XSS injection
SCRIPT_INJECTION_PATTERNS = [
    r"<script.*?>",
    r"javascript:",
    r"onerror\s*=",
    r"onload\s*=",
    r"<iframe.*?>",
]

# Patterns associated with SQL injection
SQL_INJECTION_PATTERNS = [
    r"(\bOR\b|\bAND\b)\s+\d+\s*=\s*\d+",   # e.g. OR 1=1
    r"DROP\s+TABLE",
    r"UNION\s+SELECT",
    r"--\s*$",
    r";\s*DROP",
]

# Patterns associated with command injection
COMMAND_INJECTION_PATTERNS = [
    r";\s*rm\s+-rf",
    r"&&",
    r"\|\s*nc\s",
    r"`.*`",
    r"\$\(.*\)",
]

# Keyword-based flag list (basic content filter, not malware detection)
FLAGGED_KEYWORDS = [
    "malware",
    "backdoor",
    "ransomware",
    "keylogger",
    "trojan",
    "rootkit",
]

ALL_PATTERNS = (
    SCRIPT_INJECTION_PATTERNS + SQL_INJECTION_PATTERNS + COMMAND_INJECTION_PATTERNS
)


def validate_input(user_input: str):
    """
    Validate user input against known malicious patterns.

    Returns a tuple: (is_safe: bool, reason: str or None)
    """
    if user_input is None:
        return False, "Empty input"

    text = user_input.strip()

    if len(text) == 0:
        return False, "Empty input"

    if len(text) > 2000:
        return False, "Input exceeds maximum allowed length"

    lowered = text.lower()

    # Check regex-based injection patterns
    for pattern in ALL_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            return False, f"Blocked: matched suspicious pattern ({pattern})"

    # Check flagged keywords
    for keyword in FLAGGED_KEYWORDS:
        if keyword in lowered:
            return False, f"Blocked: flagged keyword detected ('{keyword}')"

    return True, None


def sanitize_input(user_input: str) -> str:
    """
    Basic sanitization: strip HTML tags and excess whitespace.
    Applied to inputs that pass validation, as defense-in-depth.
    """
    no_tags = re.sub(r"<[^>]*>", "", user_input)
    return no_tags.strip()
