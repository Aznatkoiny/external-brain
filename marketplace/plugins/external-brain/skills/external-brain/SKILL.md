---
name: external-brain
description: Use an External Brain Obsidian vault with an AI agent. Apply when the user wants to capture a thought, ingest an academic PDF, query relationships, or maintain the vault; do not use for unrelated repositories or ordinary file editing.
---

# External Brain

Operate the user's persistent knowledge graph through its own protocol instead of treating chat history as durable memory.

## Locate the vault

Work from the External Brain repository root containing `vault/system/protocol.md`, `vault/system/schema.md`, `vault/sources/`, `scripts/`, and `templates/`. If the current directory is not that repository, locate an explicitly provided repository path or ask the user to open the External Brain project. Do not initialize or modify an unrelated directory.

Read `vault/system/protocol.md` and `vault/system/schema.md` before any knowledge mutation. Read `vault/START HERE.md` when orienting a new user.

## Route the request

- A personal idea, observation, reflection, hypothesis, or request to remember something: use `vault-capture`.
- An academic paper, PDF attachment, paper comparison, or literature-integration request: use `vault-ingest-paper`.
- A question about accumulated knowledge or relationships across sources: use `vault-query`.
- Linting, deduplication, repair, provenance review, or organization: use `vault-maintain`.
- Obsidian-specific Markdown syntax: also use `obsidian-markdown`.

Load the routed skill completely and follow it. The routed skill owns the detailed workflow; do not invent a parallel note schema.

## Persistent inputs

An uploaded PDF or chat attachment is not yet durable. Before ingestion, preserve a byte-for-byte copy under `vault/sources/papers/`. Never overwrite an existing paper: reuse it when the hash matches, or use a distinct filename/version when the bytes differ.

Preserve personal thoughts verbatim under `vault/sources/thoughts/` before interpreting them. Do not file operational conversation as knowledge.

## Finish

Report what was created or updated, which relationships remain proposals, and any review items or lint findings. Keep the original source and Obsidian Markdown authoritative.
