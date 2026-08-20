---
type: protocol
title: Log
status: active
created: 2026-08-19
updated: 2026-08-19
tags:
  - system/log
---

# Log

Append entries newest-first using `## [YYYY-MM-DD] operation | Subject`.

## [2026-08-19] maintain | Isolate the Obsidian vault

- Moved the durable knowledge graph and `.obsidian` configuration into `vault/`, leaving agent skills, templates, scripts, and plugin packaging at the repository root.
- Updated agent routing and tooling so Codex and Claude operate from the repository root while Obsidian indexes only `vault/`.

## [2026-08-19] synthesize | Docling Graph integration

- Evaluated Docling Graph against the vault protocol and recorded a proposed sidecar architecture, integration seams, limitations, and phased pilot.

## [2026-08-19] initialize | External Brain vault

- Created the source-grounded vault structure, schemas, operation skills, and deterministic validation workflow.
