import importlib.util
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def load_module(name: str, filename: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / filename)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


pr = load_module("pr", "pr.py")


class RemoteParsingTests(unittest.TestCase):
    def test_https_urls(self):
        self.assertEqual(
            pr.parse_repository_slug("https://github.com/mauricioz/lila.git"),
            "mauricioz/lila",
        )
        self.assertEqual(
            pr.parse_repository_slug("https://github.com/mauricioz/lila"),
            "mauricioz/lila",
        )
        self.assertEqual(
            pr.parse_repository_slug("https://github.com/mauricioz/lila/"),
            "mauricioz/lila",
        )

    def test_ssh_urls(self):
        self.assertEqual(
            pr.parse_repository_slug("git@github.com:mauricioz/lila.git"),
            "mauricioz/lila",
        )
        self.assertEqual(
            pr.parse_repository_slug("ssh://git@github.com/mauricioz/lila.git"),
            "mauricioz/lila",
        )

    def test_unknown_urls(self):
        for value in ("", "not-a-url", "https://example.com/lila"):
            self.assertIsNone(pr.parse_repository_slug(value))


class TargetValidationTests(unittest.TestCase):
    def test_valid_target(self):
        self.assertEqual(
            pr.validate_target("mauricioz/lila", "devs/mauri/feat/x", "main"),
            [],
        )

    def test_upstream_is_refused(self):
        problems = pr.validate_target(
            "78/xiaozhi-esp32", "devs/mauri/feat/x", "main"
        )
        self.assertEqual(len(problems), 1)
        self.assertIn("78/xiaozhi-esp32", problems[0])

    def test_missing_repository_is_refused(self):
        problems = pr.validate_target(None, "devs/mauri/feat/x", "main")
        self.assertEqual(len(problems), 1)
        self.assertIn("origin", problems[0])

    def test_main_branch_is_refused(self):
        problems = pr.validate_target("mauricioz/lila", "main", "main")
        self.assertEqual(len(problems), 1)
        self.assertIn("feature branch", problems[0])

    def test_detached_head_is_refused(self):
        problems = pr.validate_target("mauricioz/lila", "", "main")
        self.assertEqual(len(problems), 1)
        self.assertIn("no branch", problems[0])


class PayloadTests(unittest.TestCase):
    def test_payload_shape(self):
        payload = pr.build_payload(
            "mauricioz/lila", "devs/mauri/feat/x", "main", "feat: thing", "body"
        )
        self.assertEqual(
            payload,
            {
                "title": "feat: thing",
                "head": "devs/mauri/feat/x",
                "base": "main",
                "body": "body",
            },
        )

    def test_payload_never_names_the_upstream(self):
        payload = pr.build_payload(
            "mauricioz/lila", "devs/mauri/feat/x", "main", "t", "b"
        )
        self.assertNotIn("78/xiaozhi-esp32", json_text(payload))


def json_text(payload: dict) -> str:
    import json

    return json.dumps(payload)


class RepositoryInspectionTests(unittest.TestCase):
    def test_origin_points_at_the_lila_repository(self):
        if not (ROOT / ".git").exists():
            self.skipTest("not a git checkout")
        self.assertEqual(pr.origin_slug(ROOT), "mauricioz/lila")

    def test_git_command_trusts_only_this_checkout(self):
        command = pr.git_command(ROOT, "remote", "get-url", "origin")
        self.assertEqual(command[0], "git")
        self.assertEqual(command[1], "-c")
        self.assertEqual(
            command[2], f"safe.directory={ROOT.as_posix()}"
        )
        self.assertEqual(command[3:], ["remote", "get-url", "origin"])

    def test_current_branch_is_not_main(self):
        if not (ROOT / ".git").exists():
            self.skipTest("not a git checkout")
        self.assertNotEqual(pr.current_branch(ROOT), "main")

    def test_slug_is_read_from_a_remote(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            subprocess.run(["git", "init", "-q"], cwd=root, check=True)
            subprocess.run(
                ["git", "remote", "add", "origin", "git@github.com:mauricioz/lila.git"],
                cwd=root,
                check=True,
            )
            self.assertEqual(pr.origin_slug(root), "mauricioz/lila")

    def test_missing_remote_yields_no_slug(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            subprocess.run(["git", "init", "-q"], cwd=root, check=True)
            self.assertIsNone(pr.origin_slug(root))


if __name__ == "__main__":
    unittest.main()
