---
name: vault-ingest-paper
description: Ingest, compare, or integrate an academic PDF into the External Brain vault with immutable source handling, page-level citations, atomic claims, and cross-paper links. Use for papers and PDF-based research, not ordinary Markdown articles.
---

# Vault Ingest Paper

Compile an academic paper into source-grounded notes while preserving the original and the difference between reported findings and agent inference.

## Required context

Read `vault/system/protocol.md`, `vault/system/schema.md`, `vault/system/relationships.md`, `templates/source-record.md`, and `skills/obsidian-markdown/SKILL.md`. Use the environment's PDF skill when available.

## Prepare the source

1. Ensure the original is under `vault/sources/papers/`. If the user supplied an attachment or a path outside the vault, preserve a byte-for-byte copy there first. Never overwrite an existing filename: reuse it when the SHA-256 matches, or use a distinct filename/version when the bytes differ. Do not alter it after ingestion.
2. Run `python3 scripts/extract_pdf.py "vault/sources/papers/Paper.pdf"`. Reuse the hash-addressed extraction if reported.
3. Read the extracted page-delimited Markdown. Render and inspect pages containing figures, tables, equations, unusual layouts, or suspicious extraction with `--render-pages`.
4. Verify title, authors, year, DOI, and page mapping from the paper. Leave unknown metadata empty.

## Integrate knowledge

1. Search the vault for the paper, its central concepts, methods, datasets, and claimed contributions.
2. Create one source record under `vault/sources/records/` from `templates/source-record.md`; store the PDF path and exact SHA-256.
3. Create or update only durable atomic claims, concepts, and questions. A source summary alone does not justify duplicating every section as a note.
4. Cite reported claims directly to PDF pages. Cite method, population, and experimental conditions when they qualify a result.
5. Compare against relevant existing claims. Describe `supports`, `challenges`, `extends`, or other relationships with their basis and citations.
6. Mark cross-source reasoning not stated by a source as `evidence_kind: agent-inference` and `status: agent-proposed`.
7. Put possible contradictions in `vault/system/review-queue.md` as `potential-conflict`; do not resolve them autonomously.
8. Update `vault/maps/`, `vault/system/index.md`, and `vault/system/log.md`, then run `python3 scripts/vault_lint.py`.

For batch ingestion, process one paper to a coherent diff at a time so provenance and revisions remain reviewable.
