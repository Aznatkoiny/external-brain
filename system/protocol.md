---
type: protocol
title: Vault protocol
status: active
created: 2026-08-19
updated: 2026-08-19
tags:
  - system/protocol
---

# Vault protocol

This file defines how agents turn conversations and sources into durable knowledge. It is authoritative for vault behavior.

## Knowledge layers

1. **Raw sources** are immutable inputs: PDFs in `sources/papers/` and verbatim thoughts in `sources/thoughts/`.
2. **Source records** in `sources/records/` describe one raw source, its metadata, scope, limitations, and extracted takeaways.
3. **Atomic notes** in `notes/` hold one durable claim, concept, or question.
4. **Maps** in `maps/` organize a topic without pretending that hierarchy is the only relationship.
5. **Syntheses** in `syntheses/` answer cross-source questions and make agent reasoning explicit.

## Mutation contract

Before writing:

1. Identify whether the input is a personal observation, external source, question, or maintenance request.
2. Search `system/index.md`, filenames, aliases, and note contents for existing canonical pages.
3. Read the relevant existing pages and their cited sources.
4. Decide which pages need creation or revision. Avoid pages that merely repeat a source summary.

While writing:

- Preserve the raw input before synthesis.
- Make each claim note assert one proposition that can be supported, challenged, or revised.
- Link a term only when the target page helps a reader understand or navigate the statement.
- Explain semantic relationships in sentences using the vocabulary in [[system/relationships|Relationship vocabulary]].
- Preserve disagreement between sources. Do not silently average conflicting results.
- Set `status: agent-proposed` for new agent inferences and potential cross-source relationships.
- Use `confidence` only for agent inference, never as a substitute for evidence.

After writing:

1. Update `system/index.md` with new durable pages and a one-line description.
2. Append a parseable entry to `system/log.md`.
3. Add judgments requiring the user to `system/review-queue.md`.
4. Run `python3 scripts/vault_lint.py` and fix safe structural errors.
5. Summarize created, updated, and proposed relationships to the user.

## Source and citation rules

- Never alter a file in `sources/papers/` after ingestion. A replacement is a new source version.
- Record the PDF path and SHA-256 digest in its source record.
- Cite PDF evidence with `[[Paper filename.pdf#page=N|Author, year, p. N]]`.
- Page numbers refer to PDF pages as rendered by Obsidian. If printed page labels differ, say so in the source record.
- Use a short excerpt only when wording matters. Paraphrase otherwise.
- Inspect rendered pages for figures, equations, tables, multi-column ordering, or extraction ambiguity.
- A source record summarizes a paper; it is not itself evidence for a factual claim when the original PDF is available.

## Personal thought rules

- Preserve the user's wording in a dated file under `sources/thoughts/`.
- Separate verbatim text from an agent-written interpretation.
- Do not present a personal belief as an externally verified fact.
- A sensitive thought remains local; do not search for or transmit related information unless the user requests it.

## Write-back threshold

Write a chat result back when it adds durable value: a new supported claim, a clarified concept, a meaningful personal observation, an open research question, or a cross-source synthesis. Do not file greetings, operational chatter, or answers already represented without material improvement.
