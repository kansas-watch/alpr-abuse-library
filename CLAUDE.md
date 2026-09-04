# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repository is

The ALPR Abuse Library is a curated, editorially-reviewed dataset — not a software application — of news articles documenting ALPR/Flock Safety camera misuse and civil liberties concerns, maintained by Kansas Watch. The "code" here is a small static data pipeline: a JSON dataset, a validator, a static HTML viewer, and documentation of the human editorial process. Most work in this repo is data curation, not programming.

## Repository structure & data flow

- `library.json` — the single source of truth. Top-level: `_meta` (maintainer info, schema version), `abuse_categories` (the controlled vocabulary), `entries` (the actual records, in `id` order — not date order).
- `index.html` — the static site (served at library.kansas.watch). No build step; it `fetch()`es `./library.json` client-side at runtime and does all filtering/rendering in-browser. Editing `library.json` alone updates the live site — `index.html` itself rarely needs to change.
- `README.md` — contains a second, human-readable copy of the index as a Markdown table, sorted by `date_published`. It is **not** generated from `library.json` and must be kept in sync manually whenever entries are added.
- `validate_library.py` — the only "test" in this repo. Run before every commit that touches `library.json`.
- `schema.md` — field-by-field definition of `library.json` entries, plus editorial notes (e.g. one entry per *case* not per *article*; `state` is a normalized USPS code separate from the free-text `jurisdiction` display string).
- `CONTRIBUTING.md` — the human-facing submission/editorial process and the definitive descriptions of the 10 `abuse_categories` values.
- `ALPR Abuse Library - Article Submission Form - Form Responses*.csv` — periodic exports of the Google Form response sheet backing submissions. Gitignored, local-only, never committed. These are cumulative exports, not incremental — a new export contains all prior rows plus new ones.

## Commands

- Validate the dataset: `python3 validate_library.py` (defaults to `library.json`; accepts an explicit path). Checks required fields, the `abuse_categories` vocabulary, valid `state` codes/format, `date_published` format, duplicate `id`s, and duplicate/suspicious `url`s. Exits non-zero and lists every problem found — always run this before committing changes to `library.json`.
- No build, lint, or test suite beyond the validator.

## Processing a new submission-form CSV export

This is the recurring task in this repo:

1. Diff the new CSV against the previous export (match on `Timestamp` + `Article URL`) to isolate only the new rows.
2. For each new row, fetch the source article and verify it per `CONTRIBUTING.md`'s checklist (real incident, not paywalled, not speculation), and check `library.json` for existing entries with the same URL, agency, or incident.
3. Assign/confirm `abuse_categories` from the controlled vocabulary based on what the article actually documents — treat the submitter's own category picks as a starting point, not authoritative. If you deviate from what they picked, record why in the entry's `notes` field.
4. Append entries to `library.json`: `id` is the next sequential zero-padded 3-digit string (check the last entry's `id`, it is not date-based and not derivable from `entries.length` alone if any ids were ever skipped), `date_added` is today, `status: "approved"` once verified. One entry per distinct case, not per article — a single article covering multiple officers/agencies/jurisdictions gets multiple entries sharing the same `url` (the validator expects and allows this as long as `jurisdiction`/`agency` differ).
5. Add matching rows to the README index table in `date_published` order (not `id` order).
6. Update `_meta.last_updated` in `library.json` to today's date.
7. Run `python3 validate_library.py` and resolve anything it flags before committing.
8. If asked to reflect the review back into the Google Form's response spreadsheet: it has `Status` and `Editor Notes` columns (near the end, not the first columns shown in the CSV export) already used for exactly this purpose — set `Status` to `Approved` (or the appropriate value) and add the entry's `id` plus categorization rationale to `Editor Notes`, matching the style of already-filled rows.
