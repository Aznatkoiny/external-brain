# External Brain agent contract

This repository is an Obsidian vault maintained collaboratively by the user and AI agents. Markdown is the durable knowledge layer; chat history is not.

## Mandatory routing

Before mutating vault knowledge, read `system/protocol.md` and `system/schema.md` completely, then load the matching skill:

- A personal observation, idea, reflection, or request to remember something: `skills/vault-capture/SKILL.md`
- An academic paper or PDF to process, compare, or integrate: `skills/vault-ingest-paper/SKILL.md`
- A question to answer from accumulated knowledge: `skills/vault-query/SKILL.md`
- Organizing, linting, deduplicating, repairing, or reviewing the vault: `skills/vault-maintain/SKILL.md`

Whenever editing Obsidian files, also read `skills/obsidian-markdown/SKILL.md`. Only load its references needed for the current syntax.

Operational conversation is not automatically knowledge. Capture it only when the user presents it as a thought, evidence, question, or material for the vault.

## Non-negotiable boundaries

- Treat files in `sources/papers/` as immutable originals.
- Preserve personal thoughts verbatim in `sources/thoughts/` before synthesizing them.
- Separate `personal-observation`, `source-claim`, and `agent-inference` in note metadata.
- Cite paper claims to the PDF and page. Never invent a page, quote, DOI, author, or relationship.
- Search for an existing page before creating one. Prefer updating a canonical page over creating a synonym.
- Describe why two notes are related in prose. A bare wikilink is not a semantic relationship.
- Record possible contradictions as review candidates; do not promote them to fact without human review.
- Run `python3 scripts/vault_lint.py` after a meaningful knowledge mutation and report any remaining warnings.
