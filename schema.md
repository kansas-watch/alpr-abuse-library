# Data Schema

This document defines the fields in `library.json`.

## Entry Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique identifier. Format: `YYYY-NNN` (e.g. `2024-001`) |
| `url` | string | Direct URL to the published article |
| `title` | string | Article title as published |
| `publication` | string | Name of the news outlet or publishing organization |
| `submission_type` | string | One of: `case_study`, `investigative_article`, `opinion_piece`, `news_report` |
| `date_published` | string | ISO 8601 date: `YYYY-MM-DD` |
| `date_added` | string | ISO 8601 date entry was approved and added |
| `jurisdiction_city` | string | City or county where the incident occurred |
| `jurisdiction_state` | string | Two-letter state abbreviation (e.g. `KS`) |
| `agency` | string | Law enforcement agency or entity involved |
| `categories` | array | One or more abuse category slugs (see CONTRIBUTING.md) |
| `summary` | string | 1–3 sentence description of the documented incident |
| `submitted_by` | string | Name of submitter (blank if anonymous) |
| `notes` | string | Optional editor notes |

## Versioning

The `_meta.schema_version` field will increment if breaking changes are made to this schema. Non-breaking additions (new optional fields) will not increment the version.

| Version | Changes |
|---------|---------|
| `1.1` | Renamed `headline` → `title`; added `submission_type` field |
| `1.0` | Initial schema |
