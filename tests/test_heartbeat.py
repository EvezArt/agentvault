import hashlib
import importlib.util
import json
import unittest
from pathlib import Path
from unittest.mock import patch

MODULE_PATH = Path(__file__).resolve().parents[1] / "vault" / "heartbeat.py"
SPEC = importlib.util.spec_from_file_location("agentvault_heartbeat", MODULE_PATH)
heartbeat = importlib.util.module_from_spec(SPEC)
assert SPEC is not None and SPEC.loader is not None
SPEC.loader.exec_module(heartbeat)


class HeartbeatTests(unittest.TestCase):
    def test_digest_covers_canonical_event_without_claiming_export_count(self):
        event = heartbeat.build_event()
        supplied_digest = event.pop("sha256")
        canonical = json.dumps(
            event, sort_keys=True, separators=(",", ":"), ensure_ascii=False
        )
        self.assertEqual(hashlib.sha256(canonical.encode("utf-8")).hexdigest(), supplied_digest)
        self.assertEqual(event["local_vault_access"], "NOT_ACCESSED")
        self.assertNotIn("export_count", event)

    @patch.object(heartbeat.requests, "put")
    @patch.object(heartbeat, "LEDGER_GITHUB_TOKEN", "")
    def test_missing_ledger_token_fails_without_request(self, mock_put):
        with self.assertRaisesRegex(RuntimeError, "LEDGER_GITHUB_TOKEN"):
            heartbeat.post_heartbeat(heartbeat.build_event())
        mock_put.assert_not_called()

    @patch.object(heartbeat.requests, "put")
    @patch.object(heartbeat, "LEDGER_GITHUB_TOKEN", "test-ledger-token")
    def test_non_success_ledger_response_is_failure(self, mock_put):
        mock_put.return_value.status_code = 403
        with self.assertRaisesRegex(RuntimeError, "HTTP 403"):
            heartbeat.post_heartbeat(heartbeat.build_event())
        self.assertEqual(
            mock_put.call_args.kwargs["headers"]["Authorization"],
            "Bearer test-ledger-token",
        )
        self.assertEqual(mock_put.call_args.kwargs["timeout"], 15)

    @patch.object(heartbeat.requests, "put")
    @patch.object(heartbeat, "LEDGER_GITHUB_TOKEN", "test-ledger-token")
    def test_success_requires_accepted_response(self, mock_put):
        mock_put.return_value.status_code = 201
        path = heartbeat.post_heartbeat(heartbeat.build_event())
        self.assertTrue(path.startswith("DECISIONS/"))
        self.assertIn("agentvault_heartbeat_", path)

    @patch.object(heartbeat.requests, "post")
    @patch.object(heartbeat, "ABLY_KEY", "unused:test")
    @patch.object(heartbeat, "ENABLE_ABLY_HEARTBEAT", "false")
    def test_ably_is_disabled_by_default(self, mock_post):
        self.assertFalse(heartbeat.post_ably(heartbeat.build_event()))
        mock_post.assert_not_called()


if __name__ == "__main__":
    unittest.main()
