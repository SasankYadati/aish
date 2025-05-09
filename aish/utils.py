"""Utility functions for aish."""

import logging
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.syntax import Syntax
from rich.table import Table
import pyfiglet
import time


def setup_logging() -> logging.Logger:
    """Set up logging configuration.
    
    Returns:
        A configured logger instance
    """
    # Create logs directory if it doesn't exist
    log_dir = Path.home() / ".aish" / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(log_dir / "aish.log"),
            logging.StreamHandler(),
        ],
    )
    
    return logging.getLogger("aish") 

def print_header(console: Console) -> None:
    """Print the aish header.
    
    Args:
        console: Rich console instance for printing
        yolo_mode: If True, displays a more trippy and fancy header.
    """
    try:
            ascii_art_text = pyfiglet.figlet_format("AISH", font='small')
            console.print(f"[bold green]{ascii_art_text}[/bold green]", justify="center")
    except Exception as e:
        print(f"[red]Error generating pyfiglet art: {e}[/red]")
        ascii_art_text = "AISH" # Simple text fallback
        console.print(f"[bold green]{ascii_art_text}[/bold green]", justify="center")

def print_command(console: Console, command: str) -> None:
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

def print_help(console: Console) -> None:
    """Print help information."""
    help_text = """
    Usage:
      • aish "your instruction"
      • aish "your instruction that you want to execute immediately" --yolo
    
    Examples:
      • aish "Show disk usage"
      • aish "Find all Python files"
      • aish "List running processes" --yolo
    
    Options:
      • --model, -m       Model to use (default: llama-3-8b)
      • --temperature, -t Temperature (0.0 to 1.0)
      • --yolo, -y        Execute the command immediately
    """
    console.print(Panel(
        Markdown(help_text),
        title="Help",
        border_style="blue",
        padding=(1, 2),
    ))