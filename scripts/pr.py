#!/usr/bin/env python3
"""Create and verify Lila pull requests against the Lila repository.

The Lila repository used to be a GitHub fork of `78/xiaozhi-esp32`, and a pull
request was once opened against that upstream project by mistake. The target is
therefore never a dropdown choice: it is always the repository configured in the
`origin` remote, and the upstream is refused outright.

Usage:

    python scripts/pr.py check              # report and validate the local target
    python scripts/pr.py check --pr 1       # validate an existing pull request
    python scripts/pr.py open --title "chore: ..." [--body-file notes.md]

A token is read from `GITHUB_TOKEN` or `GH_TOKEN` for the commands that talk to
the GitHub API. It is never printed and never written to disk.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

LILA_REPOSITORY = "mauricioz/lila"
UPSTREAM_REPOSITORY = "78/xiaozhi-esp32"
DEFAULT_BASE = "main"
API_ROOT = "https://api.github.com"

REMOTE_PATTERNS = (
    re.compile(r"^https?://[^/]+/(?P<owner>[^/]+)/(?P<name>[^/]+?)(?:\.git)?/?$"),
    re.compile(r"^ssh://git@[^/]+/(?P<owner>[^/]+)/(?P<name>[^/]+?)(?:\.git)?/?$"),
    re.compile(r"^git@[^:]+:(?P<owner>[^/]+)/(?P<name>[^/]+?)(?:\.git)?$"),
)


def parse_repository_slug(url: str) -> str | None:
    """Return ``owner/name`` for a GitHub remote URL, or None when unknown."""
    url = (url or "").strip()
    for pattern in REMOTE_PATTERNS:
        match = pattern.match(url)
        if match:
            return f"{match.group('owner')}/{match.group('name')}"
    return None


def git_command(root: Path, *arguments: str) -> list[str]:
    """Build a git command line that trusts exactly this checkout."""
    return ["git", "-c", f"safe.directory={root.as_posix()}", *arguments]


def git_output(root: Path, *arguments: str) -> str:
    """Run a read-only git command, trusting the checkout we were pointed at.

    CI containers often check the repository out as a different user, which
    makes git refuse to read it ("dubious ownership"). Declaring this exact
    directory as safe keeps the tool working there; no other directory is
    trusted.
    """
    result = subprocess.run(
        git_command(root, *arguments),
        cwd=root,
        capture_output=True,
        check=False,
        text=True,
    )
    if result.returncode != 0:
        return ""
    return result.stdout.strip()


def origin_slug(root: Path, remote: str = "origin") -> str | None:
    """Return ``owner/name`` for the configured remote."""
    return parse_repository_slug(git_output(root, "remote", "get-url", remote))


def current_branch(root: Path) -> str:
    """Return the checked-out branch name (empty when detached)."""
    return git_output(root, "rev-parse", "--abbrev-ref", "HEAD")


def validate_target(slug: str | None, branch: str, base: str) -> list[str]:
    """Return the reasons why this pull request target is not allowed."""
    problems: list[str] = []
    if not slug:
        problems.append(
            "cannot resolve the target repository from the 'origin' remote"
        )
    elif slug == UPSTREAM_REPOSITORY:
        problems.append(
            f"refusing to target {UPSTREAM_REPOSITORY}: Lila pull requests "
            f"target {LILA_REPOSITORY}:{base}"
        )
    if not branch:
        problems.append("no branch is checked out")
    elif branch == base:
        problems.append(
            f"the current branch is '{branch}': create a feature branch "
            f"(devs/<user>/<type>/<slug>) before opening a pull request"
        )
    return problems


def build_payload(
    slug: str, branch: str, base: str, title: str, body: str
) -> dict[str, str]:
    """Build the JSON payload for the GitHub pull request API."""
    return {
        "title": title,
        "head": branch,
        "base": base,
        "body": body,
    }


def read_token() -> str | None:
    """Read the API token from the environment."""
    for name in ("GITHUB_TOKEN", "GH_TOKEN"):
        value = os.environ.get(name, "").strip()
        if value:
            return value
    return None


def api_request(
    method: str, url: str, token: str, payload: dict[str, str] | None = None
) -> dict:
    """Call the GitHub API and return the decoded JSON response."""
    data = None
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(url, data=data, method=method)
    request.add_header("Authorization", f"Bearer {token}")
    request.add_header("Accept", "application/vnd.github+json")
    request.add_header("User-Agent", "lila-pr")
    request.add_header("X-GitHub-Api-Version", "2022-11-28")
    if data is not None:
        request.add_header("Content-Type", "application/json; charset=utf-8")
    try:
        with urllib.request.urlopen(request) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as error:
        detail = error.read().decode("utf-8", errors="replace")
        message = detail
        try:
            message = json.loads(detail).get("message", detail)
        except json.JSONDecodeError:
            pass
        raise SystemExit(f"GitHub API returned {error.code}: {message}") from error
    except urllib.error.URLError as error:
        raise SystemExit(f"cannot reach the GitHub API: {error.reason}") from error


def open_pull_request(
    slug: str, branch: str, base: str, title: str, body: str, token: str
) -> str:
    """Create the pull request and return its URL."""
    payload = build_payload(slug, branch, base, title, body)
    response = api_request(
        "POST", f"{API_ROOT}/repos/{slug}/pulls", token, payload
    )
    return str(response.get("html_url", ""))


def fetch_pull_request(slug: str, number: int, token: str) -> dict:
    return api_request("GET", f"{API_ROOT}/repos/{slug}/pulls/{number}", token)


def check_pull_request(slug: str, number: int, base: str, token: str) -> list[str]:
    """Return the reasons why an existing pull request has the wrong target."""
    pull = fetch_pull_request(slug, number, token)
    problems: list[str] = []
    base_repository = (pull.get("base") or {}).get("repo", {}).get("full_name", "")
    base_ref = (pull.get("base") or {}).get("ref", "")
    if base_repository != slug:
        problems.append(
            f"pull request #{number} targets {base_repository or 'an unknown repository'}"
        )
    if base_ref != base:
        problems.append(f"pull request #{number} targets the '{base_ref}' branch")
    return problems


def command_check(args: argparse.Namespace) -> int:
    slug = origin_slug(args.root, args.remote)
    branch = current_branch(args.root)
    problems = validate_target(slug, branch, args.base)

    print(f"repository : {slug or 'unknown'}")
    print(f"branch     : {branch or 'unknown'}")
    print(f"target     : {slug}:{args.base}" if slug else "target     : unknown")

    if args.pull_request is not None:
        token = read_token()
        if token is None:
            problems.append(
                "GITHUB_TOKEN or GH_TOKEN is required to read an existing pull request"
            )
        else:
            if not slug:
                problems.append("cannot check a pull request without a target repository")
            else:
                problems.extend(
                    check_pull_request(slug, args.pull_request, args.base, token)
                )

    if problems:
        print("pull request target is not valid:", file=sys.stderr)
        for problem in problems:
            print(f"  - {problem}", file=sys.stderr)
        return 1

    print(f"OK: pull requests must target {slug}:{args.base}")
    return 0


def command_open(args: argparse.Namespace) -> int:
    slug = origin_slug(args.root, args.remote)
    branch = current_branch(args.root)
    problems = validate_target(slug, branch, args.base)
    if problems:
        print("refusing to open the pull request:", file=sys.stderr)
        for problem in problems:
            print(f"  - {problem}", file=sys.stderr)
        return 1

    token = read_token()
    if token is None:
        print(
            "GITHUB_TOKEN or GH_TOKEN is required to open a pull request",
            file=sys.stderr,
        )
        return 1

    body = ""
    if args.body_file:
        body = Path(args.body_file).read_text(encoding="utf-8")

    url = open_pull_request(
        slug, branch, args.base, args.title, body, token
    )
    print(url)
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        type=Path,
        default=ROOT,
        help=argparse.SUPPRESS,
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    check = subparsers.add_parser(
        "check", help="validate the pull request target without calling the API"
    )
    check.add_argument("--base", default=DEFAULT_BASE, help="base branch (default main)")
    check.add_argument("--remote", default="origin", help="remote to inspect")
    check.add_argument(
        "--pr",
        dest="pull_request",
        type=int,
        help="also validate this existing pull request number",
    )
    check.set_defaults(handler=command_check)

    open_parser = subparsers.add_parser(
        "open", help="create a pull request against the origin repository"
    )
    open_parser.add_argument("--title", required=True, help="pull request title")
    open_parser.add_argument(
        "--body-file", help="file with the pull request body (markdown)"
    )
    open_parser.add_argument("--base", default=DEFAULT_BASE, help="base branch")
    open_parser.add_argument("--remote", default="origin", help="remote to target")
    open_parser.set_defaults(handler=command_open)

    args = parser.parse_args(argv)
    return int(args.handler(args))


if __name__ == "__main__":
    raise SystemExit(main())
