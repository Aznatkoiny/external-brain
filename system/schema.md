---
type: protocol
title: Vault schema
status: active
created: 2026-08-19
updated: 2026-08-19
tags:
  - system/schema
---

# Vault schema

All durable notes use YAML properties followed by ordinary Obsidian Markdown. Filenames must be unique across the vault and human-readable so short wikilinks remain unambiguous.

## Shared properties

| Property | Meaning |
| --- | --- |
| `type` | `thought`, `source`, `claim`, `concept`, `question`, `map`, `synthesis`, or `protocol` |
| `title` | Canonical human-readable title |
| `status` | `active`, `agent-proposed`, `needs-review`, `superseded`, or `archived` |
| `created` | Creation date in `YYYY-MM-DD` |
| `updated` | Last meaningful revision date in `YYYY-MM-DD` |
| `aliases` | Alternative names that should resolve to this page |
| `tags` | A small set of navigation facets, not a replacement for links |

## Evidence properties

Claims and syntheses also declare:

| Property | Meaning |
| --- | --- |
| `evidence_kind` | `personal-observation`, `source-claim`, `agent-inference`, or `mixed` |
| `sources` | Wikilinks to source records or thought captures |
| `confidence` | Optional `low`, `medium`, or `high`; permitted only for inference |

Source records also declare:

| Property | Meaning |
| --- | --- |
| `source_type` | Usually `academic-paper`, but may be another explicit type |
| `file` | Vault-relative path to the immutable original |
| `sha256` | Lowercase SHA-256 digest of the original |
| `authors`, `year`, `doi` | Bibliographic values when verified; unknown values remain empty |

## Page responsibilities

- `thought`: verbatim user text plus a clearly labeled interpretation section.
- `source`: bibliographic record, structured summary, methods, findings, limitations, and PDF page links.
- `claim`: one proposition, evidence, qualifications, and relationships to other claims or concepts.
- `concept`: a stable explanation accumulated from several notes or sources; avoid turning it into a paper summary.
- `question`: an unresolved question, why it matters, and what evidence could answer it.
- `map`: a navigational view of a topic with annotated links.
- `synthesis`: an explicit argument across sources, with agreements, differences, uncertainties, and citations.

## Link style

- Use `[[Canonical filename]]` for internal notes.
- Use `[[Canonical filename|natural display text]]` when grammar requires it.
- Use `[[Paper.pdf#page=4|Author, year, p. 4]]` for PDF evidence.
- Embed only when the object should be visible inline: `![[figure.png]]` or `![[Paper.pdf#page=4]]`.
- Prefer a contextual sentence over a bare related-links list.

See [[system/relationships|Relationship vocabulary]] for semantic labels and [[system/protocol|Vault protocol]] for operating rules.
