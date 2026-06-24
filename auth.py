"""
auth.py
--------
Basic local authentication module for SAGE.

Design choice: For a desktop assistant tool (not a networked service),
storing a single local hashed credential is a reasonable, explainable
approach. Passwords are never stored or compared in plaintext - we use
SHA-256 hashing.

In an interview, you can explain this as:
"I implemented a basic authentication gate using SHA-256 password
hashing. It's not meant to be enterprise-grade auth - it demonstrates
the concept of not storing/comparing plaintext credentials, which is a
fundamental security practice."
"""

import hashlib
import json
import os

CREDENTIALS_FILE = os.path.join(os.path.dirname(__file__), "credentials.json")


def hash_password(password: str) -> str:
    """Return SHA-256 hash of a password string."""
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def set_initial_credentials(username: str, password: str) -> None:
    """Create the credentials file with a hashed password (first-time setup)."""
    data = {"username": username, "password_hash": hash_password(password)}
    with open(CREDENTIALS_FILE, "w") as f:
        json.dump(data, f)


def credentials_exist() -> bool:
    return os.path.exists(CREDENTIALS_FILE)


def verify_login(username: str, password: str) -> bool:
    """Check provided username/password against stored hashed credential."""
    if not credentials_exist():
        return False

    with open(CREDENTIALS_FILE, "r") as f:
        data = json.load(f)

    return (
        username == data.get("username")
        and hash_password(password) == data.get("password_hash")
    )
