# External Brain plugin

This skills-only plugin teaches Codex and Claude Code how to operate an External Brain vault. The vault remains ordinary Obsidian Markdown; the plugin supplies the capture, paper-ingestion, query, maintenance, and Markdown workflows.

## Codex installation

From the repository root, run:

```bash
codex plugin marketplace add "$(pwd)/marketplace"
codex plugin add external-brain@external-brain
```

Start a new Codex conversation with the repository root selected as the project. Open `vault/` separately in Obsidian.

## Claude Code installation

From the repository root, run:

```bash
claude plugin marketplace add "$(pwd)"
claude plugin install external-brain@external-brain --scope user
```

Restart Claude Code, or test the source directly during development:

```bash
claude --plugin-dir "$(pwd)/marketplace/plugins/external-brain"
```

Claude exposes explicit commands under the `external-brain` namespace and may also select the skills automatically from their descriptions.

## Daily use

Open the repository root in the agent. Open its `vault/` subfolder in Obsidian. Then use natural language, for example:

- "Remember this thought: retrieval quality depends on question quality."
- "Ingest the PDF I attached into my External Brain."
- "Compare the methods and findings across these three papers."
- "Lint the vault and show me anything that needs review."

For a PDF, copying it to `vault/sources/papers/` is the most explicit path. If it is attached in chat, the workflow first preserves a byte-for-byte copy there. The agent never treats the temporary chat attachment as the durable source.

## What the plugin does not contain

It does not bundle an AI model, upload service, vector database, or graph database. Codex or Claude supplies the agent runtime; Obsidian Markdown remains the durable knowledge layer.
