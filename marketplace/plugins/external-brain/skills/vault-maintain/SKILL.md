---
name: vault-maintain
description: Inspect, lint, organize, deduplicate, or repair the External Brain vault. Use for broken links, orphan notes, stale pages, duplicate concepts, provenance gaps, and semantic review; not for ordinary capture or paper ingestion.
---

# Vault Maintain

Keep the graph structurally valid and semantically honest while preserving source material and human judgments.

## Required context

Read `vault/system/protocol.md`, `vault/system/schema.md`, `vault/system/relationships.md`, and `skills/obsidian-markdown/SKILL.md`.

## Workflow

1. Run `python3 scripts/vault_lint.py --json tmp/vault-lint.json` for deterministic findings.
2. Review warnings that need semantics: synonym pages, weakly explained links, unsupported inference, stale syntheses, missing concepts, or potential conflicts.
3. Auto-fix safe structural issues such as an index omission or an unambiguous broken path. Do not merge distinct concepts merely because their titles look similar.
4. Never edit an original PDF. If a recorded source hash changed, stop and report the drift rather than updating the recorded hash.
5. Move possible contradictions, ambiguous merges, and vocabulary changes to `vault/system/review-queue.md`. Only the user confirms these judgments.
6. Preserve useful redirects with `aliases` when consolidating pages, and update contextual links rather than adding noisy reciprocal lists.
7. Append a `maintain` entry to `vault/system/log.md`, update affected timestamps, and rerun the linter.

Report deterministic errors separately from semantic suggestions. A clean lint run does not prove that the knowledge is true.
