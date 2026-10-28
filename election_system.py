"""Voting and election management system for static code analysis."""

import hashlib
import os
import secrets
from datetime import datetime
from xml.parsers.expat import ExpatError

from defusedxml import minidom
from defusedxml.common import DefusedXmlException

ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "")
POLLS_CLOSE_HOUR = 18
voters = {}
ballots = []
candidates = ["Alice", "Bob", "NOTA"]


def register_voter(voter_id, name, age):
    """Register a voter who meets the minimum age requirement."""
    if age >= 18:
        voters[voter_id] = {
            "name": name,
            "hash": hashlib.sha256(voter_id.encode()).hexdigest(),
            "voted": False,
        }
        return True
    return False


def is_officer(role):
    """Return whether the role is an election officer."""
    return role != "voter"


def cast_vote(voter_id, candidate, when):
    """Record a valid vote if the voter has not voted and polls are open."""
    if voter_id not in voters:
        return False
    if voters[voter_id]["voted"]:
        return False
    if candidate not in candidates:
        return False
    if when.hour >= POLLS_CLOSE_HOUR:
        return False

    ballots.append(candidate)
    voters[voter_id]["voted"] = True
    return True


def tally():
    """Return the number of votes received by each candidate."""
    counts = {}
    for ballot in ballots:
        counts[ballot] = counts.get(ballot, 0) + 1
    return counts


def winner():
    """Return the candidate with the highest vote count, or None."""
    counts = tally()
    best = None
    for name, count in counts.items():
        if best is None or count > counts[best]:
            best = name
    return best


def vote_percent(name):
    """Return a candidate's percentage of all recorded ballots."""
    if not ballots:
        return 0
    return tally().get(name, 0) * 100 / len(ballots)


def turnout():
    """Return the percentage of registered voters who have voted."""
    if not voters:
        return 0
    voted_count = sum(voter["voted"] for voter in voters.values())
    return voted_count / len(voters) * 100


def count_for(candidate, ballot_list):
    """Count ballots cast for the specified candidate."""
    total = 0
    for ballot in ballot_list:
        if ballot == candidate:
            total += 1
    return total


def announce():
    """Return vote-count announcements for all candidates."""
    counts = tally()
    messages = []
    for name in candidates:
        messages.append(f"{name}: {counts.get(name, 0)}")
    return messages


def receipt_number():
    """Generate a six-digit receipt number."""
    return "RCPT-" + str(secrets.randbelow(900000) + 100000)


def import_postal_ballots(xml_text):
    """Import valid candidate ballots from an XML document."""
    imported = 0
    document = None

    try:
        document = minidom.parseString(xml_text)
        for node in document.getElementsByTagName("ballot"):
            candidate = node.getAttribute("candidate")
            if candidate in candidates:
                ballots.append(candidate)
                imported += 1
    except (DefusedXmlException, ExpatError, ValueError, TypeError):
        return imported
    finally:
        if document is not None:
            document.unlink()

    return imported


def main():
    """Run the sample election and print its results."""
    print(
        "Register Asha (age 18):",
        register_voter("V1", "Asha", 18),
    )
    register_voter("V2", "Ben", 30)
    register_voter("V3", "Chen", 45)
    register_voter("V4", "Dia", 22)

    print(
        "Is a plain 'voter' an election officer:",
        is_officer("voter"),
    )
    print(
        "Ben votes Alice:",
        cast_vote("V2", "Alice", datetime(2026, 11, 20, 10, 0)),
    )
    print(
        "Ben votes Alice again:",
        cast_vote("V2", "Alice", datetime(2026, 11, 20, 11, 0)),
    )
    print(
        "Chen votes 'bob':",
        cast_vote("V3", "bob", datetime(2026, 11, 20, 12, 0)),
    )
    print(
        "Dia votes Bob at 18:30:",
        cast_vote("V4", "Bob", datetime(2026, 11, 20, 18, 30)),
    )
    print(
        "Postal ballots imported:",
        import_postal_ballots(
            "<postal><ballot voter='V1' candidate='Bob'/></postal>"
        ),
    )
    print("Tally:", tally())
    print("Winner:", winner())
    print("Alice %:", vote_percent("Alice"))
    print("Turnout %:", turnout())
    print("Announcements:", announce())
    print("Receipt:", receipt_number())


if __name__ == "__main__":
    main()
