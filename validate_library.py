#!/usr/bin/env python3
"""
Validation script for the ALPR Abuse Library's library.json.

Run this after any manual edit, before committing:
    python3 validate_library.py library.json

Checks:
  1. File parses as valid JSON (the existing json.load() habit, made explicit)
  2. Every entry's abuse_categories are in the controlled vocabulary
  3. Every entry has a 'state' field: a valid two-letter USPS code, a list of
     valid codes, or null (for national / non-state-specific entries)
  4. No duplicate id values
  5. No duplicate url values across entries (catches accidental re-submissions)
  6. Every entry has the required fields: id, date_published, publication,
     submission_type, title, url, jurisdiction, state, agency,
     abuse_categories, description, status
  7. date_published is a valid YYYY-MM-DD string
  8. status is one of the expected values

Exits with a non-zero status code and prints all problems found if anything
fails, so CI (or a pre-commit hook) can block on it.
"""

import json
import re
import sys
from collections import Counter

REQUIRED_FIELDS = [
    "id", "date_published", "publication", "submission_type", "title",
    "url", "jurisdiction", "state", "agency", "abuse_categories",
    "description", "status",
]

VALID_STATES = {
    "AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA", "HI", "ID",
    "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", "MA", "MI", "MN", "MS",
    "MO", "MT", "NE", "NV", "NH", "NJ", "NM", "NY", "NC", "ND", "OH", "OK",
    "OR", "PA", "RI", "SC", "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV",
    "WI", "WY", "DC",
}

VALID_STATUSES = {"approved", "pending", "rejected"}

DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def validate(path):
    errors = []

    with open(path, encoding="utf-8") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            print(f"FATAL: {path} is not valid JSON: {e}")
            sys.exit(1)

    valid_categories = set(data.get("abuse_categories", []))
    if not valid_categories:
        errors.append("_meta.abuse_categories vocabulary is empty or missing")

    entries = data.get("entries", [])
    if not entries:
        errors.append("No entries found")

    ids_seen = Counter()
    url_to_entries = {}
    notes = []

    for i, entry in enumerate(entries):
        loc = f"entry #{i} (id={entry.get('id', '?')})"

        for field in REQUIRED_FIELDS:
            if field not in entry:
                errors.append(f"{loc}: missing required field '{field}'")

        eid = entry.get("id")
        if eid:
            ids_seen[eid] += 1

        url = entry.get("url")
        if url:
            url_to_entries.setdefault(url, []).append(entry)

        date = entry.get("date_published")
        if date and not DATE_RE.match(date):
            errors.append(f"{loc}: date_published '{date}' is not YYYY-MM-DD")

        status = entry.get("status")
        if status and status not in VALID_STATUSES:
            errors.append(f"{loc}: status '{status}' not in {VALID_STATUSES}")

        cats = entry.get("abuse_categories", [])
        if not cats:
            errors.append(f"{loc}: abuse_categories is empty")
        for cat in cats:
            if cat not in valid_categories:
                errors.append(f"{loc}: unknown category '{cat}'")

        # state: null, a valid code, or a list of valid codes
        state = entry.get("state", "__MISSING__")
        if state == "__MISSING__":
            pass  # already caught by required-fields check above
        elif state is None:
            pass  # national / non-state-specific entries are fine
        elif isinstance(state, str):
            if state not in VALID_STATES:
                errors.append(f"{loc}: state '{state}' is not a valid USPS code")
        elif isinstance(state, list):
            if not state:
                errors.append(f"{loc}: state is an empty list, use null instead")
            for s in state:
                if s not in VALID_STATES:
                    errors.append(f"{loc}: state '{s}' in list is not a valid USPS code")
        else:
            errors.append(f"{loc}: state field has unexpected type {type(state).__name__}")

    for eid, count in ids_seen.items():
        if count > 1:
            errors.append(f"duplicate id '{eid}' appears {count} times")

    for url, group in url_to_entries.items():
        if len(group) <= 1:
            continue
        ids = [e.get("id") for e in group]
        signatures = {(e.get("jurisdiction"), e.get("agency")) for e in group}
        if len(signatures) == 1:
            # Same url, same jurisdiction+agency: almost certainly an
            # accidental re-submission of the same case, not a deliberate
            # split. Fail.
            errors.append(
                f"suspected accidental duplicate: ids {ids} share url and "
                f"jurisdiction/agency ({url})"
            )
        else:
            # Same source article covering distinct cases (different
            # jurisdiction and/or agency) is expected under the "track
            # cases, not articles" policy. Note it, don't fail.
            notes.append(
                f"ids {ids} intentionally share a source url across "
                f"distinct cases ({url})"
            )

    if notes:
        print(f"NOTE: {len(notes)} intentional shared-source url(s):")
        for n in notes:
            print(f"  - {n}")
        print()

    if errors:
        print(f"FAILED: {len(errors)} problem(s) found in {path}\n")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)
    else:
        print(f"OK: {path} — {len(entries)} entries, all checks passed.")
        sys.exit(0)


if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "library.json"
    validate(target)
