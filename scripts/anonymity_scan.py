"""Scan tracked-style text files for common identity, path, and secret leaks."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
import re
import sys
from typing import Iterable


TEXT_SUFFIXES = {
    ".cfg",
    ".csv",
    ".ini",
    ".json",
    ".md",
    ".py",
    ".tex",
    ".toml",
    ".tsv",
    ".txt",
    ".yaml",
    ".yml",
}
SKIP_PARTS = {".git", ".pytest_cache", ".venv", "__pycache__", "results", "outputs"}


@dataclass(frozen=True)
class Finding:
    path: Path
    line: int
    category: str
    excerpt: str


def _patterns() -> dict[str, re.Pattern[str]]:
    at_sign = "@"
    email = r"\b[A-Z0-9._%+-]+" + at_sign + r"[A-Z0-9.-]+\.[A-Z]{2,}\b"
    win_root = r"[A-Za-z]:[\\/]" + r"Users[\\/][^\\/\s]+[\\/]"
    unix_home = r"/(?:home|Users)/" + r"[^/\s]+/"
    github_token = r"gh" + r"[pousr]_[A-Za-z0-9_]{20,}"
    openai_key = r"sk" + r"-[A-Za-z0-9_-]{20,}"
    return {
        "email": re.compile(email, re.IGNORECASE),
        "absolute-user-path": re.compile(f"(?:{win_root}|{unix_home})"),
        "github-token": re.compile(github_token),
        "api-key": re.compile(openai_key),
        "private-key-header": re.compile("BEGIN " + "PRIVATE KEY"),
    }


def iter_text_files(root: Path) -> Iterable[Path]:
    for path in root.rglob("*"):
        if not path.is_file() or any(part in SKIP_PARTS for part in path.parts):
            continue
        if path.suffix.lower() in TEXT_SUFFIXES or path.name in {".gitignore"}:
            yield path


def scan(root: Path, forbidden_terms: Iterable[str] = ()) -> list[Finding]:
    patterns = _patterns()
    terms = tuple(term for term in forbidden_terms if term)
    findings: list[Finding] = []
    for path in iter_text_files(root):
        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except UnicodeDecodeError:
            continue
        for line_number, line in enumerate(lines, start=1):
            for category, pattern in patterns.items():
                if pattern.search(line):
                    findings.append(
                        Finding(path, line_number, category, line.strip()[:200])
                    )
            lowered = line.casefold()
            for term in terms:
                if term.casefold() in lowered:
                    findings.append(
                        Finding(
                            path,
                            line_number,
                            "configured-identity-term",
                            line.strip()[:200],
                        )
                    )
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", default=".", type=Path)
    parser.add_argument(
        "--forbidden-term",
        action="append",
        default=[],
        help="Additional identity string to reject (repeatable).",
    )
    args = parser.parse_args()
    findings = scan(args.root.resolve(), args.forbidden_term)
    if findings:
        for finding in findings:
            try:
                display_path = finding.path.relative_to(args.root.resolve())
            except ValueError:
                display_path = finding.path
            print(
                f"{display_path}:{finding.line}: {finding.category}: {finding.excerpt}",
                file=sys.stderr,
            )
        print(f"Anonymity scan failed with {len(findings)} finding(s).", file=sys.stderr)
        return 1
    print("Anonymity scan passed: no configured identity, local-path, or secret leaks found.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
