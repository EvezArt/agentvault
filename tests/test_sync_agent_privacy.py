import importlib.util
import unittest
from pathlib import Path
from unittest.mock import patch

MODULE_PATH = Path(__file__).resolve().parents[1] / "vault" / "sync_agent.py"
SPEC = importlib.util.spec_from_file_location("agentvault_sync_agent", MODULE_PATH)
sync_agent = importlib.util.module_from_spec(SPEC)
assert SPEC is not None and SPEC.loader is not None
SPEC.loader.exec_module(sync_agent)


class SyncAgentPrivacyTests(unittest.TestCase):
    @patch.object(sync_agent.smtplib, "SMTP_SSL")
    @patch.object(sync_agent, "EMAIL_NOTIFICATIONS_ENABLED", False)
    def test_email_is_disabled_by_default(self, mock_smtp):
        sync_agent.send_email("test subject", "metadata only")
        mock_smtp.assert_not_called()

    @patch.object(sync_agent.smtplib, "SMTP_SSL")
    @patch.object(sync_agent, "EMAIL_NOTIFICATIONS_ENABLED", True)
    @patch.object(sync_agent, "NOTIFY_EMAIL", "")
    @patch.object(sync_agent, "GMAIL_USER", "configured-user")
    @patch.object(sync_agent, "GMAIL_PASS", "configured-password")
    def test_email_requires_explicit_recipient(self, mock_smtp):
        sync_agent.send_email("test subject", "metadata only")
        mock_smtp.assert_not_called()

    @patch.object(sync_agent.smtplib, "SMTP_SSL")
    @patch.object(sync_agent, "EMAIL_NOTIFICATIONS_ENABLED", True)
    @patch.object(sync_agent, "NOTIFY_EMAIL", "operator@example.invalid")
    @patch.object(sync_agent, "GMAIL_USER", "")
    @patch.object(sync_agent, "GMAIL_PASS", "")
    def test_email_requires_credentials(self, mock_smtp):
        sync_agent.send_email("test subject", "metadata only")
        mock_smtp.assert_not_called()


if __name__ == "__main__":
    unittest.main()
