# Data Schema

This document defines the fields in `library.json`.

## Entry Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique identifier, zero-padded three-digit string in submission order (e.g. `"001"`, `"091"`). Not date-based. |
| `date_published` | string | ISO 8601 date the source article was published: `YYYY-MM-DD` |
| `publication` | string | Name of the news outlet or publishing organization |
| `submission_type` | string | One of: `case_study`, `investigative_article`, `opinion_piece`, `news_report` |
| `title` | string | Article title as published |
| `url` | string | Direct URL to the published article |
| `additional_urls` | array | Optional. Supplementary source URLs for the same case (follow-up coverage, related documents). Omit if there are none. |
| `jurisdiction` | string | Human-readable location where the incident occurred, as it should display (e.g. `"Kechi, KS"`, `"South Carolina"`, `"National"`, `"Eugene, OR / Evanston, IL / Cambridge, MA"` for multi-location entries). Free text — this is the display string, not a filter key. |
| `state` | string \| array \| null | Normalized USPS two-letter state code for filtering, aggregation, and the state heatmap. A single code (`"KS"`) for single-state entries, an array of codes (`["OR","IL","MA"]`) for entries spanning multiple states, or `null` for national/non-state-specific entries. Always fill this in when adding an entry — see Editorial Notes below. |
| `agency` | string | Law enforcement agency or entity involved |
| `abuse_categories` | array | One or more abuse category slugs from the controlled vocabulary in `_meta` (see CONTRIBUTING.md for definitions) |
| `description` | string | 1–3 sentence description of the documented incident |
| `status` | string | One of: `approved`, `pending`, `rejected`. Only `approved` entries render on the public site. |
| `date_added` | string | Optional. ISO 8601 date the entry was approved and added to the library. Older entries predating this field may omit it. |
| `submitted_by` | string | Optional. Name or handle of submitter. Omit if anonymous or self-curated. |
| `notes` | string | Optional. Editor notes — corrections made to submitter-provided data, sourcing caveats, categorization rationale. Not shown on the public site. |

## Editorial Notes

- **One entry per case, not per article.** A single source article covering multiple distinct officers, agencies, or jurisdictions gets one entry per case, sharing the same `url`. See `validate_library.py`, which treats this as expected (same `url` + different `jurisdiction`/`agency`) rather than flagging it as a duplicate.
- **`state` is required going forward.** It's a normalized filter key, not a duplicate of `jurisdiction` — fill it in at the same time you write `jurisdiction`, since you already know the state then. Run `validate_library.py` before committing; it checks `state` against the real USPS code list and will catch a missing or malformed value.

## Versioning

The `_meta.schema_version` field will increment if breaking changes are made to this schema. Non-breaking additions (new optional fields) will not increment the version.

| Version | Changes |
|---------|---------|
| `1.2` | Added `state` field (normalized USPS code, array, or null) alongside `jurisdiction`, for filtering, aggregation, and the state heatmap. Documentation also corrected to match the schema actually in use: `id` is a three-digit sequential string, not `YYYY-NNN`; `jurisdiction` is a single combined field, not split `jurisdiction_city`/`jurisdiction_state`; the categories key is `abuse_categories`, not `categories`; the description key is `description`, not `summary`; `status` and `additional_urls` were previously undocumented. |
| `1.1` | Renamed `headline` → `title`; added `submission_type` field |
| `1.0` | Initial schema |
