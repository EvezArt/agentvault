"""AgentVault — private vault + indexer for AI exports."""
from .sync_agent import scan_once, watch
from .search import app

__all__ = ["scan_once", "watch", "app"]
