# Contributing to the ALPR Abuse Library

## How Submissions Work

This library uses a **form-in, editor-out** workflow. You do not need a GitHub account to submit an article.

### Step 1 — Submit via Google Form

Use the [submission form](https://forms.gle/wL2LzXVJkSTSgbaR7) to submit an article. You'll be asked for:

| Field | Required | Notes |
|-------|----------|-------|
| Article URL | ✅ | Must be a published news article or official document |
| Article Title | ✅ | As published |
| Publication Name | ✅ | Name of the outlet |
| Date Published | ✅ | YYYY-MM-DD format preferred |
| Type of Submission | ✅ | e.g., Case Study, Investigative Article, Opinion Piece, News Report |
| City / Jurisdiction | ✅ | City or county where the incident occurred |
| State | ✅ | Drop-down list of all 50 states, DC, and other / international |
| Agency Involved | ✅ | e.g. "Wichita PD", "ICE", "Unknown" |
| Abuse Category | ✅ | Select all that apply (see categories below) |
| Brief Description | ✅ | 1–3 sentences summarizing the incident |
| Your Name | ⬜ | Optional |
| Your Email | ⬜ | Optional — only used for follow-up questions |

### Step 2 — Editorial Review

Submissions land in a private review queue. The editor (Kansas Watch) will:

- Verify the article exists and the URL is not paywalled
- Confirm the article documents a real incident, not speculation
- Check for duplicate entries
- Assign or confirm the abuse category

Most submissions are reviewed within 7 days. Approved entries are committed to `library.json` and the README index is updated.

### Step 3 — Publication

Once approved, the entry appears in:
- The README index table (visible on GitHub)
- `library.json` (machine-readable, for downstream use)

---

## Abuse Categories

| Category | Description |
|----------|-------------|
| `false_arrest` | ALPR data contributed to a wrongful arrest or misidentification |
| `stalking_targeting` | ALPR used to track an individual, including by intimate partners or officers |
| `data_breach` | ALPR data exposed, leaked, or accessed without authorization |
| `fusion_center_sharing` | Data shared with fusion centers or federal agencies without clear legal basis |
| `dragnet_surveillance` | Mass collection of vehicle movement data on populations not under investigation |
| `domestic_abuse_enablement` | ALPR used to locate victims of domestic violence or stalking |
| `immigration_enforcement` | ALPR data used in civil immigration enforcement |
| `protest_tracking` | ALPR deployed to monitor or identify protesters |
| `unauthorized_access` | Officers or employees accessing ALPR data outside their authority |
| `other` | Other civil liberties or abuse concerns not covered above |

---

## What We Don't Accept

- Unverified social media posts or screenshots
- Submissions without a working URL to a published source
- Opinion pieces that do not cite a documented incident
- Duplicate entries (check the library first)
- Content that targets private individuals not acting in a public capacity

---

## Questions?

Open an [Issue](../../issues) in this repo or contact us at [kansas.watch](https://kansas.watch).
