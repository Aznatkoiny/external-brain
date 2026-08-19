---
name: vault-capture
description: Capture a user's personal observation, idea, reflection, hypothesis, or explicit request to remember something in the External Brain vault. Do not use for incidental operational conversation or external documents.
---

# Vault Capture

Turn a thought into a preserved source plus the smallest useful set of connected durable notes.

## Required context

Read `system/protocol.md`, `system/schema.md`, `templates/thought.md`, and `skills/obsidian-markdown/SKILL.md`. Read relevant existing pages before editing them.

## Workflow

1. Search the index, aliases, filenames, and content for concepts or questions implicated by the thought.
2. Create `sources/thoughts/YYYY-MM-DD - Short descriptive title.md`. Preserve the user's material verbatim; clearly label any cleanup such as removed filler or corrected transcription.
3. Add an agent interpretation that distinguishes observation, belief, hypothesis, preference, and open question. Do not add external validation unless the user requested research.
4. Update existing concept or question pages when the thought materially changes them. Create a new atomic page only for a durable idea with a distinct identity.
5. Use `evidence_kind: personal-observation` for claims derived only from the user's thought. Use `agent-inference` for relationships the agent proposes.
6. Explain each important wikilink in a sentence. Add uncertain semantic judgments to `system/review-queue.md`.
7. Update `system/index.md` and prepend a `capture` entry to `system/log.md`.
8. Run `python3 scripts/vault_lint.py`.

Do not capture the user's approval of tooling, file operations, greetings, or other session mechanics as knowledge.
