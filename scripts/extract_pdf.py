#!/usr/bin/env python3
"""Extract an immutable academic PDF into hash-addressed, page-aware text."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
VAULT_ROOT = REPO_ROOT / "vault"
PAPERS_ROOT = (VAULT_ROOT / "sources" / "papers").resolve()


def fail(message: str) -> "NoReturn":
    print(f"error: {message}", file=sys.stderr)
    raise SystemExit(2)


def require_tool(name: str) -> str:
    path = shutil.which(name)
    if path is None:
        fail(f"required tool '{name}' is not installed")
    return path


def run(command: list[str]) -> subprocess.CompletedProcess[str]:
    try:
        return subprocess.run(command, check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as exc:
        detail = (exc.stderr or exc.stdout or "unknown command failure").strip()
        fail(f"{Path(command[0]).name} failed: {detail}")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def safe_stem(value: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9]+", "-", value).strip("-").lower()
    return cleaned[:80] or "paper"


def parse_pdfinfo(raw: str) -> dict[str, str]:
    result: dict[str, str] = {}
    for line in raw.splitlines():
        key, separator, value = line.partition(":")
        if separator:
            result[key.strip()] = value.strip()
    return result


def parse_page_spec(spec: str, page_count: int) -> list[int]:
    if not spec:
        return []
    if spec.lower() == "all":
        return list(range(1, page_count + 1))

    pages: set[int] = set()
    for part in spec.split(","):
        token = part.strip()
        if not token:
            continue
        if "-" in token:
            start_text, end_text = token.split("-", 1)
            if not start_text.isdigit() or not end_text.isdigit():
                fail(f"invalid page range '{token}'")
            start, end = int(start_text), int(end_text)
            if start > end:
                fail(f"descending page range '{token}' is not allowed")
            pages.update(range(start, end + 1))
        elif token.isdigit():
            pages.add(int(token))
        else:
            fail(f"invalid page value '{token}'")

    invalid = sorted(page for page in pages if page < 1 or page > page_count)
    if invalid:
        fail(f"page values outside 1-{page_count}: {invalid}")
    return sorted(pages)


def extract(input_path: Path, output_dir: Path, digest: str) -> tuple[int, dict[str, str]]:
    pdftotext = require_tool("pdftotext")
    pdfinfo = require_tool("pdfinfo")

    info_result = run([pdfinfo, str(input_path)])
    info = parse_pdfinfo(info_result.stdout)

    text_result = run([pdftotext, "-layout", "-enc", "UTF-8", str(input_path), "-"])
    raw_pages = text_result.stdout.replace("\x00", "").split("\f")
    if raw_pages and not raw_pages[-1].strip():
        raw_pages.pop()
    if not raw_pages:
        raw_pages = [""]

    output_dir.mkdir(parents=True, exist_ok=True)
    pages_dir = output_dir / "pages"
    pages_dir.mkdir(exist_ok=True)

    document_sections = [f"# Extracted text: {input_path.name}", ""]
    for number, page_text in enumerate(raw_pages, start=1):
        cleaned = page_text.rstrip()
        page_file = pages_dir / f"page-{number:04d}.txt"
        page_file.write_text(cleaned + "\n", encoding="utf-8")
        document_sections.extend([f"## PDF page {number}", "", cleaned, ""])

    (output_dir / "document.md").write_text("\n".join(document_sections), encoding="utf-8")

    metadata = {
        "source": input_path.relative_to(VAULT_ROOT).as_posix(),
        "sha256": digest,
        "page_count": len(raw_pages),
        "text_extractor": "pdftotext -layout",
        "pdfinfo": info,
    }
    (output_dir / "metadata.json").write_text(
        json.dumps(metadata, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    return len(raw_pages), info


def render_pages(input_path: Path, output_dir: Path, pages: list[int]) -> None:
    if not pages:
        return
    pdftoppm = require_tool("pdftoppm")
    images_dir = output_dir / "images"
    images_dir.mkdir(exist_ok=True)
    for page in pages:
        prefix = images_dir / f"page-{page:04d}"
        run(
            [
                pdftoppm,
                "-f",
                str(page),
                "-l",
                str(page),
                "-r",
                "160",
                "-png",
                "-singlefile",
                str(input_path),
                str(prefix),
            ]
        )


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Extract a vault PDF to tmp/pdfs with stable page boundaries and optional rendered pages."
    )
    parser.add_argument("pdf", type=Path, help="PDF under vault/sources/papers/")
    parser.add_argument(
        "--render-pages",
        default="",
        metavar="SPEC",
        help="Comma-separated PDF pages/ranges (for example 1,3-5) or 'all'",
    )
    args = parser.parse_args()

    input_path = args.pdf.expanduser().resolve()
    if not input_path.is_file():
        fail(f"PDF not found: {input_path}")
    if input_path.suffix.lower() != ".pdf":
        fail(f"source does not have a .pdf extension: {input_path.name}")
    if not input_path.is_relative_to(PAPERS_ROOT):
        fail("PDF must be stored under vault/sources/papers/ before extraction")

    digest = sha256_file(input_path)
    output_dir = REPO_ROOT / "tmp" / "pdfs" / f"{safe_stem(input_path.stem)}-{digest[:12]}"
    metadata_path = output_dir / "metadata.json"

    reused = False
    if metadata_path.is_file() and (output_dir / "document.md").is_file():
        metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
        if metadata.get("sha256") == digest:
            page_count = int(metadata["page_count"])
            reused = True
        else:
            fail(f"hash-addressed extraction has inconsistent metadata: {output_dir}")
    else:
        page_count, _ = extract(input_path, output_dir, digest)

    pages = parse_page_spec(args.render_pages, page_count)
    render_pages(input_path, output_dir, pages)

    result = {
        "source": input_path.relative_to(VAULT_ROOT).as_posix(),
        "sha256": digest,
        "page_count": page_count,
        "output_dir": output_dir.relative_to(REPO_ROOT).as_posix(),
        "rendered_pages": pages,
        "reused": reused,
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
