"""Tests for the CLI functionality of aish."""

from typing import Any
from unittest.mock import patch

import pytest
from typer.testing import CliRunner

from aish.cli import app


@pytest.fixture
def runner() -> CliRunner:
    """Fixture for CLI runner."""
    return CliRunner()


def test_cli_success(runner: CliRunner, mock_ollama_response: dict[str, Any]) -> None:
    """Test successful CLI execution."""
    with patch("aish.core.ollama.chat") as mock_chat, \
         patch("aish.cli.Prompt.ask") as mock_prompt, \
         patch("os.system") as mock_system:
        
        mock_chat.return_value = mock_ollama_response
        mock_prompt.return_value = "n"  # Don't execute the command
        
        result = runner.invoke(
            app,
            ["--instruction", "list all files in current directory"]
        )
        
        assert result.exit_code == 0
        assert "Generated Command:" in result.output
        assert "ls -la" in result.output
        mock_chat.assert_called_once()
        mock_system.assert_not_called()


def test_cli_execute_command(runner: CliRunner, mock_ollama_response: dict[str, Any]) -> None:
    """Test CLI execution with command execution."""
    with patch("aish.core.ollama.chat") as mock_chat, \
         patch("aish.cli.Prompt.ask") as mock_prompt, \
         patch("os.system") as mock_system:
        
        mock_chat.return_value = mock_ollama_response
        mock_prompt.return_value = "y"  # Execute the command
        
        result = runner.invoke(
            app,
            ["--instruction", "list all files in current directory"]
        )
        
        assert result.exit_code == 0
        assert "Generated Command:" in result.output
        assert "ls -la" in result.output
        mock_chat.assert_called_once()
        mock_system.assert_called_once_with("ls -la")


def test_cli_custom_model(runner: CliRunner, mock_ollama_response: dict[str, Any]) -> None:
    """Test CLI with custom model."""
    with patch("aish.core.ollama.chat") as mock_chat, \
         patch("aish.cli.Prompt.ask") as mock_prompt:
        
        mock_chat.return_value = mock_ollama_response
        mock_prompt.return_value = "n"
        
        result = runner.invoke(
            app,
            [
                "--instruction", "list all files in current directory",
                "--model", "custom-model"
            ]
        )
        
        assert result.exit_code == 0
        mock_chat.assert_called_once()
        assert mock_chat.call_args[1]["model"] == "custom-model"


def test_cli_custom_temperature(runner: CliRunner, mock_ollama_response: dict[str, Any]) -> None:
    """Test CLI with custom temperature."""
    with patch("aish.core.ollama.chat") as mock_chat, \
         patch("aish.cli.Prompt.ask") as mock_prompt:
        
        mock_chat.return_value = mock_ollama_response
        mock_prompt.return_value = "n"
        
        result = runner.invoke(
            app,
            [
                "--instruction", "list all files in current directory",
                "--temperature", "0.5"
            ]
        )
        
        assert result.exit_code == 0
        mock_chat.assert_called_once()
        assert mock_chat.call_args[1]["options"]["temperature"] == 0.5


def test_cli_error_handling(runner: CliRunner) -> None:
    """Test CLI error handling."""
    with patch("aish.core.ollama.chat") as mock_chat:
        mock_chat.side_effect = Exception("API Error")
        
        result = runner.invoke(
            app,
            ["--instruction", "list all files in current directory"]
        )
        
        assert result.exit_code == 1
        assert "Error" in result.output


def test_cli_help(runner: CliRunner) -> None:
    """Test CLI help output."""
    result = runner.invoke(app, ["--help"])
    
    assert result.exit_code == 0
    assert "Convert natural language instructions into bash commands" in result.output
    assert "--instruction" in result.output
    assert "--model" in result.output
    assert "--temperature" in result.output 