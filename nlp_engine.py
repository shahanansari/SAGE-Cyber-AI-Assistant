"""
nlp_engine.py
-------------
Rule-based intent matching and response generation for SAGE.

This is intentionally a rule-based / keyword-matching system rather
than a deep-learning NLP model. Resume claim covers "NLP concepts" -
intent classification via keyword matching IS a real, foundational
NLP technique (used in early chatbots and still used in many
production rule-based assistants for simple, bounded domains).
"""

import re
from datetime import datetime

# Each intent maps to a list of trigger keywords/phrases
INTENTS = {
    "greeting": ["hello", "hi", "hey", "good morning", "good evening"],
    "time": ["what time", "current time", "what's the time"],
    "date": ["what date", "today's date", "what day is it"],
    "help": ["help", "what can you do", "commands", "options"],
    "log_view": ["show log", "view log", "activity log", "show activity"],
    "exit": ["exit", "quit", "close", "bye", "goodbye"],
}


def tokenize(text: str) -> list:
    """Simple tokenizer: lowercase and split on non-alphanumeric chars."""
    return re.findall(r"[a-z0-9']+", text.lower())


def match_intent(text: str) -> str:
    """
    Match cleaned input text against known intent keyword sets.
    Returns the intent name, or 'unknown' if no match found.
    """
    lowered = text.lower()

    for intent, phrases in INTENTS.items():
        for phrase in phrases:
            if phrase in lowered:
                return intent

    return "unknown"


def generate_response(text: str) -> str:
    """
    Main entry point: matches intent and returns an appropriate
    response string. This is called AFTER input has passed validation
    in security.py.
    """
    intent = match_intent(text)

    if intent == "greeting":
        return "Hello! I'm SAGE, your assistant. Type 'help' to see what I can do."

    elif intent == "time":
        return f"Current time: {datetime.now().strftime('%H:%M:%S')}"

    elif intent == "date":
        return f"Today's date: {datetime.now().strftime('%Y-%m-%d')}"

    elif intent == "help":
        return (
            "I can help with:\n"
            "- Greetings (try 'hello')\n"
            "- Time / date queries\n"
            "- Viewing recent activity logs ('show log')\n"
            "- Type 'exit' to close the app"
        )

    elif intent == "log_view":
        return "__SHOW_LOG__"  # special signal handled by the GUI layer

    elif intent == "exit":
        return "__EXIT__"  # special signal handled by the GUI layer

    else:
        return (
            "I didn't recognize that command. Type 'help' to see what I support."
        )
