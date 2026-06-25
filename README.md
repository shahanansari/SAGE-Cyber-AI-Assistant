# SAGE — Cyber Assistant (GUI-Based)

A desktop AI assistant built in Python with a PyQt5 GUI, focused on
demonstrating practical, foundational cybersecurity concepts alongside
basic NLP-style task automation.

## Features

- **Local authentication** — username/password login gated by a
  SHA-256 hashed credential store (no plaintext passwords saved).
- **Input validation & sanitization** — every user message is checked
  against known injection patterns (script/XSS, SQL injection,
  command injection) and a flagged-keyword filter before being
  processed, based on OWASP Top 10 concepts.
- **Rule-based NLP engine** — intent matching via keyword sets,
  routing recognized commands (greetings, time/date, help, log
  viewing, exit) to response handlers.
- **Activity logging** — every login attempt, user input, and blocked
  input is written to a timestamped local log file (`logs/activity.log`),
  viewable from within the app via the `show log` command.
- **Modular architecture** — GUI, authentication, security, NLP, and
  logging are fully separated into independent modules.

## Project Structure

```
sage_assistant/
├── main.py          # GUI layer (login window + chat window)
├── auth.py          # Authentication logic (hashing, verification)
├── security.py      # Input validation & sanitization
├── nlp_engine.py     # Intent matching & response generation
├── logger.py         # Activity logging
├── requirements.txt
└── logs/
    └── activity.log  # created at runtime
```

## How It Works

1. On first run, the app prompts you to set up a local username and
   password. The password is hashed (SHA-256) and stored in
   `credentials.json` — never in plaintext.
2. After login, the chat window opens. Every message you type passes
   through `security.py` first:
   - If it matches a known malicious pattern (e.g. `<script>`,
     `DROP TABLE`, `; rm -rf`) or a flagged keyword (e.g. "malware",
     "backdoor"), it's blocked and logged.
   - If it's safe, it's sanitized and passed to `nlp_engine.py`.
3. The NLP engine matches the cleaned text against known intents
   (greeting, time, date, help, log viewing, exit) and returns a
   response.
4. Every step (login attempts, inputs, blocks) is logged with a
   timestamp via `logger.py`.

## Setup & Run

```bash
pip install -r requirements.txt
python main.py
```

## Supported Commands (try these in the chat)

| Input              | Behavior                          |
|--------------------|------------------------------------|
| `hello`            | Greeting response                  |
| `what time is it`  | Returns current time               |
| `today's date`     | Returns current date               |
| `help`             | Lists supported commands           |
| `show log`         | Displays last 10 activity log lines|
| `exit`             | Closes the application             |

Try also sending something like `<script>alert(1)</script>` or
`DROP TABLE users` — you'll see it get blocked and logged instead of
reaching the response engine.

## Design Notes / Limitations (honest scope)

This project is intentionally scoped as a **learning/demonstration
project**, not production security software:

- The input filter is **rule-based / pattern-matching**, not a true
  WAF or malware scanner. It demonstrates the *concept* of input
  validation (OWASP Top 10 — Injection), not enterprise-grade
  detection.
- The NLP engine uses **keyword/intent matching**, not a trained
  machine learning model. This was a deliberate choice to keep the
  assistant's logic transparent and explainable for a learning
  project, rather than relying on a black-box model.
- Authentication is **single local user**, hashed locally — suitable
  for a desktop tool, not designed for multi-user or networked
  authentication.

## Possible Future Improvements

- Add salted hashing (currently unsalted SHA-256) for stronger
  credential storage.
- Expand the intent set / connect to a small ML-based intent
  classifier.
- Add a settings panel to manage flagged keywords without editing code.
