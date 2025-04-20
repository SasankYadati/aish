"""Command-line interface for aish."""

import os

import typer
from rich.console import Console
from rich.prompt import Prompt
from typer import Option

from aish.core import generate_command
from aish.utils import setup_logging

# Initialize Typer app
app = typer.Typer(
    name="aish",
    help="Convert natural language instructions into bash commands",
    add_completion=False,
)

# Initialize console
console = Console()

# Setup logging
logger = setup_logging()

@app.command()
def main(
    instruction: str = Option(
        ...,
        "--instruction",
        "-i",
        help="Natural language instruction to convert to bash command",
    ),
    model: str = Option(
        "hf.co/saisasanky/Llama-3.1-8B-Instruct-4bit-aish_gguf",
        "--model",
        "-m",
        help="Ollama model to use for command generation",
    ),
    temperature: float = Option(
        0.2,
        "--temperature",
        "-t",
        help="Temperature for command generation (0.0 to 1.0)",
        min=0.0,
        max=1.0,
    ),
) -> None:
    """Convert natural language instructions into bash commands.
    
    Args:
        instruction: The natural language instruction to convert
        model: The Ollama model to use for command generation
        temperature: The temperature parameter for command generation
    """
    try:
        # Generate command
        command = generate_command(instruction, model, temperature)
        
        # Print the command
        console.print("\n[bold green]Generated Command:[/bold green]")
        console.print(f"[yellow]{command}[/yellow]\n")
        
        # Ask for confirmation before executing
        if Prompt.ask("Execute command?", choices=["y", "n"], default="n") == "y":
            os.system(command)
            
    except Exception as e:
        logger.error(f"Error generating command: {e!s}")
        console.print(f"[red]Error: {e!s}[/red]")
        raise typer.Exit(1)

if __name__ == "__main__":
    app() 