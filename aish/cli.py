"""Command-line interface for aish."""

import os
from typing import Optional

import typer
import pyfiglet
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.markdown import Markdown
from rich.syntax import Syntax
from rich.table import Table
from typer import Argument, Option

from aish.core import generate_command
from aish.utils import setup_logging

# Initialize Typer app
app = typer.Typer(
    name="aish",
    help="Convert natural language instructions into bash commands",
    add_completion=False,
    rich_markup_mode="rich",
)

# Initialize console
console = Console()

# Setup logging
logger = setup_logging()

def print_header() -> None:
    """Print the aish header."""
    # 1. Generate art using pyfiglet (choose a font)
    try:
        # You can try different fonts like 'standard', 'slant', 'block', 'banner3-D', etc.
        font_style = 'standard' 
        ascii_art_text = pyfiglet.figlet_format("AISH", font='small')
    except pyfiglet.FontNotFound:
        print(f"[red]Error: pyfiglet font '{font_style}' not found. Using default.[/red]")
        ascii_art_text = pyfiglet.figlet_format("AISH") # Fallback to default
    except Exception as e:
        print(f"[red]Error generating pyfiglet art: {e}[/red]")
        ascii_art_text = "AISH" # Simple text fallback
    console.print(f"[bold green]{ascii_art_text}[/bold green]", justify="center")

def print_command(command: str) -> None:
    """Print the generated command in a nice format."""
    # Create a table for the command
    table = Table(show_header=False, box=None)
    table.add_column("Command", style="bold green")
    table.add_row(Syntax(command, "bash", theme="monokai", line_numbers=False))
    
    # Print in a panel
    console.print(Panel(
        table,
        title="[bold green]Generated Command[/bold green]",
        border_style="green",
        padding=(1, 2),
    ))

def print_help() -> None:
    """Print help information."""
    help_text = """
    [bold]Usage:[/bold]
      aish "your instruction"
    
    [bold]Examples:[/bold]
      • aish "Show disk usage"
      • aish "Find all Python files"
      • aish "List running processes"
    
    [bold]Options:[/bold]
      --model, -m      Model to use (default: llama2)
      --temperature, -t Temperature (0.0 to 1.0)
    """
    console.print(Panel(
        Markdown(help_text),
        title="[bold blue]Help[/bold blue]",
        border_style="blue",
        padding=(1, 2),
    ))

@app.command()
def main(
    instruction: str = Argument(
        ...,
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
    help: Optional[bool] = Option(
        None,
        "--help",
        "-h",
        help="Show this help message and exit.",
    ),
) -> None:
    """Convert natural language instructions into bash commands.
    
    Args:
        instruction: The natural language instruction to convert
        model: The Ollama model to use for command generation
        temperature: The temperature parameter for command generation
        help: Show help message
    """
    if help:
        print_header()
        print_help()
        raise typer.Exit()
        
    try:
        # Print header
        print_header()
        
        # Generate command
        command = generate_command(instruction, model, temperature)
        
        # Print the command
        print_command(command)
        
        # Ask for confirmation before executing
        if Prompt.ask(
            "\n[bold yellow]Execute command?[/bold yellow]",
            choices=["y", "n"],
            default="n",
            show_choices=True,
            show_default=True,
        ) == "y":
            console.print("\n[bold green]Executing command...[/bold green]\n")
            os.system(command)
            
    except Exception as e:
        logger.error(f"Error generating command: {e!s}")
        console.print(Panel(
            f"[red]Error: {e!s}[/red]",
            title="[bold red]Error[/bold red]",
            border_style="red",
        ))
        raise typer.Exit(1)

if __name__ == "__main__":
    app() 