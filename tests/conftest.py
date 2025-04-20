"""Shared fixtures for aish tests."""

import pytest
from typing import Dict, Any


@pytest.fixture
def mock_ollama_response() -> Dict[str, Any]:
    """Fixture for mock Ollama API response."""
    return {
        "message": {
            "content": "```bash\nls -la\n```"
        }
    } 