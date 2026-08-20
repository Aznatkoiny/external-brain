---
type: map
title: External Brain
status: active
created: 2026-08-19
updated: 2026-08-19
aliases:
  - Start here
tags:
  - system/navigation
---

# External Brain

This vault is a source-grounded, agent-maintained Zettelkasten for personal thinking and academic research.

## Use it with an AI agent

Open the `external-brain` repository root as the working project in Codex or Claude Code. Open only its `vault/` subfolder in Obsidian. The repository-level instructions make the agent follow the vault protocol while Obsidian indexes only the knowledge files.

The installable plugin under the repository's `marketplace/` directory packages the same workflows for Codex and Claude Code. Installation details are in `marketplace/README.md` outside this vault.

After opening the vault, you can say:

- "Remember this thought: ..."
- "Ingest the new PDF in `vault/sources/papers/`."
- "What relationships have we found across these papers?"
- "Review and repair my External Brain."

For a PDF, either copy it into the repository's `vault/sources/papers/` directory yourself or attach it and ask the agent to ingest it. An attached PDF is copied there before processing so it remains available after the chat ends. Inside Obsidian, this directory appears as `sources/papers/`.

## Start here

- Browse the topic map at [[Home]].
- Browse the complete catalog at [[system/index|Index]].
- Review unresolved judgments at [[system/review-queue|Review queue]].
- Inspect the maintenance history at [[system/log|Log]].

## Add knowledge

- Share a thought and ask the agent to capture it.
- Place an academic PDF in the repository's `vault/sources/papers/` directory and ask the agent to ingest it.
- Ask a question across the vault; durable cross-source conclusions may become a synthesis.

> [!important]
> Original PDFs and verbatim thought captures are source material. Agents build the linked notes around them without rewriting the originals.
