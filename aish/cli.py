"""Command-line interface for aish."""

import os
from typing import Optional

import typer
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from typer import Argument, Option

from aish.core import generate_command
from aish.utils import setup_logging, print_header, print_help, print_command

# Initialize Typer app
app = typer.Typer(
    name="aish",
    help="Convert natural language instructions into bash commands",
    add_completion=False,
    rich_markup_mode="rich",
)

console = Console()
logger = setup_logging()

@app.command()
def main(
    instruction: Optional[str] = Argument(
        None,
        help="Natural language instruction to convert to bash command",
    ),
    model: Optional[str] = Option(
        "llama",
        "--model",
        "-m",
        help="Ollama model to use for command generation",
    ),
    temperature: Optional[float] = Option(
        0.2,
        "--temperature",
        "-t",
        help="Temperature for command generation (0.0 to 1.0)",
        min=0.0,
        max=1.0,
    ),
    yolo: Optional[bool] = Option(
        None,
        "--yolo",
        "-y",
        help="Use yolo mode (execute the command immediately)",
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
    if help or not instruction:
        print_header(console)
        print_help(console)
        raise typer.Exit()
        
    try:
        # Print header
        print_header(console)
        
        # Generate command
        command = generate_command(instruction, model, temperature)
        
        # Print the command
        print_command(console, command)
        
        # Ask for confirmation before executing
        if yolo or Prompt.ask(
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