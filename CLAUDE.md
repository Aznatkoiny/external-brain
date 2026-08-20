# External Brain agent contract

This repository contains an Obsidian vault in `vault/`. Markdown in that directory is the durable knowledge layer.

Before changing vault knowledge, read `vault/system/protocol.md` and `vault/system/schema.md`, then read the applicable project skill:

- Personal thought or observation: `skills/vault-capture/SKILL.md`
- Academic paper or PDF: `skills/vault-ingest-paper/SKILL.md`
- Question against the vault: `skills/vault-query/SKILL.md`
- Vault health or organization: `skills/vault-maintain/SKILL.md`

For every Obsidian edit, also read `skills/obsidian-markdown/SKILL.md` and only the relevant referenced syntax guide.

Keep `vault/sources/papers/` immutable. Preserve user thoughts verbatim before synthesis. Distinguish personal observations, sourced claims, and agent inferences. Use page-level PDF citations, search before creating notes, explain links in prose, and send uncertain contradictions to human review. Run `python3 scripts/vault_lint.py` after meaningful mutations.
