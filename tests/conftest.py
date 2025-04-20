"""Shared fixtures for aish tests."""

from typing import Any

import pytest


@pytest.fixture
def mock_ollama_response() -> dict[str, Any]:
    """Fixture for mock Ollama API response."""
    return {
        "message": {
            "content": "```bash\nls -la\n```"
        }
    } 