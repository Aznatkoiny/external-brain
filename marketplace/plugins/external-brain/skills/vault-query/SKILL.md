---
name: vault-query
description: Answer questions from the External Brain vault, including comparisons and relationships across papers, with traceable evidence. Use when the user asks what the vault knows; do not use merely to capture new material.
---

# Vault Query

Answer from accumulated knowledge first, then make durable insights compound without presenting inference as source fact.

## Required context

Read `vault/system/protocol.md`, `vault/system/schema.md`, and `skills/obsidian-markdown/SKILL.md`. For cross-source analysis, also read `vault/system/relationships.md` and `templates/synthesis.md`.

## Workflow

1. Read `vault/system/index.md`, then search filenames, aliases, and content under `vault/` with `rg`. Follow relevant links outward until the important claims and their sources are covered.
2. Inspect the source record and original cited PDF pages when wording, scope, methods, figures, or conflicting results matter. A wiki page is a navigation aid, not a substitute for evidence.
3. Answer with a direct conclusion, supporting evidence, meaningful disagreement, and remaining uncertainty. Use page-level links for paper-dependent statements.
4. Label novel cross-source conclusions as inference. Never cite one paper as supporting a claim it does not make.
5. Write back only if the answer adds durable value. Substantive cross-source analysis becomes `vault/syntheses/Question or topic.md` with `status: agent-proposed`; small corrections update the canonical page instead.
6. If writing back, update `vault/system/index.md` and `vault/system/log.md`, then run `python3 scripts/vault_lint.py`.

If evidence is insufficient, say what is missing and optionally create a question note. Do not fill a gap with general model memory unless the user explicitly permits external research.
