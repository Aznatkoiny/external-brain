#!/usr/bin/env python3
"""Deterministic structural and provenance checks for the External Brain vault."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from collections import defaultdict
from dataclasses import asdict, dataclass
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
VAULT_ROOT = REPO_ROOT / "vault"
CONTENT_ROOTS = (
    "sources/records",
    "sources/thoughts",
    "notes",
    "maps",
    "syntheses",
    "system",
)
ROOT_CONTENT_FILES = ("START HERE.md",)
IGNORED_PARTS = {".obsidian"}
COMMON_FIELDS = {"type", "title", "status", "created", "updated", "tags"}
LINK_RE = re.compile(r"!?\[\[([^\]]+)\]\]")
LOG_HEADING_RE = re.compile(r"^## \[\d{4}-\d{2}-\d{2}\] [a-z-]+ \| .+$", re.MULTILINE)


@dataclass(frozen=True)
class Finding:
    severity: str
    code: str
    path: str
    message: str


def relative(path: Path) -> str:
    return path.relative_to(VAULT_ROOT).as_posix()


def content_files() -> list[Path]:
    files: set[Path] = set()
    for root_name in CONTENT_ROOTS:
        root = VAULT_ROOT / root_name
        if root.exists():
            files.update(path for path in root.rglob("*.md") if path.is_file())
    for file_name in ROOT_CONTENT_FILES:
        path = VAULT_ROOT / file_name
        if path.is_file():
            files.add(path)
    return sorted(files)


def linkable_files() -> list[Path]:
    result: list[Path] = []
    for path in VAULT_ROOT.rglob("*"):
        if not path.is_file() or any(part in IGNORED_PARTS for part in path.relative_to(VAULT_ROOT).parts):
            continue
        if path.name in {"AGENTS.md", "CLAUDE.md"}:
            continue
        if path.suffix.lower() in {".md", ".pdf", ".png", ".jpg", ".jpeg", ".svg", ".canvas", ".base"}:
            result.append(path)
    return sorted(result)


def parse_frontmatter(text: str) -> dict[str, str] | None:
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---\n", 4)
    if end == -1:
        return None
    fields: dict[str, str] = {}
    for line in text[4:end].splitlines():
        if line[:1].isspace() or ":" not in line:
            continue
        key, value = line.split(":", 1)
        fields[key.strip()] = value.strip().strip('"').strip("'")
    return fields


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def expected_type(path: Path) -> str | None:
    rel = relative(path)
    if rel.startswith("sources/records/"):
        return "source"
    if rel.startswith("sources/thoughts/"):
        return "thought"
    if rel.startswith("notes/claims/"):
        return "claim"
    if rel.startswith("notes/concepts/"):
        return "concept"
    if rel.startswith("notes/questions/"):
        return "question"
    if rel.startswith("maps/") or rel == "START HERE.md":
        return "map"
    if rel.startswith("syntheses/"):
        return "synthesis"
    return None


def normalized_link_target(raw: str) -> str:
    target = raw.split("|", 1)[0].strip()
    target = target.split("#", 1)[0].strip()
    return target.removesuffix(".md").strip("/")


def prose_for_link_checks(text: str) -> str:
    """Remove Markdown code where wikilink syntax is illustrative, not active."""
    without_fences = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
    return re.sub(r"`[^`\n]*`", "", without_fences)


def build_link_indexes(files: list[Path]) -> tuple[dict[str, list[Path]], dict[str, list[Path]]]:
    by_name: dict[str, list[Path]] = defaultdict(list)
    by_path: dict[str, list[Path]] = defaultdict(list)
    for path in files:
        rel = relative(path)
        name_key = path.name.casefold() if path.suffix.lower() != ".md" else path.stem.casefold()
        path_key = rel.casefold()
        if path.suffix.lower() == ".md":
            path_key = path_key.removesuffix(".md")
        by_name[name_key].append(path)
        by_path[path_key].append(path)
    return by_name, by_path


def resolve_link(
    raw_target: str, by_name: dict[str, list[Path]], by_path: dict[str, list[Path]]
) -> tuple[str, Path | None]:
    target = normalized_link_target(raw_target)
    if not target:
        return "local-anchor", None
    path_matches = by_path.get(target.casefold(), [])
    if len(path_matches) == 1:
        return "ok", path_matches[0]
    if len(path_matches) > 1:
        return "ambiguous", None
    basename = Path(target).name
    name_key = basename.casefold()
    if not Path(basename).suffix:
        name_key = basename.casefold()
    name_matches = by_name.get(name_key, [])
    if len(name_matches) == 1:
        return "ok", name_matches[0]
    if len(name_matches) > 1:
        return "ambiguous", None
    return "missing", None


def lint() -> list[Finding]:
    findings: list[Finding] = []
    markdown_files = content_files()
    all_linkable = linkable_files()
    by_name, by_path = build_link_indexes(all_linkable)
    graph: dict[Path, set[Path]] = defaultdict(set)

    markdown_stems: dict[str, list[Path]] = defaultdict(list)
    for path in markdown_files:
        markdown_stems[path.stem.casefold()].append(path)
    for paths in markdown_stems.values():
        if len(paths) > 1:
            joined = ", ".join(relative(path) for path in paths)
            for path in paths:
                findings.append(Finding("error", "duplicate-title", relative(path), f"duplicate filename stem: {joined}"))

    for path in markdown_files:
        rel = relative(path)
        text = path.read_text(encoding="utf-8")
        fields = parse_frontmatter(text)
        if fields is None:
            findings.append(Finding("error", "frontmatter", rel, "missing or unterminated YAML frontmatter"))
            fields = {}
        else:
            missing = sorted(COMMON_FIELDS - fields.keys())
            if missing:
                findings.append(Finding("error", "required-fields", rel, f"missing properties: {', '.join(missing)}"))

            wanted_type = expected_type(path)
            if wanted_type and fields.get("type") != wanted_type:
                findings.append(
                    Finding("error", "note-type", rel, f"expected type '{wanted_type}', found '{fields.get('type', '')}'")
                )

            if fields.get("type") in {"claim", "synthesis"}:
                evidence_missing = sorted({"evidence_kind", "sources"} - fields.keys())
                if evidence_missing:
                    findings.append(
                        Finding("error", "evidence-fields", rel, f"missing evidence properties: {', '.join(evidence_missing)}")
                    )

            if fields.get("type") == "source":
                source_missing = sorted({"source_type", "file", "sha256"} - fields.keys())
                if source_missing:
                    findings.append(
                        Finding("error", "source-fields", rel, f"missing source properties: {', '.join(source_missing)}")
                    )
                else:
                    source_path = (VAULT_ROOT / fields["file"]).resolve()
                    if not source_path.is_relative_to((VAULT_ROOT / "sources" / "papers").resolve()):
                        findings.append(Finding("error", "source-path", rel, "source file must be under sources/papers/"))
                    elif not source_path.is_file():
                        findings.append(Finding("error", "source-missing", rel, f"source file not found: {fields['file']}"))
                    elif not re.fullmatch(r"[0-9a-f]{64}", fields["sha256"]):
                        findings.append(Finding("error", "source-hash-format", rel, "sha256 must be 64 lowercase hex characters"))
                    elif sha256_file(source_path) != fields["sha256"]:
                        findings.append(Finding("error", "source-hash-drift", rel, "source PDF hash differs from recorded sha256"))

        for raw in LINK_RE.findall(prose_for_link_checks(text)):
            target = normalized_link_target(raw)
            if not target:
                continue
            status, resolved = resolve_link(raw, by_name, by_path)
            if status == "missing":
                findings.append(Finding("error", "broken-link", rel, f"unresolved wikilink: [[{raw}]]"))
            elif status == "ambiguous":
                findings.append(Finding("error", "ambiguous-link", rel, f"ambiguous wikilink: [[{raw}]]"))
            elif resolved is not None:
                graph[path].add(resolved)
                graph[resolved].add(path)

        if fields.get("type") == "claim" and fields.get("evidence_kind") == "source-claim":
            if not re.search(r"\[\[[^\]]+\.pdf#page=\d+", text, re.IGNORECASE):
                findings.append(
                    Finding("error", "page-citation", rel, "source-claim must include at least one PDF #page=N wikilink")
                )

    durable_prefixes = ("sources/records/", "notes/", "maps/", "syntheses/")
    for path in markdown_files:
        rel = relative(path)
        if rel.startswith(durable_prefixes) and not graph.get(path):
            findings.append(Finding("warning", "orphan", rel, "durable page has no inbound or outbound wikilinks"))

    log_path = VAULT_ROOT / "system" / "log.md"
    if log_path.is_file():
        log_text = log_path.read_text(encoding="utf-8")
        operation_headings = [line for line in log_text.splitlines() if line.startswith("## [")]
        for heading in operation_headings:
            if not LOG_HEADING_RE.fullmatch(heading):
                findings.append(Finding("error", "log-format", "system/log.md", f"invalid log heading: {heading}"))

    return sorted(findings, key=lambda item: (item.severity != "error", item.path, item.code, item.message))


def main() -> int:
    parser = argparse.ArgumentParser(description="Check vault links, schemas, provenance, and source immutability.")
    parser.add_argument("--json", type=Path, help="also write a JSON report to this path")
    parser.add_argument("--strict", action="store_true", help="treat warnings as failures")
    args = parser.parse_args()

    findings = lint()
    errors = sum(item.severity == "error" for item in findings)
    warnings = sum(item.severity == "warning" for item in findings)

    if findings:
        for item in findings:
            print(f"{item.severity.upper():7} {item.code:20} {item.path}: {item.message}")
    print(f"vault lint: {errors} error(s), {warnings} warning(s)")

    if args.json:
        output_path = args.json if args.json.is_absolute() else REPO_ROOT / args.json
        output_path.parent.mkdir(parents=True, exist_ok=True)
        payload = {"errors": errors, "warnings": warnings, "findings": [asdict(item) for item in findings]}
        output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    return 1 if errors or (args.strict and warnings) else 0


if __name__ == "__main__":
    raise SystemExit(main())
