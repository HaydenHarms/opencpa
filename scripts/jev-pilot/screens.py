"""Jev screens for opencpa question quality.

Each item is shown to Jev as stem + choices only (no key, no rationales, no skill tag), the same blindness the
blind verifier works under. Four checks run in one call; blueprint-task mapping runs in a second call (FAR only).
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))

SKILL_LEVELS = [
    "Remembering and Understanding -- recalls or identifies one rule, definition or classification; any arithmetic is incidental",
    "Application -- applies a rule or performs a calculation on the facts given",
    "Analysis -- examines a draft, reconciliation or set of facts to detect, investigate or correct discrepancies, "
    "or to derive the impact of an error, change or transaction; the student must find what is wrong or work out an effect",
]
SKILL_SHORT = ["Remembering and Understanding", "Application", "Analysis"]

CHECKS = {
    "giveaway": {
        "type": "noul",
        "instructions": (
            "The stem states, names or points at something the student is supposed to work out: a classification "
            "label the student must decide (for example 'meets the criteria', 'distinct performance obligation', "
            "'reasonably possible'), a stated conclusion or required presentation, wording that restates a rule's "
            "criteria nearly word for word, or the error the student is supposed to find."
        ),
    },
    "form_cue": {
        "type": "noul",
        "instructions": (
            "A choice can be picked or ruled out from its form alone, without solving the problem: the correct-looking "
            "choice is noticeably longer or more detailed than the others, several choices are combinations of the same "
            "components, or a choice answers a different period or statement line than the question asks."
        ),
    },
    "ambiguity": {
        "type": "noul",
        "instructions": (
            "The stem leaves out a fact or an election the entity made that is needed to reach one answer, or more "
            "than one choice is defensible under GAAP as the question is written."
        ),
    },
    "skill": {
        "type": "score",
        "instructions": "The cognitive skill level this question tests, judged by what the student must do.",
        "criteria": SKILL_LEVELS,
    },
}


def item_state(rec):
    lines = [f"CPA exam section: {rec['section']}", f"Topic: {rec['topic']}", "", "QUESTION STEM:", rec["stem"], "", "CHOICES:"]
    lines += [f"{c['id']}. {c['text']}" for c in rec["choices"]]
    return "\n".join(lines)


def task_question():
    tasks = json.load(open(os.path.join(HERE, "far_tasks.json")))
    return {
        "task": {
            "type": "choice",
            "instructions": "The 2026 FAR blueprint representative task this question mainly tests.",
            "criteria": {f"{t['code']} {t['task']}": None for t in tasks},
        }
    }, {f"{t['code']} {t['task']}": t["code"] for t in tasks}
