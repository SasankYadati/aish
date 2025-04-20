"""Tests for the core functionality of aish."""

from typing import Any
from unittest.mock import patch

import pytest

from aish.core import generate_command


def test_generate_command_success(mock_ollama_response: dict[str, Any]) -> None:
    """Test successful command generation."""
    with patch("aish.core.ollama.chat") as mock_chat:
        mock_chat.return_value = mock_ollama_response
        
        instruction = "list all files in current directory"
        result = generate_command(instruction)
        
        assert result == "ls -la"
        mock_chat.assert_called_once()


def test_generate_command_without_markdown(mock_ollama_response: dict[str, Any]) -> None:
    """Test command generation when response doesn't have markdown formatting."""
    mock_response = {"message": {"content": "ls -la"}}
    
    with patch("aish.core.ollama.chat") as mock_chat:
        mock_chat.return_value = mock_response
        
        instruction = "list all files in current directory"
        result = generate_command(instruction)
        
        assert result == "ls -la"


def test_generate_command_empty_instruction() -> None:
    """Test command generation with empty instruction."""
    with pytest.raises(ValueError, match="Instruction cannot be empty"):
        generate_command("")


def test_generate_command_whitespace_instruction() -> None:
    """Test command generation with whitespace-only instruction."""
    with pytest.raises(ValueError, match="Instruction cannot be empty"):
        generate_command("   ")


def test_generate_command_ollama_error() -> None:
    """Test command generation when Ollama API returns an error."""
    with patch("aish.core.ollama.chat") as mock_chat:
        mock_chat.side_effect = Exception("API Error")
        
        with pytest.raises(Exception, match="Ollama API error"):
            generate_command("list files")


def test_generate_command_custom_model(mock_ollama_response: dict[str, Any]) -> None:
    """Test command generation with a custom model."""
    with patch("aish.core.ollama.chat") as mock_chat:
        mock_chat.return_value = {"message": {"content": "ls -la"}}
        
        instruction = "list all files in current directory"
        model = "custom-model"
        result = generate_command(instruction, model=model)
        
        assert result == "ls -la"
        mock_chat.assert_called_once_with(
            model=model,
            messages=[{"role": "user", "content": f"Convert this instruction to a bash command: {instruction}"}],
            options={"temperature": 0.2, "num_predict": 150}
        )


def test_generate_command_custom_temperature(mock_ollama_response: dict[str, Any]) -> None:
    """Test command generation with a custom temperature."""
    with patch("aish.core.ollama.chat") as mock_chat:
        mock_chat.return_value = {"message": {"content": "ls -la"}}
        
        instruction = "list all files in current directory"
        temperature = 0.5
        result = generate_command(instruction, temperature=temperature)
        
        assert result == "ls -la"
        mock_chat.assert_called_once_with(
            model="llama2",
            messages=[{"role": "user", "content": f"Convert this instruction to a bash command: {instruction}"}],
            options={"temperature": temperature, "num_predict": 150}
        ) 